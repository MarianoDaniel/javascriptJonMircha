"""Procurement API views

This file has the all procurement api
operations.
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import MultiPoint
from django.db import connections
import traceback
from IGIQ2.session_functions import process_rpf
from Procurement.session_functions import get_tax_for_vq
from datetime import datetime, timedelta, timezone
from django.views.decorators.csrf import csrf_exempt
import re
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
import traceback
from multiprocessing import Process
from django.db.models import Case, When, Value, CharField
from rest_framework import generics, status, pagination
from rest_framework import viewsets
from django.http import HttpResponse
import jwt
from IGIQ2.misc_functions import strip_accents
import random, string
from django.conf import settings as djsettings
import xlsxwriter
from django.core.files.base import ContentFile
from api.procurement.utilities import get_vendor_cost_predictor_model
from mysite.celery import (
    process_rpf_async,
    send_data_to_quickbase_async,
    # send_infeasibility_detected_async

)

from rest_framework.response import Response
from rest_framework.views import APIView
from mysite.settings import PRODUCTIONENVIROMENT, JWT_EMAIL_SECRET
from rest_framework.filters import OrderingFilter
from mysite.settings import graylog_logger


from mysite.quickbase_tables import (
    procurement_vendorquote_table,
    procurement_vendorquote_fields,
    procurement_vendor_catalog_fields,
    procurement_vendor_catalog_table,
    procurement_contact_table,
    procurement_contact_filds,
    procurement_vendor_contact_field,
    procurement_vendor_contact_table,
    procurement_task_field,
    procurement_task_table
)
from mysite.quickbase_app_tokens import procurement_token
from api.procurement.utilities import (save_into_qb,
    get_tax_for_data_geolocal,
    is_number,
    update_presences,
    update_service_offered,
    update_instances_inverse,
    create_presence_for_vendors_disolved,
    create_service_offered_for_vendors_disolved)
from api.procurement.utilities import create_dic
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from api.core.filters import (
    TaskFilter
)
from Procurement.models import (
    VendorCatalog,
    VendorQuotes,
    VendorContactRelation,
    Contact,
    VendorCoverage,
    Contact,
    VendorPricelist,
    Price,
    Taxes,
    Voc,
    VocLine,
    Presence,
    Tier,
    VCPMlog
)

from IGIQ2.models import (
    UserQuotes
)
from mysite.models import (
    Task,
    EmailLog,
    RelevantSites,
    Fiber,
    ServiceOffered,
    DataCenter)
# Permissions

# Serializers
from api.core.serializers import (
    TaskSerializer,
    TaskMapSerializer,
    VendorQuoteSerializer,
    VendorQuoteRelationsSerializer,
    VendorQuoteUpdateSerializer

)

# Serializers
from api.pricing.serializers import (
    VendorPricelistSerializer as VPLPricingSerializer
)
from api.procurement.serializers import (
    VendorCatalogRelationsSerializer,
    VendorCatalogSerializer,
    VendorsContactsSerializer,
    RelevantSitesSerializer,
    RelevantSitesWriteSerializer,
    FiberSerializer,
    FiberWriteSerializer,
    VendorCoverageSerializer,
    VendoCoverageWriteSerializer,
    ServiceOfferedSerializer,
    VendoCoverageWriteSerializer,
    VendorsContactsSerializer,
    VendorPricelistRelationsSerializer,
    VendorPriceSerializer,
    PriceRelationsSerializer,
    TaxSerializer,
    TaxRelationsSerializer,
    VocMinSerializer,
    VoclineMinSerializer,
    VocSerializer,
    VoclineSerializer,
    PresenceSerializer,
    PresenceWriteSerializer,
    ServiceOfferedWriteSerializer,
    DataCenterSerializer,
    DataCenterRelationsSerializer,
    TierSerializer,
    VendorPricelistSerializer,
    VCPMlogSerializer,
    VCPMlogRelationsSerializer,
)

from api.procurement.serializers import ContactSerializer
# Filters
from mysite.slug_generator import get_unique_slug
from .filters import (
    VendorQuoteFilter,
    VendorCatalogFilter,
    VendorsContactsFilter,
    VendorPricelistFilter,
    PresenceFilter,
    VoclineFilter,
    DataCenterFilter
)

# Quickbase Functions
from .quickbase_functions import (
    post_vendor_quote_in_quickbase,
    post_contact_in_quickbase,
    post_vendor_catalog_in_quickbase
)
from django.core.mail import (
    send_mail
)
# Adicional methods
from Procurement.session_functions import hash_to_vendorquotes_and_vendor, get_vendor_quotes_from_slug, \
    get_vendor_from_slug
from Procurement.email_functions import (send_email,
                                         is_valid_email,
                                         render_email_template,
                                         get_email)

from api.periodic_scripts.save_quickbase import send_to_quickbase_async_data
import time
from mysite.settings import (
    METABASE_SITE_URL,
    METABASE_SECRET_KEY
)
# Views or Viewsets

#-----

#Vendor Pricelist View

class VendorPricelistViewSet(viewsets.ModelViewSet):
    """

    """
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import cache_page
    from django.views.decorators.vary import vary_on_cookie, vary_on_headers

    #queryset = VendorPricelist.objects.all()
    queryset = VendorPricelist.objects.all().select_related(
        'fk_vendor_catalog',
        'fk_service_type',
        'fk_currency',
        'fk_created_by',
        'fk_updated_by',
    ).prefetch_related('delivery_points',
                       'presences',
                       'price_vendor_pricelist',
                       'comments',
                       ).order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': VendorPricelistRelationsSerializer,
        'update': VendorPricelistRelationsSerializer,
        'partial_update': VendorPricelistRelationsSerializer,
        'list': VendorPricelistSerializer,
        'retrieve': VendorPricelistSerializer,
        'destroy': VendorPricelistSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = VendorPricelistFilter

    #@method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    #Create

    def create(self, request, *args, **kwargs):
        """
        Create a CommonAddress object.
        :return:
            A 201 HTTP Response indicating
            the Vendor Pricelist creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """Perform the save operations.
        Returns:
            A Price creation in database
        """
        try:
            return serializer.save(fk_created_by=self.request.user,
                               created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []
    #Update

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Price update in database
        """
        try:
            return serializer.save(fk_updated_by=self.request.user,
                                   updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

#-----

#Vendor Pricelist View

class VPLPricingViewSet(viewsets.ModelViewSet):
    """

    """
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import cache_page
    from django.views.decorators.vary import vary_on_cookie, vary_on_headers

    #queryset = VendorPricelist.objects.all()
    queryset = VendorPricelist.objects.all().select_related(
        'fk_vendor_catalog',
        'fk_service_type',
        'fk_currency',
        'fk_created_by',
        'fk_updated_by',
    ).prefetch_related('delivery_points',
                       'presences',
                       'price_vendor_pricelist',
                       'comments',
                       ).order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'list': VPLPricingSerializer,
        'retrieve': VPLPricingSerializer,
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = VendorPricelistFilter

    #@method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

#-----

#Price View

class PriceViewSet(viewsets.ModelViewSet):
    """
    Price View Set
    """

    queryset = Price.objects.all().select_related(
        'fk_bw_up',
        'fk_bw_down',
        'fk_created_by',
        'fk_updated_by',
    ).order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': PriceRelationsSerializer,
        'update': PriceRelationsSerializer,
        'partial_update': PriceRelationsSerializer,

        'list': VendorPriceSerializer,
        'retrieve': VendorPriceSerializer,
        'destroy': VendorPriceSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    #filterset_class = PriceFilter

    def get_object(self):
        if self.request.method in ['PATCH', 'PUT']:
            queryset = self.filter_queryset(self.get_queryset())
            obj = queryset.filter(slug__in=[data['slug'] for data in self.request.data])
            self.check_object_permissions(self.request, obj)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            slug = self.kwargs['slug']
            try:
                obj = queryset.get(slug=slug)
            except Task.DoesNotExist:
                obj = None
            self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    #Create

    def create(self, request, *args, **kwargs):
        """
        Create a CommonAddress object.
        :return:
            A 201 HTTP Response indicating
            the Vendor Pricelist creation, otherwise
            an exception raise
        """

        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """Perform the save operations.
        Returns:
            A Price creation in database
        """
        try:
            return serializer.save(fk_created_by=self.request.user,
                                   created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    #Update

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Price update in database
        """
        try:
            return serializer.save(fk_updated_by=self.request.user,
                                   updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial, many=True)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

#-----

#Tax View


class TaxesPagination(pagination.PageNumberPagination):
    """
    Clase especifica donde se implementa la paginacion de Taxes
    """
    page_size = 300

class TaxViewSet(viewsets.ModelViewSet):
    """
    Tax ViewSet
    """

    queryset = Taxes.objects.all().select_related(
        'country',
        'city',
        'vendor',
        'fk_county',
        'fk_state',
        'fk_city',
        'fk_country',
    ).order_by('fk_country__name',
               'fk_state__name',
               'fk_county__name',
               'vendor__name'
               )

    pagination_class = TaxesPagination
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': TaxRelationsSerializer,
        'update': TaxRelationsSerializer,
        'partial_update': TaxRelationsSerializer,

        'list': TaxSerializer,
        'retrieve': TaxSerializer,
        'destroy': TaxSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    #filterset_class = TaxesFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except:
            print(traceback.format_exc())
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):

        try:
            instance.delete()
        except Exception:
            print(traceback.format_exc())

    def get_serializer_class(self):

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Tax model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    #Create
    def create(self, request, *args, **kwargs):
        """
        Create a Tax object.
        :return:
            A 201 HTTP Response indicating
            the Vendor Pricelist creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """Perform the save operations.
        Returns:
            A Tax creation in database
        """
        try:
            return serializer.save(fk_created_by=self.request.user,
                                   created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    #Update
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Price update in database
        """
        try:
            return serializer.save(fk_updated_by=self.request.user,
                               updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

#-----

#Voc View

class VocViewSet(viewsets.ModelViewSet):
    """
    Voc View
    """

    #queryset = Voc.objects.all()
    queryset = Voc.objects.all().select_related(
        'related_currency',
        'related_vendor',
        'created_by',
        'updated_by',
    ).prefetch_related('voc_lines_for').order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        #'create': VocRelationsSerializer,
        #'update': VocRelationsSerializer,
        #'partial_update': VocRelationsSerializer,

        'list': VocMinSerializer,
        'retrieve': VocMinSerializer,
        #'destroy': VocSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    #filterset_class = VocFilter

    def get_serializer_class(self):

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set id as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

#-----

#Voc View

class VoclineViewSet(viewsets.ModelViewSet):
    """
    Vocline View
    """

    #queryset = VocLine.objects.all()
    queryset = VocLine.objects.all().select_related(
        'related_equipment',
        'related_license',
        'related_proc_vq',
        'related_log_vq',
        'related_service_inventory',
        'fk_cross_connect',
        'related_voc',
        'created_by',
        'updated_by',
    ).order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        #'create': VoclineRelationsSerializer,
        #'update': VoclineRelationsSerializer,
        #'partial_update': VoclineRelationsSerializer,

        'list': VoclineMinSerializer,
        'retrieve': VoclineMinSerializer,
        #'destroy': VoclineSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = VoclineFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set id as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

#-----

# Task Viewset

class TaskViewSet(viewsets.ModelViewSet):
    """
    TaskViewSet

    ModelViewSet for Task objects. Include
    create(), update(), list(), destroy()
    operations
    """
    queryset = Task.objects.filter(content_type=ContentType.objects.get(model='userquotes')).select_related('department',
                        'created_by',
                        'updated_by'
    ).prefetch_related('assignee',
                              'content_object',
                              'content_object__related_currency',
                              'content_object__related_bw_down',
                              'content_object__related_bw_up',
                              'content_object__related_service_type',
                              'content_object__related_a_address',
                              'content_object__related_a_address__related_city',
                              'content_object__related_a_address__related_country',
                              'content_object__related_city',
                              'content_object__related_country',
                              'content_object__project',
                              'content_object__related_service',
                              'content_object__project__related_customer',
                              'content_object__project__assignee',
                              'content_object__project__source_user',
                              'content_object__related_endcustomer',
                              'content_object__quotevendor_quote',
                              'content_object__quotevendor_quote__vendor',
                              'content_object__quotevendor_quote__quote',
                              'dependant_on'
                              ).order_by('-is_escalated', 'priority', '-id')
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TaskFilter


    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk Taskmodel to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def get_object(self):
        if self.request.method in ['PUT', 'PATCH']:
            queryset = self.filter_queryset(self.get_queryset())
            obj = queryset.filter(slug__in=[data['slug'] for data in self.request.data])
            self.check_object_permissions(self.request, obj)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            slug = self.kwargs['slug']
            try:
                obj = queryset.get(slug=slug)
            except Task.DoesNotExist:
                obj = None
            self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """Create a Task object.

        Returns:
            A 201 HTTP Response indicating
            the Task creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data, many=True)
        # Check if is valid
        serializer.is_valid(raise_exception=True)

        # If serializer is valid, then save the object
        self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, *args, **kwargs):

        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_create(self, serializer):
        """Perform the save operations.

        Returns:
            A Task creation in database
        """
        # Creates the task
        try:
            serializer.save(created_by=self.request.user, created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Task creation in database
        """
        try:
            return serializer.save(updated_by=self.request.user,
                        updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def save_data_in_quickbase(self, user, created_objs):

        # Reanudo conexion
        try:
            conn = connections['default']
            conn.connect()
        except Exception:
            graylog_logger.error('TaskViewSet DB Reconnection Error \n' + str(traceback.format_exc()))
        else:
            # Guardar en quickbase
            # Analizar el response (code status)
            # Guardar error si fuera el caso.
            if created_objs and len(created_objs) > 0:
                try:
                    dict = create_dic(created_objs) # Se crea el diccionario con el modelo que corresponda, detecta solo el modelo
                    a, b = save_into_qb(procurement_task_field, dict, procurement_task_table, user, procurement_token,
                                 'API_ImportFromCSV', created_objs) # Guarda en quickbase y genera un registro en base de datos si falla
                except Exception:
                    graylog_logger.error('TaskViewSet XML Creation Error \n' + str(traceback.format_exc()))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial, many=True)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            # Celery
            if PRODUCTIONENVIROMENT:
                try:
                    id_list = [instance.id for instance in created_objs]
                except Exception:
                    id_list = []
                try:
                    send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'Task')
                except Exception:
                    # Aqui hacer algo con la captura de la excepcion.
                    graylog_logger.error('TaskViewSet \n '
                                         'Update Process Error \n' +
                                         str(traceback.format_exc())
                                         )


            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


