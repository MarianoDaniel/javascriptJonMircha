"""General API Serializers

This file has the objects serializations
for later use in api views.
"""
from django.db.models import Q
from django.core.exceptions import ValidationError
import pytz
import traceback

from api.procurement.utilities import get_tax_for_data_geolocal
from api.tools_script import coord_isvalid
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from mysite.models import ExchangeRate

from api.custom_fields import (
    ContentObjectRelatedField
)

from api.price_log_hit.serializers import (
    PriceLogHitReadSerializer,
)

from Logistics.models import (
    Service,
    Equipment,
    License,
    VendorQuote,
    CrossConnect
)

from IGIQ2.models import (
    UserQuotes,
    UserIG,
    CustomerQuoteVendor,
    VQtoCQIrrelevanceRelation)

from mysite.models import (
    Bandwidth,
    City,
    CommonAddress,
    Country,
    Currency,
    EndCustomer,
    ServiceType,
    Task,
    Project,
    Event,
    Notification,
    Company,
    OfficialCity,
    County,
    State,
    OfficialCountry,
    VendorPOP
)

from Procurement.models import (
    Contact,
    VendorCatalog,
    VendorQuotes,
    TECH_Z_LOC,
    TECH_A_LOC
)

from IGIQ2.models import (
    UserQuotes,
    UserProjects
)

from PriceList.models import (
    PriceLogHit,
)


class DateTimeFieldOverridden(serializers.DateTimeField):
    def to_representation(self, value):
        local_tz = pytz.timezone('UTC')
        value = local_tz.localize(value)
        return super(DateTimeFieldOverridden, self).to_representation(value)


class EquipmentSerializer(serializers.ModelSerializer):
    """
        EquipmentSerializer for serialize a Equipment object
    """

    class Meta:
        model = Equipment
        fields = (
            'id',
            'name'
        )


class LicenseSerializer(serializers.ModelSerializer):
    """
        LicenseSerializer for serialize a License object
    """

    class Meta:
        model = License
        fields = (
            'id',
            'quickbase_id',
            'name'
        )


class LogVendorQuoteSerializer(serializers.ModelSerializer):
    """
    LogVendorQuoteSerializer for serialize a Logistic VendorQuote object
    """

    class Meta:
        model = VendorQuote
        fields = (
            'id',
            'vquickbase_id'
        )


class CrossConnectMinSerializer(serializers.ModelSerializer):
    """
    CrossConnectSerializer for serialize a CrossConnect object
    """

    class Meta:
        model = CrossConnect
        fields = (
            'id',
            'quickbase_id'
        )


class VendorCatalogMinSerializer(serializers.ModelSerializer):
    tier = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
        source='fk_tier'
     )
    class Meta:
        model = VendorCatalog
        fields = (
            'name',
            'slug',
            'tier'
        )


class CompanyMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'id'
        )