# Task Viewset

class TaskMapViewSet(viewsets.ModelViewSet):
    """
    TaskViewSet

    ModelViewSet for Task objects. Include
    create(), update(), list(), destroy()
    operations
    """

    queryset = Task.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'task_id'
    pagination_class = None
    serializer_class = TaskMapSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

# Task Dashboard
class TaskDashboardViewSet(generics.ListAPIView):
    """
    TaskDashboardViewSet

    ListAPIView for Task objects. Include
    list(), destroy()
    operations
    """

    queryset = Task.objects.filter(content_type__model='userquotes')\
        .prefetch_related('assignee', 'content_object').order_by('-is_escalated', 'priority', '-id')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.count()

    def list(self, request, *args, **kwargs):
        quantity = self.filter_queryset(self.get_queryset())
        return Response({
            'count': quantity
        })

# VendorQuote Dashboard
class VendorQuoteDashboardViewSet(generics.ListAPIView):
    """
    VendorQuoteDashboardViewSet

    ListAPIView for VendorQuote objects. Include
    list(), destroy()
    operations
    """

    queryset = VendorQuotes.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = VendorQuoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VendorQuoteFilter

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.count()

    def list(self, request, *args, **kwargs):
        quantity = self.filter_queryset(self.get_queryset())
        return Response({
            'count': quantity
        })