class CrossConnectSerializer(serializers.ModelSerializer):
    """
    CrossConnectSerializer for serialize a CrossConnect object
    """

    connecting_vendor = VendorCatalogMinSerializer(read_only=True, source='fk_connecting_vendor')
    connecting_company = CompanyMinSerializer(read_only=True, source='fk_connecting_company')
    contracted_vendor = VendorCatalogMinSerializer(read_only=True, source='fk_contracted_vendor')
    pop = serializers.SerializerMethodField()

    class Meta:
        model = CrossConnect
        fields = (
            'slug',
            'quickbase_id',
            'status',
            'purpose',
            'role',
            'type',
            'connecting_vendor',
            'connecting_company',
            'contracted_vendor',
            'work_order',
            'circuit_id',
            'activation_date',
            'disconnect_work_order',
            'disconnection_date',
            'stop_bill_date',
            'pop'  # a través de la relación con Network Links)
        )

    def get_pop(self, instance):

        try:
            try:
                return {
                    'pop_id': instance.elated_xc_ext1_crossconnect.first().related_pop_ext1.pop_id,
                    'quickbase_id': instance.elated_xc_ext1_crossconnect.first().related_pop_ext1.pop_quickbase_id
                }
            except Exception:
                return {
                    'pop_id': instance.related_xc_ext2_crossconnect.first().related_pop_ext2.pop_id,
                    'quickbase_id': instance.elated_xc_ext2_crossconnect.first().related_pop_ext2.pop_quickbase_id
                }
        except Exception:
            return None


            # def to_representation(self, value):
            #     from PriceList.models import NetworkLink
            #     pop = None
            #     net = NetworkLink.objects.get(Q(related_xc_ext2__id= value.id) | Q( related_xc_ext1 = value.id) )
            #     if net.related_xc_ext1 != None:
            #         pop = net.related_pop_ext1
            #     elif net.related_xc_ext2 != None:
            #         pop = net.related_pop_ext2
            #     value.pop = pop
            #     return super(CrossConnectSerializer, self).to_representation(value)


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer

    ModelSerializer for serialize a User object
    """
    # avatar_url = serializers.SerializerMethodField()
    main_group = serializers.ReadOnlyField(source='userig.main_group.name')
    unread_notifications = serializers.ReadOnlyField(source='userig.unread_notifications_count')
    avatar_url = serializers.ImageField(source='userig.avatar')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'avatar_url', 'main_group', 'is_active', 'unread_notifications')

    """def get_avatar_url(self, obj):
        try:
            if obj.userig.avatar:
                avatar_url = obj.userig.avatar.url
            else:
                avatar_url = ''
        except (UserIG.DoesNotExist, AttributeError):
            avatar_url = ''
        return avatar_url
    """


class UserSerializerMin(serializers.ModelSerializer):
    """UserSerializerMin

    ModelSerializer for serialize a User object
    """
    user = serializers.IntegerField(source='id')
    # avatar_url = serializers.SerializerMethodField()
    avatar_url = serializers.ImageField(source='userig.avatar')

    class Meta:
        model = User
        fields = ('user', 'first_name', 'last_name', 'avatar_url', 'username')

    """def get_avatar_url(self, obj):
        try:
            if obj.userig.avatar:
                avatar_url = obj.userig.avatar.url
            else:
                avatar_url = ''
        except UserIG.DoesNotExist:
            avatar_url = ''
        return avatar_url
    """


class GroupSerializer(serializers.ModelSerializer):
    """UserSerializer

    ModelSerializer for serialize a User object
    """

    class Meta:
        model = Group
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    """TaskSerializer

    ModelSerializer for serialize a Task object
    """

    class Meta:
        model = ContentType
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    """ServiceTypeSerializer

    ModelSerializer for serialize a ServiceType object
    """

    class Meta:
        model = ServiceType
        fields = ('label', 'code', 'id', 'upper_limit_usd', 'lower_limit_usd', 'quickbase_id')


class BandwidthSerializer(serializers.ModelSerializer):
    """BandwidthSerializer

    ModelSerializer for serialize a Bandwidth object
    """
    name = serializers.CharField(source='label')
    bw = serializers.IntegerField(source='id')
    service = serializers.IntegerField(source='related_service_id')

    class Meta:
        model = Bandwidth
        fields = ('name', 'bps_amount', 'bw', 'service')


class BandwidthSerializerMin(serializers.ModelSerializer):
    bw = serializers.IntegerField(source='id')

    class Meta:
        model = Bandwidth
        fields = ('bw', 'label', 'bps_amount')


class CurrencySerializerMin(serializers.ModelSerializer):
    """CurrencySerializer

    ModelSerializer for serialize a Currency object
    """

    class Meta:
        model = Currency
        fields = ('code', 'name')


class CurrencySerializer(serializers.ModelSerializer):
    """CurrencySerializer

    ModelSerializer for serialize a Currency object
    """

    class Meta:
        model = Currency
        fields = ('code', 'name', 'fixed_exchange_rate', 'rate_fixed_date')


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    """CurrencySerializer

    ModelSerializer for serialize a Currency object
    """
    exchange_rate = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ('code', 'name', 'exchange_rate')

    def get_exchange_rate(self, obj):
        try:
            exchange_rate = ExchangeRate.objects.filter(related_currency_code=obj).order_by(
                '-date').first().exchange_rate
        except Exception:
            exchange_rate = None
            pass
        return exchange_rate


class CountrySerializer(serializers.ModelSerializer):
    """CountrySerializer

    ModelSerializer for serialize a Country object
    """
    currencies = CurrencySerializer(source="currency_country", read_only=True, many=True)

    class Meta:
        model = Country
        fields = ('id', 'name', 'currencies')


class CitySerializer(serializers.ModelSerializer):
    """CitySerializerMin

    ModelSerializer for serialize a City object
    """
    related_country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'state', 'related_country')


class CitySerializerMin(serializers.ModelSerializer):
    """CitySerializerMin

    ModelSerializer for serialize a City object
    """

    class Meta:
        model = City
        fields = ('id', 'name', 'state')


class CommonAddressSerializer(serializers.ModelSerializer):
    """CommonAddressSerializer

    ModelSerializer for serialize a CommonAddress object
    """

    related_city = CitySerializerMin(read_only=True)
    related_country = CountrySerializer(read_only=True)

    class Meta:
        model = CommonAddress
        fields = ('id', 'address', 'related_city', 'related_country', 'latitude', 'longitude','quickbase_id')


class CommonAddressWriteSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='related_city')
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), source='related_country')

    class Meta:
        model = CommonAddress
        fields = (
        'id', 'address', 'quickbase_id', 'city', 'country', 'latitude', 'longitude', 'zipcode', 'location_point')

    def to_internal_value(self, data):
        if 'city' in data and data['city']:
            try:
                data['city'] = data['city']['id'] if 'id' in data['city'] else None
            except (City.DoesNotExist, KeyError, TypeError):
                data['city'] = None
        if 'country' in data and data['country']:
            try:
                data['country'] = data['country']['id'] if 'id' in data['country'] else None
            except (Country.DoesNotExist, KeyError, TypeError):
                data['country'] = None
        if 'latitude' in data and 'longitude' in data and data['latitude'] and data['longitude']:
            if coord_isvalid(data['latitude'], data['longitude']):
                try:
                    data['location_point'] = 'POINT (' + str(data['longitude']) + ' ' + str(data['latitude']) + ')'
                except (ValueError, KeyError, TypeError):
                    raise serializers.ValidationError({'Coordinates': 'Error representation to point gis'})
            else:
                raise serializers.ValidationError({'Coordinates': 'are not valid'})

        return super(CommonAddressWriteSerializer, self).to_internal_value(data)


class EndCustomerSerializer(serializers.ModelSerializer):
    """EndCustomerSerializer

    ModelSerializer for serialize a EndCustomer object
    """

    class Meta:
        model = EndCustomer
        fields = '__all__'


class TaskListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        task_mapping = {task.slug: task for task in instance}
        data_mapping = {item['slug']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for task_id, data in data_mapping.items():
            task = task_mapping.get(task_id, None)
            if task is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(task, data))

        # Perform deletions.
        for task_id, task in task_mapping.items():
            if task_id not in data_mapping:
                task.delete()
        return ret

    def to_internal_value(self, data):
        """

        :param data:
        :return: data normalized
        """

        ret = []
        errors = []

        for item in data:
            try:
                # Code that was inserted
                self.child.instance = self.instance.get(slug=item['slug']) if self.instance else None
                self.child.initial_data = item
                # Until here
                validated = self.child.run_validation(item)
            except ValidationError as exec:
                errors.append(exec.message)

            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise errors

        return ret


class TaskSerializer(serializers.ModelSerializer):
    """TaskSerializer

    ModelSerializer for serialize a Task object
    """
    related_data = serializers.IntegerField(source='object_id', required=True)
    department = serializers.PrimaryKeyRelatedField(required=True, queryset=Group.objects.all())
    stat = serializers.CharField(source='status', required=True)
    preference = serializers.CharField(source='priority', required=True)
    type = serializers.CharField(source='type_of_aim', max_length=25, required=True)
    user_assignee_min = UserSerializerMin(source='assignee', read_only=True)
    user_assignee = serializers.PrimaryKeyRelatedField(source='assignee', write_only=True, queryset=User.objects.all())
    escalated = serializers.BooleanField(source='is_escalated', required=True)
    related_content = ContentObjectRelatedField(source='content_object', read_only=True)
    has_comments = serializers.SerializerMethodField(read_only=True)
    start = serializers.DateTimeField(source='start_date', required=False)
    end = serializers.DateTimeField(source='end_date', required=False)
    deadline = serializers.DateTimeField(source='due_date', required=False)
    created_date = serializers.DateTimeField(source='created_at', read_only=False, required=False)
    updated_at = serializers.DateTimeField(read_only=False, required=False)
    updated_by = serializers.IntegerField(required=False, source='updated_by_id', read_only=False)
    automated = serializers.BooleanField(required=False, source='flag_automated_closure')
    content_model = serializers.SlugRelatedField(source='content_type', required=True,
                                                 queryset=ContentType.objects.all(), slug_field='model')

    class Meta:
        list_serializer_class = TaskListSerializer
        model = Task
        fields = ('related_data', 'stat', 'preference', 'user_assignee',
                  'user_assignee_min', 'department', 'type', 'department', 'escalated',
                  'has_comments', 'related_content', 'start', 'end', 'content_model',
                  'deadline', 'created_date', 'automated',
                  'slug', 'updated_at', 'updated_by', 'details')

    def get_has_comments(self, obj):
        return obj.comments.filter(type='comment').exists()

    def to_internal_value(self, data):
        if 'stat' in data:
            try:
                data['stat'] = data['stat']
            except KeyError:
                raise serializers.ValidationError({'Status': 'Status is required'})
        if 'start' in data:
            try:
                data['start'] = data['start']
            except KeyError:
                raise serializers.ValidationError({'Status': 'date_start is required'})
        if 'end' in data:
            try:
                data['end'] = data['end']
            except KeyError:
                raise serializers.ValidationError({'Status': 'date_end is required'})
        return super(TaskSerializer, self).to_internal_value(data)


class TaskMapSerializer(serializers.ModelSerializer):
    """TaskSerializer

    ModelSerializer for serialize a Task object
    """
    # object_id = serializers.IntegerField()
    status = serializers.CharField()
    latitude = serializers.CharField(source='content_object.latitude')
    longitude = serializers.CharField(source='content_object.longitude')
    # related_data = serializers.IntegerField(source='content_object.id')
    escalated = serializers.BooleanField(source='is_escalated')
    preference = serializers.CharField(source='priority')
    assignee = serializers.IntegerField(source='assignee_id')
    task = serializers.SlugField(source='slug', read_only=True)

    class Meta:
        model = Task
        fields = ('task', 'status', 'latitude', 'longitude', 'preference', 'escalated', 'assignee')


class TaskWithVendorsSerializer(serializers.ModelSerializer):
    """TaskWithVendorsSerializer

    ModelSerializer for serialize result from process tasks, quotes and suggested vendors

    """
    user_assignee = UserSerializer(source='assignee', read_only=True)
    related_content = ContentObjectRelatedField(source='content_object', read_only=True)
    has_comments = serializers.SerializerMethodField()
    task = serializers.IntegerField(source='id')
    type = serializers.CharField(source='type_of_aim', max_length=25)
    related_data = serializers.IntegerField(source='object_id')
    start = serializers.DateTimeField(source='start_date')
    end = serializers.DateTimeField(source='end_date')
    deadline = serializers.DateTimeField(source='due_date')
    escalated = serializers.BooleanField(source='is_escalated')
    stat = serializers.CharField(source='status')
    preference = serializers.CharField(source='priority')
    content_type = serializers.SlugRelatedField(read_only=True, slug_field='model')

    class Meta:
        model = Task
        fields = ('task', 'related_data', 'type', 'user_assignee',
                  'has_comments', 'related_content',
                  'start', 'end', 'content_type',
                  'deadline', 'stat', 'preference',
                  'escalated')

    def get_has_comments(self, obj):
        return obj.comments.filter(type='comment').exists()


class CustomerQuoteVendorListSerializer(serializers.ListSerializer):
    """CustomerQuoteVendorListSerializer

       ModelListSerializer for serialize a CustomerQuoteVendor List objects
    """

    def update(self, instance, validated_data):
        ideses = instance.values('id')

        # Unifico los id's a actualizar con su respectivo valor.
        for i, elem in enumerate(validated_data):
            elem.update(ideses[i])

        cqvendor_mapping = {customerqvendor.id: customerqvendor for customerqvendor in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for cq_id, data in data_mapping.items():
            cq = cqvendor_mapping.get(cq_id, None)
            if cq is None:
                pass
            else:
                ret.append(self.child.update(cq, data))

        return ret

    def to_internal_value(self, data):
        """

        :param data:
        :return: data normalized
        """
        ret = []
        errors = []
        for item in data:
            try:
                # Code that was inserted
                self.child.instance = self.instance.get(quote_id=item['customer_quote'],
                                                        vendor__slug=item['vendor_quoted']) if self.instance else None
                self.child.initial_data = item
                # Until here
                validated = self.child.run_validation(item)
            except ValidationError as ex:
                errors.append(ex.message)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise errors
        return ret


class CustomerQuoteVendorSerializer(serializers.ModelSerializer):
    """CustomerQuoteVendorSerializer

        ModelSerializer for serialize a CustomerQuoteVendor object
    """

    from api.procurement.serializers import (
        VendorCatalogMinSerializer
    )

    vendor = VendorCatalogMinSerializer(read_only=True)
    customer_quote = serializers.PrimaryKeyRelatedField(read_only=True, source='quote')

    class Meta:
        model = CustomerQuoteVendor
        list_serializer_class = CustomerQuoteVendorListSerializer
        fields = ('customer_quote', 'vendor', 'type', 'location', 'purpose', 'radio', 'rating')


class CustomerQuoteVendorSerializerRelation(serializers.ModelSerializer):
    """CustomerQuoteVendorSerializer

        ModelSerializer for serialize a CustomerQuoteVendor object
    """

    customer_quote = serializers.PrimaryKeyRelatedField(read_only=True, source='quote')
    vendor_quoted = serializers.PrimaryKeyRelatedField(read_only=True, source='vendor')

    class Meta:
        model = CustomerQuoteVendor
        list_serializer_class = CustomerQuoteVendorListSerializer
        fields = ('customer_quote', 'vendor_quoted')


class ServiceSerializerMin(serializers.ModelSerializer):
    related_requested_bw_down = serializers.SlugRelatedField(read_only=True, slug_field='label')
    related_requested_bw_up = serializers.SlugRelatedField(read_only=True, slug_field='label')
    related_service_type = serializers.SlugRelatedField(read_only=True, slug_field='label')
    related_customer = serializers.SlugRelatedField(read_only=True, slug_field='name')
    related_city = serializers.SlugRelatedField(read_only=True, slug_field='name')
    related_customer_quote = serializers.SlugRelatedField(read_only=True, slug_field='cq_id')
    related_country = serializers.SlugRelatedField(read_only=True, slug_field='name',
                                                   source='related_city.related_country')

    class Meta:
        model = Service
        fields = (
            'service_id',
            'status',
            'related_city',
            'related_country',
            'related_customer',
            'latitude',
            'longitude',
            'related_requested_bw_down',
            'related_requested_bw_up',
            'related_service_type',
            'related_customer_quote'
        )


class OpportunitySerializer(serializers.ModelSerializer):
    from api.pricing.serializers import (
        CompanySerializerMin
    )

    opp_name = serializers.CharField(source='project_name')
    related_customer = CompanySerializerMin(read_only=True)
    user_assignee = UserSerializer(source='assignee', read_only=True, many=True)
    user_source = UserSerializer(source='source_user', read_only=True)

    class Meta:
        model = UserProjects
        fields = (
            'project_id',
            'opp_name',
            'related_customer',
            'user_assignee',
            'description',
            'source',
            'user_source',
            'hot',
        )


class UserQuoteSerializer(serializers.ModelSerializer):
    """UserQuoteSerializer

    ModelSerializer for serialize a UserQuote object
    """

    from api.procurement.serializers import (
        VCPMlogSerializerMin
    )

    related_bw_down = BandwidthSerializerMin(read_only=True)
    related_bw_up = BandwidthSerializerMin(read_only=True)
    related_service_type = ServiceTypeSerializer(read_only=True)
    related_currency = CurrencySerializer(read_only=True)
    related_a_address = CommonAddressSerializer(read_only=True)
    related_city = CitySerializerMin(read_only=True)
    related_country = CountrySerializer(read_only=True)
    project = OpportunitySerializer(read_only=True)
    related_endcustomer = EndCustomerSerializer(read_only=True)
    local_billing = serializers.BooleanField(read_only=True)
    taxes = serializers.CharField(read_only=True)
    polygon_hit = serializers.BooleanField(read_only=True)
    category_hit = serializers.BooleanField(read_only=True)
    bw_hit = serializers.BooleanField(read_only=True)
    related_hit = serializers.PrimaryKeyRelatedField(read_only=True)
    #Se debe utilizar el related name para esta relacion
    related_vcpmlog = VCPMlogSerializerMin(source='vcpmlog_customer_quote',
                                           many=True,
                                           read_only=True)
    providers = CustomerQuoteVendorSerializer(source='quotevendor_quote', many=True, read_only=True)

    class Meta:
        model = UserQuotes
        fields = ('term', 'z_address', 'latitude', 'longitude',
                  'comments', 'nrc', 'mrc', 'tech_details', 'last_vendors_suggestion_load_at',
                  'created_by', 'last_updated_by', 'last_updated_at',
                  'cq_id', 'project', 'status', 'due_date', 'geocode_result',
                  'location_comments', 'taxes', 'date_created',
                  'date_requested', 'date_quoted', 'related_bw_down',
                  'related_bw_up', 'related_service_type', 'related_currency',
                  'related_a_address', 'related_city', 'related_country',
                  'related_endcustomer', 'quotability_index', 'local_billing', 'taxes', 'polygon_hit', 'bw_hit',
                  'category_hit', 'related_hit', 'related_vcpmlog', 'providers','handoff_hit')


class UserQuoteSerializerMin(serializers.ModelSerializer):
    """UserQuoteSerializerMin

    ModelSerializer for serialize a UserQuote object with
    summarize information
    """

    related_bw_down = BandwidthSerializerMin(read_only=True)
    related_bw_up = BandwidthSerializerMin(read_only=True)
    related_service_type = ServiceTypeSerializer(read_only=True)
    related_currency = serializers.SlugRelatedField(read_only=True, slug_field='code')
    related_a_address = CommonAddressSerializer(read_only=True)
    related_city = CitySerializerMin(read_only=True)
    related_country = CountrySerializer(read_only=True)
    related_endcustomer = serializers.SlugRelatedField(read_only=True, slug_field='name')
    project = OpportunitySerializer(read_only=True)
    providers = CustomerQuoteVendorSerializer(source='quotevendor_quote', many=True)
    service_id = serializers.SerializerMethodField()
    local_billing = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = UserQuotes
        fields = ('term', 'z_address', 'latitude', 'longitude',
                  'comments', 'nrc', 'mrc', 'tech_details',
                  'cq_id', 'project', 'status', 'due_date',
                  'location_comments', 'taxes', 'date_quoted',
                  'related_bw_down', 'related_bw_up',
                  'related_service_type', 'related_endcustomer',
                  'related_currency', 'related_city', 'last_vendors_suggestion_load_at',
                  'related_country', 'related_a_address', 'type',
                  'geocode_result', 'is_escalated', 'service_id', 'providers', 'local_billing', 'zipcode')

    def get_service_id(self, obj):
        return obj.related_service.first().service_id if obj.related_service.exists() else None


class UserQuoteSerializerPatch(serializers.ModelSerializer):
    """UserQuoteSerializer

    ModelSerializer for serialize a UserQuote object
    """
    related_bw_down = BandwidthSerializerMin(read_only=True)
    related_bw_up = BandwidthSerializerMin(read_only=True)
    related_service_type = ServiceTypeSerializer(read_only=True)
    related_a_address = CommonAddressSerializer(read_only=True)
    related_city = CitySerializerMin(read_only=True)
    related_country = CountrySerializer(read_only=True)
    project = OpportunitySerializer(read_only=True)
    related_endcustomer = EndCustomerSerializer(read_only=True)
    currency = serializers.SlugRelatedField(allow_null=True, source='related_currency', slug_field='code',
                                            required=False, queryset=Currency.objects.all(), write_only=True)
    related_priceloghit = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, write_only=True,
                                                     queryset=PriceLogHit.objects.all(), source='related_hit')

    class Meta:
        model = UserQuotes
        fields = ('term', 'z_address', 'latitude', 'longitude',
                  'comments', 'nrc', 'mrc', 'tech_details', 'last_vendors_suggestion_load_at',
                  'created_by', 'last_updated_by', 'last_updated_at',
                  'cq_id', 'project', 'status', 'due_date', 'geocode_result',
                  'location_comments', 'taxes', 'date_created',
                  'date_requested', 'date_quoted', 'related_bw_down',
                  'related_bw_up', 'related_service_type', 'currency',
                  'related_a_address', 'related_city', 'related_country',
                  'related_endcustomer', 'local_billing', 'currency', 'related_priceloghit')

        read_only_fields = ('term', 'z_address', 'latitude', 'longitude',
                            'comments', 'tech_details', 'last_vendors_suggestion_load_at',
                            'created_by', 'last_updated_by', 'last_updated_at',
                            'cq_id', 'project', 'due_date', 'geocode_result',
                            'location_comments', 'date_created',
                            'date_requested', 'related_bw_down',
                            'related_bw_up', 'related_service_type',
                            'related_a_address', 'related_city', 'related_country',
                            'related_endcustomer')

        extra_kwargs = {
            'nrc': {'write_only': True},
            'mrc': {'write_only': True},
            'status': {'write_only': True},
            'local_billing': {'write_only': True},
            'date_quoted': {'write_only': True},
            'taxes': {'write_only': True},
            'currency': {'write_only': True},
        }


class VendorQuoteListSerializer(serializers.ListSerializer):
    """VendorQuoteSerializer

    ModelSerializer for serialize a VendorQuote object
    """

    def create(self, validated_data):
        objects = []
        for data in validated_data:
            data['tax_nrc_percentage'], data['tax_mrc_percentage'] = get_tax_for_data_geolocal(
                data['latitude'] if data['latitude'] else None,
                data['longitude'] if data['longitude'] else None,
                data['vendor'].slug if data['vendor'] else None)
            objects.append(self.child.create(data))
        return objects

    def update(self, instance, validated_data):

        vq_mapping = {vq.slug: vq for vq in instance}
        data_mapping = {item['slug']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for vq_id, data in data_mapping.items():
            vq = vq_mapping.get(vq_id, None)
            ret.append(self.child.update(vq, data))

        # Perform deletions.
        for vq_id, vq in vq_mapping.items():
            if vq_id not in data_mapping:
                vq.delete()

        return ret

    def to_internal_value(self, data):
        """

        :param data:
        :return: data normalized
        """

        ret = []
        errors = []

        for item in data:
            try:
                # Code that was inserted
                self.child.instance = self.instance.get(slug=item['slug']) if self.instance else None
                self.child.initial_data = item
                # Until here
                validated = self.child.run_validation(item)
            except ValidationError as ex:
                errors.append(ex.message)

            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise errors

        return ret


class TaskSerializerMin(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'status', 'type_of_aim'
        )


class VendorQuoteSerializer(serializers.ModelSerializer):
    """VendorQuoteSerializer

    ModelSerializer for serialize a VendorQuote object
    """

    from api.procurement.serializers import (
        VendorCatalogMinSerializer
    )

    vendor_catalog = VendorCatalogMinSerializer(source='vendor', read_only=True)
    bw_down = BandwidthSerializerMin(source='related_bw_down', read_only=True)
    bw_up = BandwidthSerializerMin(source='related_bw_up', read_only=True)
    service_type = ServiceTypeSerializer(read_only=True, source='related_service_type')
    tech_a_loc = serializers.MultipleChoiceField(choices=TECH_A_LOC, source='tech_aloc', required=False,
                                                 allow_blank=True, allow_null=True)
    tech_z_loc = serializers.MultipleChoiceField(choices=TECH_Z_LOC, source='tech_zloc', required=False,
                                                 allow_blank=True, allow_null=True)
    currency = CurrencySerializerMin(source='related_currency', read_only=True)
    city = CitySerializerMin(read_only=True, source='related_city')
    country = CountrySerializer(read_only=True, source='related_country')
    a_address = CommonAddressSerializer(read_only=True, source='related_a_address')
    zip_code = serializers.CharField(source='zipcode', required=False, allow_blank=True, allow_null=True)
    created_by = UserSerializerMin(read_only=True)
    last_updated_by = UserSerializerMin(required=False, read_only=True)
    date_created = serializers.DateTimeField(read_only=True)
    task = TaskSerializer(read_only=True, source='fk_task')
    date_status = serializers.DateField(read_only=True, source='status_date')
    exchange_rate = serializers.FloatField(required=False, allow_null=True)
    costs_t_i = serializers.BooleanField(read_only=True, source='costs_taxes_included')

    class Meta:
        model = VendorQuotes
        list_serializer_class = VendorQuoteListSerializer
        fields = ('status', 'service_type', 'vendor_catalog', 'bw_down', 'bw_up', 'tax_nrc_percentage',
                  'tax_mrc_percentage', 'tax_nrc', 'exchange_rate', 'lead_time',
                  'tax_mrc', 'date_status', 'solution', 'ip', 'email_outreach',
                  'tech_z_loc', 'tech_a_loc', 'comments', 'tech_details', 'zip_code',
                  'date_created', 'is_from_vendor_pricelist',
                  'type_of_coverage', 'term', 'currency', 'nrc', 'mrc', 'last_updated_at',
                  'city', 'country', 'a_address', 'z_address', 'date_created', 'last_updated_at',
                  'latitude', 'longitude', 'created_by', 'last_updated_by', 'task', 'slug', 'quickbase_id',
                  'exchange_rate', 'costs_t_i'
                  )


class VendorQuoteRelationsSerializer(serializers.ModelSerializer):
    """VendorQuoteSerializer

    ModelSerializer for serialize a VendorQuote object
    """
    vendor = serializers.SlugRelatedField(slug_field='slug', queryset=VendorCatalog.objects.all())
    bw_down = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_bw_down',
                                                 queryset=Bandwidth.objects.all())
    bw_up = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, source='related_bw_up',
                                               queryset=Bandwidth.objects.all())
    service_type = serializers.PrimaryKeyRelatedField(source='related_service_type', queryset=ServiceType.objects.all())
    currency = serializers.SlugRelatedField(allow_null=True, source='related_currency', slug_field='code',
                                            required=False, queryset=Currency.objects.all())
    city = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_city', required=False,
                                              queryset=City.objects.all())
    country = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_country', required=False,
                                                 queryset=Country.objects.all())
    a_address = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_a_address', required=False,
                                                   queryset=CommonAddress.objects.all())
    zip_code = serializers.CharField(source='zipcode', required=False, allow_null=True, allow_blank=True)
    created_by = UserSerializerMin(read_only=True)
    tech_a_loc = serializers.MultipleChoiceField(choices=TECH_A_LOC, source='tech_aloc', required=False,
                                                 allow_blank=True, allow_null=True)
    tech_z_loc = serializers.MultipleChoiceField(choices=TECH_Z_LOC, source='tech_zloc', required=False,
                                                 allow_blank=True, allow_null=True)
    last_updated_by = UserSerializerMin(required=False, read_only=True)
    date_created = serializers.DateTimeField(read_only=True)
    task = serializers.SlugRelatedField(allow_null=True, required=False, source='fk_task', slug_field='slug',
                                        queryset=Task.objects.all())
    comments = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    date_status = serializers.DateField(source='status_date', allow_null=True, required=False)
    exchange_rate = serializers.FloatField(required=False, allow_null=True)
    costs_t_i = serializers.BooleanField(write_only=True, default=False, source='costs_taxes_included')

    class Meta:
        model = VendorQuotes
        list_serializer_class = VendorQuoteListSerializer
        fields = ('service_type', 'vendor', 'bw_down', 'bw_up', 'type_of_coverage', 'currency',
                  'city', 'country', 'a_address', 'last_updated_by', 'date_created', 'created_by',
                  'slug', 'last_updated_at', 'term', 'z_address', 'zip_code', 'latitude', 'longitude',
                  'comments', 'nrc', 'mrc', 'status', 'tax_nrc_percentage', 'tax_mrc_percentage',
                  'tax_nrc', 'tax_mrc', 'exchange_rate', 'date_status', 'lead_time', 'solution', 'email_outreach',
                  'quickbase_id', 'tech_a_loc', 'tech_z_loc', 'type_of_coverage', 'last_updated_at', 'task',
                  'location_point', 'email_outreach', 'ip', 'tech_details', 'is_from_vendor_pricelist',
                  'exchange_rate', 'costs_t_i'
                  )

    def to_internal_value(self, data):
        """
        :param data: body json from request
        :return: data json parsed for internal representation
        """
        # IZO-A, IZO-B, Dark Fiber, IPVPN, Ethernet, Clear Channel / IPLC
        SERVICES_NEED_A_ADDRESS = [5, 8, 15, 18, 28, 41]
        vendor = None
        if 'vendor' in data and data['vendor']:
            try:
                data['vendor'] = data['vendor']['slug']
                vendor = VendorCatalog.objects.get(slug=data['vendor'])
            except (KeyError, ValueError):
                raise serializers.ValidationError({'vendor': 'Vendor Missing slug key'})

        if 'task' in data:
            try:
                data['task'] = data['task']['slug']
            except (KeyError, ValueError, TypeError):
                data['task'] = None

        if 'service_type' in data and data['service_type']:
            try:
                data['service_type'] = data['service_type'].get('id', '')
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Service Type': 'Vendor Missing id key'})
        if 'bw_down' in data and data['bw_down']:
            try:
                data['bw_down'] = data['bw_down']['id'] if 'id' in data['bw_down'] else None

            except (KeyError, ValueError, TypeError, AttributeError):
                data['bw_down'] = None
                raise serializers.ValidationError({'Bandwidth down': 'Bandwidth Missing id key'})
        if 'bw_up' in data and data['bw_up']:
            try:
                data['bw_up'] = data['bw_up']['id']
            except (KeyError, ValueError):
                data['bw_up'] = None

        if 'currency' in data and data['currency']:
            try:
                data['currency'] = str(data['currency']['code'])
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Currency': 'currency Missing code key'})

        if not 'currency' in data or not data['currency']:
            try:
                data['currency'] = 'BRL' if vendor.country.name.lower() in ['brasil', 'brazil'] else 'USD'
            except (AttributeError, KeyError, TypeError, KeyError):
                data['currency'] = 'USD'

        if 'city' in data and data['city']:
            try:
                data['city'] = data['city']['id']
            except (KeyError, ValueError):
                raise serializers.ValidationError({'City': 'city Missing id key'})
        if 'country' in data and data['country']:
            try:
                data['country'] = data['country']['id']
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Country': 'country Missing id key'})
        if 'a_address' in data and data['a_address'] is not None:
            if data['service_type'] in SERVICES_NEED_A_ADDRESS:
                try:
                    data['a_address'] = data['a_address']['id']
                except (KeyError, ValueError):
                    raise serializers.ValidationError({'A address': 'a address Missing id key'})
            else:
                data['a_address'] = ''

        if 'latitude' in data and 'longitude' in data and data['latitude'] and data['longitude']:
            if coord_isvalid(data['latitude'], data['longitude']):
                try:
                    data['location_point'] = 'POINT (' + str(data['longitude']) + ' ' + str(data['latitude']) + ')'
                except (ValueError, KeyError, TypeError):
                    raise serializers.ValidationError({'Coordinates': 'Error representation to point gis'})
            else:
                raise serializers.ValidationError({'Coordinates': 'are not valid'})
        if 'tech_a_loc' in data and data['tech_a_loc']:
            try:
                for item in data['tech_a_loc']:
                    if item not in dict(TECH_A_LOC):
                        raise serializers.ValidationError(
                            {'Tech A Loc': '%s, not in %s' % (item, list((dict(TECH_A_LOC)).keys()))})
            except (ValueError, KeyError, TypeError):
                raise serializers.ValidationError({'Tech A Loc': 'Key validation error'})
        if 'tech_zloc' in data and data['tech_zloc']:
            try:
                for item in data['tech_zloc']:
                    if item not in dict(TECH_Z_LOC):
                        raise serializers.ValidationError(
                            {'Tech Z Loc': '%s, not in %s' % (item, list((dict(TECH_Z_LOC)).keys()))})
            except (ValueError, KeyError, TypeError):
                raise serializers.ValidationError({'Tech Z Loc': 'Key validation error'})
        if 'date_status' in data and data['date_status']:
            data['date_status'] = data['date_status']
            if 'currency' in data and data['currency']:
                try:
                    if data['currency'] != 'USD':
                        data['exchange_rate'] = ExchangeRate.objects \
                            .filter(date__lte=data['date_status'], related_currency_code__code=data['currency']) \
                            .order_by('-date').first().exchange_rate


                    else:
                        data['exchange_rate'] = 1
                except (KeyError, ValueError, AttributeError, ExchangeRate.DoesNotExist):
                    data['exchange_rate'] = None
        return super(VendorQuoteRelationsSerializer, self).to_internal_value(data)


class VendorQuoteUpdateSerializer(serializers.ModelSerializer):
    """VendorQuoteUpdateSerializer

    Creado para update y partial update.
    """
    vendor = serializers.SlugRelatedField(slug_field='slug', queryset=VendorCatalog.objects.all())
    bw_down = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_bw_down',
                                                 queryset=Bandwidth.objects.all())
    bw_up = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, source='related_bw_up',
                                               queryset=Bandwidth.objects.all())
    service_type = serializers.PrimaryKeyRelatedField(source='related_service_type', queryset=ServiceType.objects.all())
    currency = serializers.SlugRelatedField(allow_null=True, source='related_currency', slug_field='code',
                                            required=False, queryset=Currency.objects.all())
    city = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_city', required=False,
                                              queryset=City.objects.all())
    country = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_country', required=False,
                                                 queryset=Country.objects.all())
    a_address = serializers.PrimaryKeyRelatedField(allow_null=True, source='related_a_address', required=False,
                                                   queryset=CommonAddress.objects.all())
    zip_code = serializers.CharField(source='zipcode', required=False, allow_null=True, allow_blank=True)
    created_by = UserSerializerMin(read_only=True)
    tech_a_loc = serializers.MultipleChoiceField(choices=TECH_A_LOC, source='tech_aloc', required=False,
                                                 allow_blank=True, allow_null=True)
    tech_z_loc = serializers.MultipleChoiceField(choices=TECH_Z_LOC, source='tech_zloc', required=False,
                                                 allow_blank=True, allow_null=True)
    last_updated_by = UserSerializerMin(required=False, read_only=True)
    date_created = serializers.DateTimeField(read_only=True)
    task = serializers.SlugRelatedField(allow_null=True, required=False, source='fk_task', slug_field='slug',
                                        queryset=Task.objects.all())
    comments = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    date_status = serializers.DateField(source='status_date', allow_null=True, required=False)
    exchange_rate = serializers.FloatField(required=False, allow_null=True)
    costs_t_i = serializers.BooleanField(write_only=True, default=False, source='costs_taxes_included')

    class Meta:
        model = VendorQuotes
        list_serializer_class = VendorQuoteListSerializer
        fields = ('service_type', 'vendor', 'bw_down', 'bw_up', 'type_of_coverage', 'currency',
                  'city', 'country', 'a_address', 'last_updated_by', 'date_created', 'created_by',
                  'slug', 'last_updated_at', 'term', 'z_address', 'zip_code', 'latitude', 'longitude',
                  'comments', 'nrc', 'mrc', 'status', 'tax_nrc_percentage', 'tax_mrc_percentage',
                  'tax_nrc', 'tax_mrc', 'exchange_rate', 'date_status', 'lead_time', 'solution', 'email_outreach',
                  'quickbase_id', 'tech_a_loc', 'tech_z_loc', 'type_of_coverage', 'last_updated_at', 'task',
                  'location_point', 'email_outreach', 'ip', 'tech_details', 'is_from_vendor_pricelist',
                  'exchange_rate', 'costs_t_i'
                  )


    def to_internal_value(self, data):
        """
        :param data: body json from request+
        :return: data json parsed for internal representation
        """
        # IZO-A, IZO-B, Dark Fiber, IPVPN, Ethernet, Clear Channel / IPLC
        SERVICES_NEED_A_ADDRESS = [5, 8, 15, 18, 28, 41]
        vendor = None
        if 'vendor' in data and data['vendor']:
            try:
                data['vendor'] = data['vendor']['slug']
                vendor = VendorCatalog.objects.get(slug=data['vendor'])
            except (KeyError, ValueError):
                raise serializers.ValidationError({'vendor': 'Vendor Missing slug key'})

        if not 'vendor' in data or not data['vendor']:
            try:
                vendor = VendorQuotes.objects.get(slug=data['slug'])
            except (KeyError, ValueError):
                raise serializers.ValidationError({'vendor': 'Vendor Missing slug key'})

        if 'task' in data:
            try:
                data['task'] = data['task']['slug']
            except (KeyError, ValueError, TypeError):
                data['task'] = None

        if 'service_type' in data and data['service_type']:
            try:
                data['service_type'] = data['service_type'].get('id', '')
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Service Type': 'Vendor Missing id key'})
        if 'bw_down' in data and data['bw_down']:
            try:
                data['bw_down'] = data['bw_down']['id'] if 'id' in data['bw_down'] else None

            except (KeyError, ValueError, TypeError, AttributeError):
                data['bw_down'] = None
                raise serializers.ValidationError({'Bandwidth down': 'Bandwidth Missing id key'})
        if 'bw_up' in data and data['bw_up']:
            try:
                data['bw_up'] = data['bw_up']['id']
            except (KeyError, ValueError):
                data['bw_up'] = None

        if 'currency' in data and data['currency']:
            try:
                data['currency'] = str(data['currency']['code'])
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Currency': 'currency Missing code key'})

        if not 'currency' in data or not data['currency']:
            try:
                data['currency'] = 'BRL' if vendor.related_country.__dict__['name'].lower() in ['brasil', 'brazil'] else vendor.related_currency.__dict__['code']

            except (AttributeError, KeyError, TypeError, KeyError):
                print(traceback.format_exc())
                data['currency'] = 'USD'

        if 'city' in data and data['city']:
            try:
                data['city'] = data['city']['id']
            except (KeyError, ValueError):
                raise serializers.ValidationError({'City': 'city Missing id key'})
        if 'country' in data and data['country']:
            try:
                data['country'] = data['country']['id']
            except (KeyError, ValueError):
                raise serializers.ValidationError({'Country': 'country Missing id key'})
        if 'a_address' in data and data['a_address'] is not None:
            if data['service_type'] in SERVICES_NEED_A_ADDRESS:
                try:
                    data['a_address'] = data['a_address']['id']
                except (KeyError, ValueError):
                    raise serializers.ValidationError({'A address': 'a address Missing id key'})
            else:
                data['a_address'] = ''

        if 'latitude' in data and 'longitude' in data and data['latitude'] and data['longitude']:
            if coord_isvalid(data['latitude'], data['longitude']):
                try:
                    data['location_point'] = 'POINT (' + str(data['longitude']) + ' ' + str(data['latitude']) + ')'
                except (ValueError, KeyError, TypeError):
                    raise serializers.ValidationError({'Coordinates': 'Error representation to point gis'})
            else:
                raise serializers.ValidationError({'Coordinates': 'are not valid'})
        if 'tech_a_loc' in data and data['tech_a_loc']:
            try:
                for item in data['tech_a_loc']:
                    if item not in dict(TECH_A_LOC):
                        raise serializers.ValidationError(
                            {'Tech A Loc': '%s, not in %s' % (item, list((dict(TECH_A_LOC)).keys()))})
            except (ValueError, KeyError, TypeError):
                raise serializers.ValidationError({'Tech A Loc': 'Key validation error'})
        if 'tech_zloc' in data and data['tech_zloc']:
            try:
                for item in data['tech_zloc']:
                    if item not in dict(TECH_Z_LOC):
                        raise serializers.ValidationError(
                            {'Tech Z Loc': '%s, not in %s' % (item, list((dict(TECH_Z_LOC)).keys()))})
            except (ValueError, KeyError, TypeError):
                raise serializers.ValidationError({'Tech Z Loc': 'Key validation error'})
        if 'date_status' in data and data['date_status']:
            data['date_status'] = data['date_status']
            if 'currency' in data and data['currency']:
                try:
                    if data['currency'] != 'USD':
                        data['exchange_rate'] = ExchangeRate.objects \
                            .filter(date__lte=data['date_status'], related_currency_code__code=data['currency']) \
                            .order_by('-date').first().exchange_rate


                    else:
                        data['exchange_rate'] = 1
                except (KeyError, ValueError, AttributeError, ExchangeRate.DoesNotExist):
                    data['exchange_rate'] = None
        return super(VendorQuoteUpdateSerializer, self).to_internal_value(data)

class ProjectSerializerMin(serializers.ModelSerializer):
    user_assignee = UserSerializerMin(source='assignee', read_only=True)
    related_content = ContentObjectRelatedField(source='content_object', read_only=True)
    content_type = serializers.SlugRelatedField(read_only=True, slug_field='model')

    class Meta:
        model = Project
        fields = (
            'name',
            'user_assignee',
            'start_date',
            'type_of_aim',
            'related_content',
            'content_type'
        )


class EventSerializer(serializers.ModelSerializer):
    """EventSerializer

    EventSerializer for serialize an Event object
    """
    created_by = UserSerializer(read_only=True)
    content_type = serializers.SlugRelatedField(slug_field='model',
                                                queryset=ContentType.objects.exclude(app_label='VendorPriceList'))
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'type',
            'object_id',
            'comment',
            'created_at',
            'created_by',
            'content_type'
        )

    def to_internal_value(self, data):
        if 'object_id' in data:
            if isinstance(data['object_id'], int):
                try:
                    data['object_id'] = int(data['object_id'])
                except KeyError:
                    raise serializers.ValidationError({'ObjectId': 'ObjectId is requerid'})
            else:
                try:
                    data['object_id'] = ContentType.objects.exclude(app_label='VendorPriceList').get(
                        model=data['content_type']).model_class().objects.get(
                        slug=data['object_id']).id
                except KeyError:
                    raise serializers.ValidationError({'ObjectId': 'ObjectId is requerid'})
        return super(EventSerializer, self).to_internal_value(data)


class NotificationSerializer(serializers.ModelSerializer):
    """NotificationSerializer

    NotificationSerializer for serialize an Event object
    """

    triggered_by = UserSerializerMin(read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "read", "sent_at", "read_at", "title", "action_url", "description", "triggered_by")


class VQtoCQIrrelevanceRelationSerializer(serializers.ModelSerializer):
    """VQtoCQirrelevanceRelationSerializer
       for serialize an VQtoCQIrrelevanceRelation object.
    """
    fk_vendor_quote_slug = serializers.SlugRelatedField(slug_field='slug', source='fk_vendor_quote',
                                                        queryset=VendorQuotes.objects.all())
    fk_customer_quote_cq_id = serializers.PrimaryKeyRelatedField(source='fk_customer_quote',
                                                                 queryset=UserQuotes.objects.all())

    class Meta:
        model = VQtoCQIrrelevanceRelation
        fields = (
            'id',
            'fk_vendor_quote_slug',
            'fk_customer_quote_cq_id',
            'comment',
            'created_at',
            'created_by',
        )

    def to_internal_value(self, data):
        data['fk_customer_quote_cq_id'] = data['customerQuote']['id']
        data['fk_vendor_quote_slug'] = data['vendorQuote']['slug']
        data.pop('customerQuote')
        data.pop('vendorQuote')
        return super(VQtoCQIrrelevanceRelationSerializer, self).to_internal_value(data)


class CompanySerializer(serializers.ModelSerializer):
    """
    ModelSerializer for serialize a Company object with minimum values
    """

    class Meta:
        model = Company
        fields = (
            'name',
            'quotes_email',
        )


class BandwidthSerializerMin(serializers.ModelSerializer):
    """BandwidthSerializerMin

            BandwidthSerializerMin for serialize a Bandwidth object with minimum values
        """
    bw = serializers.IntegerField(source='id')

    class Meta:
        model = Bandwidth
        fields = ('bw', 'label')


class ServiceSerializer(serializers.ModelSerializer):
    """
        ServiceSerializer for serialize a Service object
    """
    related_customer = CompanySerializer()
    related_service_type = ServiceTypeSerializer()
    related_requested_bw_down = BandwidthSerializerMin()

    class Meta:
        model = Service
        fields = ['service_id',
                  'order_date',
                  'related_service_type',
                  'related_customer',
                  'related_requested_bw_down',
                  'latitude',
                  'longitude',
                  'squickbase_id',
                  'related_customer_quote',
                  'status',
                  'updated_at'
                  ]


class CountySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(
        source='related_state',
        read_only=True,
        slug_field='name')

    country = serializers.SlugRelatedField(
        source='related_country',
        read_only=True,
        slug_field='name')

    class Meta:
        model = County
        fields = ('name', 'state', 'country', 'slug')


class StateSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(source='related_country',
                                           read_only=True,
                                           slug_field='name')

    class Meta:
        model = State
        fields = ('name', 'country', 'slug')


class OfficialCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialCountry
        fields = ['name', 'slug', 'state_label', 'county_label', 'city_label']


# VendorPOP Serializers

class VendorPopSerializer(serializers.ModelSerializer):
    """
    Clase serializadora del modelo Vendor Pop. (Lectura)
    """

    from api.procurement.serializers import (
        VendorCatalogMinSerializer
    )

    # Relaciones:

    vendor = VendorCatalogMinSerializer(read_only=True,
                                        source='fk_vendor')

    common_address = CommonAddressSerializer(read_only=True,
                                             source='fk_common_address')

    class Meta:
        model = VendorPOP
        fields = ('slug',
                  'name',
                  'vendor',
                  'common_address')


class VendorPopRelationsSerializer(serializers.ModelSerializer):
    """
    Clase serializadora del modelo Vendor Pop. (Escritura)
    """

    # Relaciones

    vendor = serializers.SlugRelatedField(slug_field='slug',
                                          allow_null=False,
                                          required=True,
                                          source='fk_vendor',
                                          queryset=VendorCatalog.objects.all())

    common_address = serializers.PrimaryKeyRelatedField(allow_null=False,
                                                        required=True,
                                                        source='fk_common_address',
                                                        queryset=CommonAddress.objects.all())

    class Meta:
        model = VendorPOP
        fields = ('slug',
                  'name',
                  'vendor',
                  'common_address')

        # def to_internal_value(self, data):
        #     """
        #     Metodo que se encarga de realizar las transformacion necesarias para la deseralizacion
        #     """
        #     if 'vendor' in data and data['vendor']:
        #         try:
        #             data['vendor'] = data['vendor']['slug']
        #             vendor = VendorCatalog.objects.get(slug=data['vendor'])
        #         except (KeyError, ValueError):
        #             raise serializers.ValidationError({'vendor': 'Vendor Missing slug key'})
        #
        #     if 'common_address' in data and data['common_address']:
        #         try:
        #             data['common_address'] = data['common_address']['id']
        #         except (KeyError, ValueError):
        #             raise serializers.ValidationError({'Common Address': 'Common Address Missing slug key'})
        #
        #     return super(VendorPopRelationsSerializer, self).to_internal_value(data)

# -----