# VendorCatalog Dashboard
class VendorCatalogDashboardViewSet(generics.ListAPIView):
    """
    VendorCatalogDashboardViewSet

    ListAPIView for Vendor objects. Include
    list(), destroy()
    operations
    """

    queryset = VendorCatalog.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = VendorCatalogSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VendorCatalogFilter

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.count()

    def list(self, request, *args, **kwargs):
        quantity = self.filter_queryset(self.get_queryset())
        return Response({
            'count': quantity
        })


class VendorQuoteGetTaxes(generics.ListAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        if 'lat' in self.request.data and \
           'lon' in self.request.data and \
           'vendor_slug' in self.request.data:
            tax_nrc, tax_mrc = get_tax_for_data_geolocal(
                self.request.data['lat'],
                self.request.data['lon'],
                self.request.data['vendor_slug']
            )
            if tax_nrc is not None:
                return JsonResponse(dict(nrc_tax_percentage=tax_nrc, mrc_tax_percentage=tax_mrc), safe=False)
            else:
                return JsonResponse({}, safe=False)
        return Response(json.dumps({}), status=status.HTTP_404_NOT_FOUND, content_type='application/json')


class VendorQuoteViewSet(viewsets.ModelViewSet):
    """VendorQuoteViewSet

    ModelViewSet for VendorQuote objects. Include
    create(), update(), list(), destroy()
    operations

    """
    #2.87, 2.96
    queryset = VendorQuotes.geo_objects.all().select_related(
        'related_service_type',
        'vendor',
        'related_currency',
        'related_city',
        'related_country',
        'related_a_address',
        'related_bw_up',
        'related_bw_down',
        'fk_task',
        'created_by',
        'last_updated_by'
    ).prefetch_related('fk_task__content_object',
                       'fk_task__content_object__quotevendor_quote',
                       'related_country__currency_country',
                       'related_a_address__related_city',
                       'related_a_address__related_country',
                       'fk_task__assignee',
                       'fk_task__department',
                       'fk_task__content_type'
                       ).order_by('-id')
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': VendorQuoteRelationsSerializer,
        'update': VendorQuoteUpdateSerializer,
        'partial_update': VendorQuoteUpdateSerializer,
        'list': VendorQuoteSerializer,
        'retrieve': VendorQuoteSerializer,
        'destroy': VendorQuoteSerializer
    }
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = VendorQuoteSerializer
    filterset_class = VendorQuoteFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorQuote Model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug is None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def get_object(self):
        if self.request.method in ['PUT', 'PATCH']:
            queryset = self.filter_queryset(self.get_queryset())
            try:
                obj = queryset.filter(slug__in=[data['slug'] for data in self.request.data])
            except (KeyError, ValueError):
                obj = None
            self.check_object_permissions(self.request, obj)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            slug = self.kwargs['slug']
            try:
                obj = queryset.get(slug=slug)
            except VendorQuotes.DoesNotExist:
                obj = None
            self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """Create a Vendor quote object.

        Returns:
            A 201 HTTP Response indicating
            the Vendor Quote creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data

        serializer = self.get_serializer(data=request.data, many=True)
        # Check if is valid
        serializer.is_valid(raise_exception=True)
        # If serializer is valid, then save the object
        try:
            created_objs = self.custom_perform_create(serializer)
        except Exception:
            created_objs = []
            graylog_logger.error('VendorQuoteViewSet Creacion Vendor Quotes: ' + traceback.format_exc())

        # Celery
        if PRODUCTIONENVIROMENT:
            try:
                id_list = [instance.id for instance in created_objs]
            except Exception:
                id_list = []
            try:
                send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorQuote')
                #send_to_quickbase_async_data(id_list, self.request.user.username, 'VendorQuote')
            except Exception:
                # Aqui hacer algo con la captura de la excepcion.
                graylog_logger.error('VendorQuoteViewSet \n '
                                     'Creation Process Error \n' +
                                     str(traceback.format_exc())
                                     )

        headers = self.get_success_headers(serializer.data)
        return Response([{"slug": item['slug']} for item in serializer.data],
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """Perform the save operations.

        Returns:
            A Vendor Quote creation in database
        """
        # Creates the vendor quote
        try:
            return serializer.save(created_by=self.request.user)
        except Exception:
            print(traceback.format_exc())
            return []

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def save_data_in_quickbase(self, user, created_objs):

        # Reanudo conexion
        try:
            conn = connections['default']
            conn.connect()
        except Exception:
            graylog_logger.error('VendorQuoteViewSet DB Reconnection Error \n' + str(traceback.format_exc()))
        else:
            # Guardar en quickbase
            # response, listresponse = post_vendor_quote_in_quickbase(created_objs, user)
            # Analizar el response (code status)
            # Guardar error si fuera el caso.
            if created_objs and len(created_objs) > 0:
                try:
                    # Se crea el diccionario con el modelo que corresponda, detecta solo el modelo
                    dict = create_dic(created_objs)
                    # Guarda en quickbase y genera un registro en base de datos si falla
                    a, b = save_into_qb(procurement_vendorquote_fields, dict, procurement_vendorquote_table,
                                        user, procurement_token, 'API_ImportFromCSV', created_objs)
                except Exception:
                    graylog_logger.error('VendorQuoteViewSet XML Creation Error \n' + str(traceback.format_exc()))

    def partial_update(self, request, *args, **kwargs):

        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A VendorQuote update in database
        """
        try:
            return serializer.save(last_updated_by=self.request.user,
                        last_updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial, many=True)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            # Aca hacemos un proceso paralelo
            if PRODUCTIONENVIROMENT:
                try:
                    id_list = [instance.id for instance in created_objs]
                except Exception:
                    id_list = []
                try:
                    send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorQuote')
                    # send_to_quickbase_async_data(id_list, self.request.user.username, 'VendorQuote')
                except Exception:
                    # Aqui hacer algo con la captura de la excepcion.
                    graylog_logger.error('VendorQuoteViewSet \n '
                                         'Update Process Error \n' +
                                         str(traceback.format_exc())
                                         )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)


class VendorCatalogViewSet(viewsets.ModelViewSet):
    """
    VendorCatalogViewSet

    ModelViewSet for VendorCatalog objects. Include
    create(), update(), list(), destroy()
    operations
    """

    queryset = VendorCatalog.objects.all().order_by('name')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = VendorCatalogSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VendorCatalogFilter
    serializer_action_classes = {
        'create': VendorCatalogRelationsSerializer,
        'update': VendorCatalogRelationsSerializer,
        'partial_update': VendorCatalogRelationsSerializer,
        'list': VendorCatalogSerializer,
        'retrieve': VendorCatalogSerializer,
        'destroy': VendorCatalogSerializer

    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(slug=slug)
        return queryset

    def get_object(self):
        if self.request.method in ['PUT', 'PATCH']:
            queryset = self.filter_queryset(self.get_queryset())
            try:
                obj = queryset.filter(slug__in=[data['slug'] for data in self.request.data])
            except Exception:
                obj = []
            self.check_object_permissions(self.request, obj)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            slug = self.kwargs['slug']
            try:
                obj = queryset.get(slug=slug)
            except VendorCatalog.DoesNotExist:
                obj = None
            self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """Create a VendorCatalog object.

        Returns:
            A 201 HTTP Response indicating
            the Task creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data

        serializer = self.get_serializer(data=request.data, many=True)
        # Check if is valid
        serializer.is_valid(raise_exception=True)

        try:
            created_objs = self.custom_perform_create(serializer)
        except Exception:
            created_objs = []
            graylog_logger.error('VendorQuoteViewSet Creation Error \n' + str(traceback.format_exc()))

        # Aca llamamos a celery

        if PRODUCTIONENVIROMENT:
            try:
                id_list = [instance.id for instance in created_objs]
            except Exception:
                id_list = []
            try:
                #send_to_quickbase_async_data(id_list, self.request.user.username, 'VendorCatalog') # Descomentar si se prueba de local
                send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorCatalog') # comentar si se prueba de local

            except Exception:
                # Aqui hacer algo con la captura de la excepcion.
                graylog_logger.error('VendorCatalogViewSet \n '
                                     'Process Error \n' +
                                     str(traceback.format_exc())
                                     )

        headers = self.get_success_headers(serializer.data)
        return Response([{"slug": item['slug']} for item in serializer.data], status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_create(self, serializer):
        """Perform the save operations.

           Returns:
               A Vendor Catalog creation in database
           """
        try:
            return serializer.save(created_by=self.request.user)
        except Exception:
            print(traceback.format_exc())
            return []


    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Vendor Catalog creation in database
        """
        try:
            return serializer.save(last_updated_by=self.request.user,
                        last_updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, many=True)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Aca hacemos un proceso paralelo
        if PRODUCTIONENVIROMENT:
            try:
                id_list = [instance.id for instance in created_objs]
            except Exception:
                id_list = []
            try:
                send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorCatalog')

            except Exception:
                # Aqui hacer algo con la captura de la excepcion.
                graylog_logger.error('VendorCatalogViewSet \n '
                                     'Process Error \n' +
                                     str(traceback.format_exc())
                                     )

        return Response(status=status.HTTP_200_OK)

    def save_data_in_quickbase(self, user, data):

        # Reanudo conexion
        try:
            conn = connections['default']
            conn.connect()
        except Exception:
            graylog_logger.error('VendorQuoteViewSet DB Reconnection Error \n' + str(traceback.format_exc()))

        # Guardar en quickbase
        if data and len(data) > 0:
            try:
                dict = create_dic(data)  # Se crea el diccionario con el modelo que corresponda, detecta solo el modelo
                a, b = save_into_qb(procurement_vendor_catalog_fields, dict, procurement_vendor_catalog_table, user, procurement_token,
                             'API_ImportFromCSV',
                             data)  # Guarda en quickbase y genera un registro en base de datos si falla
            except Exception:
                graylog_logger.error('VendorQuoteViewSet XML Creation Error \n' + str(traceback.format_exc()))

class CodeGeneratorAPIViewSet(viewsets.generics.ListAPIView):
    """CodeGeneratorAPIViewSet


    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):

        if 'vendorName' in self.request.query_params:
            from api.procurement.utilities import vendor_code_name_generator as vcg
            try:
                name = vcg(strip_accents(self.request.query_params['vendorName']))
            except (Exception):
                return HttpResponse(json.dumps({}), status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            return HttpResponse(json.dumps({'code_generated': name}), content_type='application/json')

        return HttpResponse(json.dumps({}), status=status.HTTP_404_NOT_FOUND, content_type='application/json')


# Contact Viewset

class ContactsViewSet(viewsets.ModelViewSet):
    """
    ContactsViewSet

    ModelViewSet for Contacts objects. Include
    create(), update(), list(), destroy()
    operations
    """
    queryset = Contact.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = ContactSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    # filterset_class = ContactFilter

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk Contact to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(slug=slug)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a Task object.

        Returns:
            A 201 HTTP Response indicating
            the Task creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data, many=True)
        # Check if is valid
        serializer.is_valid(raise_exception=True)

        # If serializer is valid, then save the object
        self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        request.data['updated_at'] = datetime.now(tz=timezone.utc)
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_create(self, serializer):
        """Perform the save operations.

        Returns:
            A Contact creation in database
        """
        # Creates the Contacts
        try:
            return serializer.save(created_by=self.request.user, created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


# Contact Viewset
class ContactsMapViewSet(viewsets.ModelViewSet):
    """
    ContactsMapViewSet

    ModelViewSet for ContactsMap objects. Include
    create(), update(), list(), destroy()
    operations
    """

    queryset = Task.objects.all().order_by('assignee__first_name', 'assignee__last_name')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'task_id'
    pagination_class = None
    serializer_class = TaskMapSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class VendorsContactsViewSet(viewsets.ModelViewSet):
    queryset = VendorContactRelation.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = VendorsContactsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VendorsContactsFilter
    serializer_action_classes = {
        'create': VendorsContactsSerializer,
        'update': VendorsContactsSerializer,
        'partial_update': VendorsContactsSerializer,
        'list': VendorsContactsSerializer,
        'destroy': VendorsContactsSerializer
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorsContactsModel to return response
        """
        id = self.request.query_params.get("id", None)
        if id is None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(id=id)
        return queryset

    def get_object(self):
        if self.request.method in ['PUT', 'PATCH']:
            queryset = self.filter_queryset(self.get_queryset())
            try:
                obj = queryset.filter(vendor__slug__in=[data['vendor'] for data in self.request.data])
            except Exception:
                obj = []
            self.check_object_permissions(self.request, obj)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            try:
                id = self.kwargs['id'] if self.kwargs != {} else None
                obj = queryset.get(id=id)
            except VendorContactRelation.DoesNotExist:
                obj = None
            self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        """Create a VendorsContacts object.

        Returns:
            A 201 HTTP Response indicating
            the Task creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        #request.data['created_by'] = self.request.user
        serializer = None
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
            print(traceback.format_exc())
        # If serializer is valid, then save the object
        try:
            created_objs = self.custom_perform_create(serializer)
        except:
            created_objs = None
        headers = self.get_success_headers(serializer.data)
        response = {}
        if created_objs is not None:
            try:
                response['vendorcontact'] = created_objs.id
                response['vendor'] = created_objs.vendor.slug
                response['contact'] = created_objs.contact.slug
            except (KeyError, ValueError, AttributeError, VendorContactRelation.DoesNotExist):
                graylog_logger.error('VendorsContactsViewSet Creation Error \n' + str(traceback.format_exc()))

        # Aca hacemos un proceso paralelo
        if PRODUCTIONENVIROMENT:
            try:
                id_list = [ created_objs.id]
            except Exception:
                id_list = []
            try:
                #send_to_quickbase_async_data(id_list, self.request.user.username, 'VendorContact')
                send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorContact')
            except Exception:
                # Aqui hacer algo con la captura de la excepcion.
                graylog_logger.error('VendorContactViewSet \n '
                                     'Process Error \n' +
                                     str(traceback.format_exc())
                                     )

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        for data in request.data:
            data['modified_by'] = self.request.user.username
        serializer = self.get_serializer(instance, data=request.data, partial=partial, many=True)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_update(serializer)

        # Aca hacemos un proceso paralelo
        if PRODUCTIONENVIROMENT:
            try:
                id_list = [elem.id for elem in created_objs]
            except Exception:
                id_list = []
            try:
                #send_to_quickbase_async_data(id_list, self.request.user.username, 'VendorContact')
                send_data_to_quickbase_async.delay(id_list, self.request.user.username, 'VendorContact')
            except Exception:
                # Aqui hacer algo con la captura de la excepcion.
                graylog_logger.error('VendorContactViewSet \n '
                                     'Process Error \n' +
                                     str(traceback.format_exc())
                                     )
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_create(self, serializer):
        try:
            return serializer.save(created_by=self.request.user)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A VendorsContacts creation in database
        """
        try:
            return serializer.save(modified_by=self.request.user)
        except Exception:
            print(traceback.format_exc())
            return None

    def save_data_in_quickbase(self,  data, user):
        # Reanudo conexion
        try:
            conn = connections['default']
            conn.connect()
        except Exception:
            graylog_logger.error('VendorContactViewSet DB Reconnection Error \n' + str(traceback.format_exc()))
        # Guardar en quickbase
        if data and len(data) > 0:

            try:
                dict = create_dic(data)  # Se crea el diccionario con el modelo que corresponda, detecta solo el modelo
                save_into_qb(procurement_vendor_contact_field, dict, procurement_vendor_contact_table, user, procurement_token,
                         'API_ImportFromCSV',
                         data)  # Guarda en quickbase y genera un registro en base de datos si falla
            except Exception:
                graylog_logger.error('VendorContactViewSet XML Creation Error \n' + str(traceback.format_exc()))


class RelevantSitesViewSet (viewsets.ModelViewSet):
    queryset = RelevantSites.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = RelevantSitesSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_action_classes = {
        'partial_update': RelevantSitesWriteSerializer,
        'list': RelevantSitesSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(slug=slug)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs['slug']
        try:
            obj = queryset.get(slug=slug)
        except RelevantSites.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

class FiberViewSet (viewsets.ModelViewSet):
    queryset = Fiber.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = FiberSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_action_classes = {
        'partial_update': FiberWriteSerializer,
        'list': FiberSerializer,
        'retrieve': FiberSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(slug=slug)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs['slug']
        try:
            obj = queryset.get(slug=slug)
        except Fiber.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

class VendorcoverageViewSet (viewsets.ModelViewSet):
    queryset = VendorCoverage.objects.all().select_related(
        'related_vendor',
        'fk_county_coverage',
        'fk_state_coverage',
        'fk_country_coverage'
    ).prefetch_related('presences')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = VendorCoverageSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_action_classes = {
        'partial_update': VendoCoverageWriteSerializer,
        'list': VendorCoverageSerializer,
        'retrieve': VendorCoverageSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        id = self.request.query_params.get("id", None)
        if id == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(id=id)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        id = self.kwargs['id']
        try:
            obj = queryset.get(id=id)
        except VendorCoverage.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class ServiceOfferedViewSet (viewsets.ModelViewSet):
    queryset = ServiceOffered.objects.all().select_related(
        'fk_vendor',
        'fk_service_type',
        'fk_bw_lower_limit',
        'fk_bw_upper_limit'
    )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = ServiceOfferedSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_action_classes = {
        'create': ServiceOfferedWriteSerializer,
        'partial_update': ServiceOfferedWriteSerializer,
        'list': ServiceOfferedSerializer,
        'retrieve': ServiceOfferedSerializer,
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        id = self.request.query_params.get("id", None)
        if id == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(id=id)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        id = self.kwargs['id']
        try:
            obj = queryset.get(id=id)
        except ServiceOffered.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class PresencesViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.all().select_related(
        'fk_vendor',
        'fk_old_vendorcoverage'
    ).prefetch_related(
        'content_object',
        #'content_object__geometry_set'
    )
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = PresenceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PresenceFilter

    serializer_action_classes = {
        'create': PresenceWriteSerializer,
        'partial_update': PresenceSerializer,
        'list': PresenceSerializer,
        'retrieve': PresenceSerializer,
        'destroy':PresenceSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorCatalogModel to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(slug=slug)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs['slug']
        try:
            obj = queryset.get(slug=slug)
        except Presence.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_create(self, serializer):
        #return serializer.save(created_by=self.request.user)
        try:
            return serializer.save()
        except Exception:
            print(traceback.format_exc())
            return []

    def create(self, request, *args, **kwargs):
        """Create a VendorsContacts object.

        Returns:
            A 201 HTTP Response indicating
            the Task creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        request.data['created_by'] = self.request.user
        serializer = None
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
            print(traceback.format_exc())
        # If serializer is valid, then save the object
        try:
            created_objs = self.custom_perform_create(serializer)
        except Exception:
            print(traceback.format_exc())
        headers = self.get_success_headers(serializer.data)
        response = serializer.data


        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class ProcessRFP(APIView):
    """ProcessRFP
     Call process_rpf_async
    :param request: quotes_ids
    :return: Async call process_rpf
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):

        rand_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        path = djsettings.MEDIA_ROOT + "/" + rand_name + "_rfp.xlsx"

        if 'quotes_ids' in request.data and 'buffer' in request.data:
            try:
                quotes = UserQuotes.objects.filter(cq_id__in=json.loads(request.data['quotes_ids'])).order_by('cq_id')
                workbook = xlsxwriter.Workbook(path)
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, "Quote ID")
                worksheet.write(0, 1, "Direccion")
                worksheet.write(0, 2, "Latitud")
                worksheet.write(0, 3, "Longitud")
                worksheet.write(0, 4, "Country")
                worksheet.write(0, 5, "City")
                for idx, quote in enumerate(quotes):
                    worksheet.write(idx + 1, 0, str(quote.cq_id) if quote.cq_id is not None else '')
                    worksheet.write(idx + 1, 1, str(quote.z_address) if quote.z_address is not None else '')
                    worksheet.write(idx + 1, 2, str(quote.latitude) if quote.latitude is not None else '')
                    worksheet.write(idx + 1, 3, str(quote.longitude) if quote.longitude is not None else '')
                    worksheet.write(idx + 1, 4, str(quote.city) if quote.city is not None else '')
                    worksheet.write(idx + 1, 5, str(quote.related_country.name) if quote.related_country is not None else '')
                workbook.close()

                buffer = request.data['buffer'] if is_number(request.data['buffer']) else None
                first_name = request.user.first_name
                email = request.user.email
                process_rpf_async.delay(path, first_name, email, True, None, False, 'Procurement', buffer)
                # process_rpf(path, first_name, email, True, None, False, 'Procurement', buffer) # DESCOMENTAR PARA PROBAR LOCAL
                return Response(status=status.HTTP_200_OK, content_type='application/json')

            except Exception(KeyError, ValueError, AttributeError):
                print(traceback.format_exc())

        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


class MetaBaseApi(APIView):
    """
        Class View MetaBase
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        """
        :param request: Obligatorio Nro de Dashboard que necesita de MetaBase.
                        Obligatorio type para saber que parametros trae.
        :param args:
        :param kwargs:
        :return: Url para acceder al DashBoard Publico de Metabase
        """

        payload = dict()

        if 'type' in request.data and request.data['type'] == 'vendor':
            payload = {
                'resource': {'dashboard': request.data['dashboard'] if 'dashboard' in request.data else None},
                'params':{
                            'name_vendor': request.data['name_vendor'] if 'name_vendor' in request.data else None,
                            'date_range': request.data['date_range'] if 'date_range' in request.data else None
                         },
                'exp': round(time.time()) + (60 * 10)
            }

        try:
            token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
            iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf8") + "#bordered=true&titled=true"
            return Response(status=status.HTTP_200_OK, content_type='application/json', data = {'iframe': iframeUrl} )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


#
#
# Methods Container
#
#
#
@csrf_exempt
def send_email_to_vendor(request):
    """
     Send email to Vendor function
    :param request:
    :return: True if email was send succesful otherwise False
    """
    message = ''
    info_response = {"message": [], "email": None, "created": None}
    stream = BytesIO(request.body)
    body_data = JSONParser().parse(stream)

    if request.method == "POST":

        vq_slugs_list = body_data['vqs'] if 'vqs' in body_data else []
        vendor_id = body_data['vendor'] if 'vendor' in body_data else None
        if len(vq_slugs_list) > 0 and vendor_id:
            try:
                email_log = EmailLog.objects.create()
                jwt_payload = {'email_log': email_log.id, 'vqs': vq_slugs_list, 'vendor': vendor_id}
                jwt_hash = jwt.encode({'email_log': email_log.id}, JWT_EMAIL_SECRET, algorithm='HS256').decode("utf-8")
                vq_list = get_vendor_quotes_from_slug(vq_slugs_list)
            except Exception:
                info_response["message"].append("ERROR: Failed to create JWT or get VQs")
                info_response["created"] = False
                info_response["email"] = body_data
                email_notificacion_error('ERROR: Failed to create JWT or get VQs: \n %s ' % body_data)
                return HttpResponse(json.dumps(info_response), status=500)
            else:
                try:
                    try:
                        body = render_email_template(vq_list, body_data['language'], request.user, body_data['header'], body_data['footer'], jwt_hash)
                        thread_id = body_data['threadId'] if 'threadId' in body_data else ''
                        in_reply_to = body_data['inReplyTo'] if 'inReplyTo' in body_data else ''
                        subject = body_data['subject']
                        to_contacts = [email for email in body_data['toContacts'] if is_valid_email(email)] if 'toContacts' in body_data else []
                        cc_contacts = [email for email in body_data['ccContacts'] if is_valid_email(email)] if 'ccContacts' in body_data else []
                        cc_contacts.append('procurement@ignetworks.com')

                        if not to_contacts:
                            info_response["created"] = False
                            info_response["message"].append("ERROR: No valid TO recipients")
                            info_response["email"] = body_data
                            email_notificacion_error('Error to contacts invalido: \n %s ' % body_data)
                            return HttpResponse(json.dumps(info_response), status=400)
                        try:
                            vendor_found = VendorCatalog.objects.get(slug=vendor_id)
                        except (VendorCatalog.DoesNotExist, AttributeError, KeyError, ValueError):
                            info_response["created"] = False
                            info_response["message"].append("ERROR: No valid Vendor or Vendor code name")
                            info_response["email"] = body_data
                            email_notificacion_error('ERROR: No valid Vendor or Vendor code name: \n %s ' % body_data)
                            return HttpResponse(json.dumps(info_response), status=400)

                        email = send_email(sender=request.user.email,
                                           to=','.join(to_contacts),
                                           subject=subject,
                                           body=body,
                                           cc=','.join(cc_contacts) if cc_contacts else '',
                                           thread_id=thread_id,
                                           in_reply_to=in_reply_to,
                                           user=request.user
                                           )

                    except Exception:
                        print(traceback.format_exc())
                        message = None
                        result = 'Failed send email algorithm'
                        email_notificacion_error('Failed send email algorithm: \n %s ' % body_data)
                    else:
                        if email is not None:
                            for vq in vq_list:
                                vq.email_outreach = 'sent'
                                vq.save()
                            message = get_email(email['id'])
                            result = 'Message Sent'

                            EmailLog.objects.filter(id=email_log.id).update(
                                payload=jwt_payload,
                                subject=subject,
                                to=','.join(to_contacts),
                                cc=','.join(cc_contacts),
                                sent_by=request.user,
                                thread_id=email['threadId'],
                                message_id=format(message['Message-Id']),
                            )

                    if message is not None:
                        info_response['message'] = "succesful"
                        info_response['created'] = True
                        return HttpResponse(json.dumps(info_response), status=200, content_type="application/json")
                    else:
                        info_response["created"] = False
                        info_response["message"].append(result)
                        info_response["email"] = body_data
                        email_notificacion_error('mensagge vacio: \n %s ' % body_data)
                        return HttpResponse(json.dumps(info_response), status=400)

                except Exception:
                    print(traceback.format_exc())
                    info_response["created"] = False
                    info_response["message"].append("ERROR: Bad request format")
                    info_response["email"] = body_data
                    email_notificacion_error('ERROR: Bad request format: \n %s ' % body_data)
                    return HttpResponse(json.dumps(info_response), status=400)
        else:
            info_response["message"].append("ERROR: Vendor quote or Vendor missing")
            info_response["created"] = False
            info_response["email"] = body_data
            email_notificacion_error('ERROR: Vendor quote or Vendor missing: \n %s ' % body_data)
            return HttpResponse(json.dumps(info_response), status=400)
    else:
        info_response["message"].append("ERROR: Bad request format")
        info_response["created"] = False
        info_response["email"] = body_data
        email_notificacion_error('ERROR: Bad request format: \n %s ' % body_data)
        return HttpResponse(json.dumps(info_response), status=400)


def email_notificacion_error(msg):
    send_mail(
        'IGIQ | Error Send Email to Vendor',
        msg,
        'IG Networks | IT Team',
        ['lmercado@ignetworks.com'],
        fail_silently=True
    )

class AcquisicionVendor(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):

        response_status = None

        try:
            response_status = Response(status=status.HTTP_200_OK)
            vendor_catalog_disolved = VendorCatalog.objects.get(slug=str(request.data['acquired_vendor']))
            vendor_catalog_permanent = VendorCatalog.objects.get(slug=str(request.data['permanent_vendor']))
            #Create Presence and ServiceOffered
            if (create_presence_for_vendors_disolved(vendor_catalog_disolved, vendor_catalog_permanent) and
                    create_service_offered_for_vendors_disolved(vendor_catalog_disolved, vendor_catalog_permanent)):

                # Guardo cambios del vendorcatalog Permanent con fk_acquisitor_vendor nuevo
                try:
                    # Asignacion del atributo fk_acquisitor_vendor
                    vendor_catalog_permanent.fk_acquisitor_vendor = vendor_catalog_disolved
                    vendor_catalog_disolved.status = 'inactive'
                    vendor_catalog_permanent.save()
                    vendor_catalog_disolved.save()
                    response_status = Response(status=status.HTTP_200_OK)
                except (AttributeError, TypeError, KeyError):
                    print(str(traceback.format_exc()))
                    graylog_logger.error(
                        'Fails to save vendorcatalog permanent and disolved in adquicit url'.format(str(traceback.format_exc())))
                    response_status = Response({'Validation Error - Fails to save vendors': 'Bad request format'},
                                               status=status.HTTP_400_BAD_REQUEST)

            else:
                response_status = Response({'Validation Error - Fails to create Presences': 'Bad request format'},
                                           status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, TypeError, KeyError):
            print(str(traceback.format_exc()))
            response_status = Response({'Validation Error - Fails to get vendors': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)


        return response_status

class DataCenterViewSet(viewsets.ModelViewSet):
    """

    """


    queryset = DataCenter.objects.all().select_related(
        'fk_vendor',
        'fk_common_address'
    ).prefetch_related('fk_common_address__related_city').order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': DataCenterRelationsSerializer,
        'update': DataCenterRelationsSerializer,
        'partial_update': DataCenterRelationsSerializer,

        'list': DataCenterSerializer,
        'retrieve': DataCenterSerializer,
        'destroy': DataCenterSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = DataCenterFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    #Create

    def create(self, request, *args, **kwargs):
        """
        Create a CommonAddress object.
        :return:
            A 201 HTTP Response indicating
            the Vendor Pricelist creation, otherwise
            an exception raise
        """
        # Serialize the information in request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_objs = self.custom_perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """Perform the save operations.
        Returns:
            A Price creation in database
        """
        return serializer.save()

    #Update

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def custom_perform_update(self, serializer):
        """Perform the save operations.

        Returns:
            A Price update in database
        """

        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)



class DuplicatedVendor(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):

        response_status = Response(status=status.HTTP_409_CONFLICT)

        try:
            vendor_catalog_duplicated = VendorCatalog.objects.get(slug=str(request.data['duplicated_vendor']))
            vendor_catalog_original = VendorCatalog.objects.get(slug=str(request.data['original_vendor']))

            #Update insatnces relacionadas a VendorCatalog, update Presences and Update Service Offered
            if (
                    update_instances_inverse(vendor_catalog_duplicated, vendor_catalog_original) and
                    update_presences(vendor_catalog_duplicated, vendor_catalog_original) and
                    update_service_offered(vendor_catalog_duplicated, vendor_catalog_original)):
                # Guardo cambios del vendorcatalog dupliate a inactivo
                try:
                    vendor_catalog_duplicated.status = "inactive"
                    vendor_catalog_duplicated.save()
                    response_status = Response(status=status.HTTP_200_OK)
                except Exception:
                    graylog_logger.error(
                        'Fails to save vendorcatalog duplicated  url'.format(str(traceback.format_exc())))
                    print("Fails to update vendors Catalogs ",traceback.format_exc())

                    response_status = Response({'Validation Error - Fails to update vendor to inactive': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_status = Response({'Validation Error': 'Error during execution'},
                                           status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            print(traceback.format_exc())
            response_status = Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

        return response_status


class InfeasibilityDetected(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):

        response_status = Response(status=status.HTTP_409_CONFLICT)
        if request.data['vendor'] != '' :
            try:
                # send_infeasibility_detected_async.delay(str(request.data['vendor']))
                response_status = Response(status=status.HTTP_200_OK)

            except Exception:
                print(traceback.format_exc())
                response_status = Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

        return response_status


class RecordVPLPrices(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):

        response_status = Response(status=status.HTTP_409_CONFLICT)
        if request.data['vpl_slug'] != '' :
            try:
                vpl = VendorPricelist.objects.get(slug=request.data['vpl_slug'])
                new_prices_screenshot = {
                    'registered_by_id': request.user.id,
                    'registered_date': datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
                    'prices': list(vpl.price_vendor_pricelist.all().values('fk_bw_down__bps_amount','fk_bw_up_id__bps_amount', 'nrc', 'mrc'))
                }

                if not vpl.previous_prices:
                    vpl.previous_prices = []
                vpl.previous_prices.append(new_prices_screenshot)
                vpl.save()

                response_status = Response(status=status.HTTP_200_OK)

            except Exception:
                print(traceback.format_exc())
                response_status = Response({'Validation Error': 'Bad request format'}, status=status.HTTP_400_BAD_REQUEST)

        return response_status


class CreateBulkPresencesAPIViewSet(APIView):
    """
    CreateBulkPresencesAPIViewSet
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        from api.core.utilities import generate_slugs

        if 'ids' in request.data and 'type' in request.data and 'vendor_slug' in request.data:
            try:
                if request.data['type'] == 'relevantsites':
                    generate_slugs('relevantsites')
                content_type = ContentType.objects.get(model=request.data['type'])
                vendor = VendorCatalog.objects.get(slug=request.data['vendor_slug'])
                ids = request.data['ids']

                # Elimino aquellos ids que ya estan asociados a este vendor, si hay alguno
                existing_presences = Presence.objects.filter(
                    content_type_id=content_type.id,
                    object_id__in=ids,
                    fk_vendor=vendor.id
                )
                if existing_presences.exists():
                    ids = [el for el in ids if int(el) not in list(existing_presences.values_list('object_id', flat=True))]

                # Elimino aquellos ids que no coinciden con ningun objeto existente
                objects = content_type.get_all_objects_for_this_type(id__in=ids)

                if objects.count() != len(ids):
                    ids = [el for el in ids if int(el) in list(objects.values_list('id', flat=True))]

                for obj_id in ids:
                    Presence.objects.create(
                        object_id = obj_id,
                        content_type_id = content_type.id,
                        fk_vendor_id = vendor.id
                    )
            except Exception:
                return HttpResponse(json.dumps({}), status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            return Response(status=status.HTTP_200_OK)

        return HttpResponse(json.dumps({}), status=status.HTTP_404_NOT_FOUND, content_type='application/json')


class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = TierSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_action_classes = {
        'list': TierSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
            :param queryset:
            :return: Set slug as pk VendorsContactsModel to return response
        """
        id = self.request.query_params.get("id", None)
        if id is None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(id=id)
        return queryset

#-----

#VCPMLog View

class VCPMLogViewSet(viewsets.ModelViewSet):
    """
    VCPMLog View Set
    """

    queryset = VCPMlog.objects.all().select_related(
        'fk_customer_quote',
        'fk_created_by',
        'fk_updated_by',
    ).order_by('-id')

    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_action_classes = {
        'create': VCPMlogRelationsSerializer,
        'update': VCPMlogRelationsSerializer,
        'partial_update': VCPMlogRelationsSerializer,

        'list': VCPMlogSerializer,
        'retrieve': VCPMlogSerializer,
        'destroy': VCPMlogSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    #filterset_class = VCPMlogFilter

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs['slug']
        try:
            obj = queryset.get(slug=slug)
        except VCPMlog.DoesNotExist:
            obj = None
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        """
        :param queryset:
        :return: Set slug as pk Vendor Pricelist model to return response
        """
        slug = self.request.query_params.get("slug", None)
        if slug == None:
            queryset = self.queryset
        else:
            queryset = self.queryset.get(slug=slug)
        return queryset

    def paginate_queryset(self, queryset):
        """
        :param queryset:
        :return: No paginated response if query_params contain 'all_elements' otherwise return Paginated Response
        """
        if 'all_elements' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    #Create

    def create(self, request, *args, **kwargs):
        """
        Create a VCPMLog object.
        :return:
            A 201 HTTP Response indicating
            the Vendor Pricelist creation, otherwise
            an exception raise
        """

        #print('request.data: ', request.data)

        input = {
            'index': [0],
            'columns': ['bps_amount',
                        'term',
                        'tech',
                        'latitude',
                        'longitude'],
            'data': [[request.data['bps_amount'],
                      request.data['term'],
                      request.data['technology'],
                      request.data['lat'],
                      request.data['lon']]]
        }

        #Hacer la llamada al VCPM y armar la data a serializar
        response = get_vendor_cost_predictor_model(input, request.data['country']['id'])

        input_serializer = {
            'mrc': response['mrc'][0],
            'model': response['modelo'],
            'model_version': response['version'],
            'technology': request.data['technology'],
            'customer_quote': request.data['cq_id']
        }

        try:
            serializer = self.get_serializer(data=input_serializer)
            serializer.is_valid(raise_exception=True)
        except Exception:
            print(traceback.format_exc())

        # If serializer is valid, then save the object
        try:
            created_objs = self.custom_perform_create(serializer)
        except Exception:
            created_objs = []
            print(traceback.format_exc())

        headers = self.get_success_headers(serializer.data)

        #print('serializer.data: ', serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def custom_perform_create(self, serializer):
        """
        Perform the save operations.
        Returns:
            A VCPMLog creation in database
        """
        try:
            return serializer.save(fk_created_by=self.request.user,
                                   created_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    #Update

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.update(request, *args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            return []

    def custom_perform_update(self, serializer):
        """
        Perform the save operations.
        Returns:
            A VCPMLog update in database
        """
        try:
            return serializer.save(fk_updated_by=self.request.user,
                                   updated_at=datetime.now(tz=timezone.utc))
        except Exception:
            print(traceback.format_exc())
            return []

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            created_objs = self.custom_perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Validation Error': 'Bad request format'},
                            status=status.HTTP_400_BAD_REQUEST)

#-----

