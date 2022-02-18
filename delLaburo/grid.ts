/* import { Component, Input, OnChanges, OnInit, ViewChild } from '@angular/core';
import { CustomerQuote } from "../../../../../core/models/pricing/customer-quote";
import { CustomerQuotesService } from "../../../services/customer-quote.service";
import { ColDef, ColumnApi, GridApi } from 'ag-grid-community';
import { Service } from "../../../../../core/models/coreflow/service";
import { AgGridAngular } from 'ag-grid-angular';
import { ServicioService } from '../../../services/servicio.service';
import { ServiceSupportLevelRendererComponent } from './components-for-service-delivery/service-support-level-renderer/service-support-level-renderer.component';

@Component({
  selector: 'app-service-delivery-form',
  template: ` 
  <button (click)="getSelectedRows()">Get Selected Rows</button>
  <div *ngIf="rowData.length >0">    
  <ag-grid-angular
    #myGrid
    style="width: 1950px; height: 500px;"
    class="ag-theme-alpine"
    [rowData]="rowData"
    [columnDefs]="columnDefs"
    (cellClicked)="onCellClicked($event)"
    (gridReady)="onGridReady($event)"
    (cellValueChanged)="onCellValueChanged($event)"
  >
  </ag-grid-angular>
</div>
<ul id="modalList"></ul>
  `,
})
export class ServiceDeliveryFormComponent implements OnInit, OnChanges {
  @Input() ids: [] = [];
  columnDefs: ColDef[] = [];
  rowData = [];
  columnApi: ColumnApi;
  api: GridApi;
  columnasCQ: string[] = ['z_address', 'term', 'latitude', 'longitude', 'customer_quote', 'related_end_customer', 'service_type', 'z_postal_code',]
  term: string[] = ['One Time', '1 month', '3 months', '6 months', ' 8 months', '12 months', '18 months', '19 months', ' 24 months', '36 months', '48 months', '60 months', '72 months']
  @ViewChild('myGrid', { static: false }) agGrid: AgGridAngular

  constructor(private sCostumerQuote: CustomerQuotesService,
    private sService: ServicioService) {

  }

  ngOnInit(): void {

  }

  ngOnChanges(): void {
 */

    /**
     Utilizo el servicio para traerme las cq al mandarle un objeto como lo
     espera el filtro (Hay que ver si se puede mejorar y presindir del filtro)
     */
   /*  this.sCostumerQuote.getCustomerQuotes({
      cq_id: this.ids
    }).subscribe(res => {
      console.log(res); */
      /**
       recorro la respuesta que tiene las cq, creo un servicio con la
       función estática fromCustomerQuote que me permite popular los
       campos de este con datos de la cq
       */
      /**Me guardo las claves del objeto servicio en un array.*/
/*       const cabeceraServicio = Object.keys(new Service({})); */
      /**
       Creo un objeto cuyo valor sea la clave de las propiedades de la
       entidad Servicio {field: nombre de la clave} así lo espera la librería --> ej: {field: "project_id"}
       Cada objeto se pushea al array columnDefs que viene predeterminado
       por la librería 'ag-grid-community'
       */
      /* cabeceraServicio.forEach((key, i) => {
        this.columnDefs.push(this.columnMaker(cabeceraServicio[i + 1]))
   /*    }); */
    /*   res.forEach((cq) => {
        const row = {};
        const service = Service.fromCustomerQuote(cq); */
        /**Como hice con la cabecera*/
     /*    const keyForCreatePropery = Object.keys(service); */ 
        /**
         Recorro las claves y creo las propiedades en row con los nombres de las de service,
         luego le cargo el valor de lo que hay en el service creado que ya tiene agregado lo de la cq
         */
    /*     keyForCreatePropery.forEach((key, i) => {
          row[keyForCreatePropery[i + 1]] = service[keyForCreatePropery[i + 1]]; */
        /* }); */
        /**Agrego el objeto creado al rowData. Este rowData va a ser usado por la librería para renderizar las filas en la tabla.**/
/*         this.rowData.push(row)
      });
      console.log(this.rowData)
    })
  } */
/* 
  onCellClicked(e) {
    if (this.columnasCQ.indexOf(e.colDef.field) === -1) {
      e.colDef.editable = true
      this.modalFunction(e)


    }

  } */
/*   modalFunction(e) {
    console.log("MODALFUNCTION", e)
    if (e.colDef.field === "status") {
      const $olMenu = document.getElementById("modalList")
      $olMenu.innerHTML = ""
      $olMenu.style.position = "absolute"
      $olMenu.style.left = `${e.event.clientX}px`
      $olMenu.style.top = `${e.event.clientY}px`
      $olMenu.style.background = "#babfc7"
      $olMenu.style.color = "black"
      document.addEventListener("click", e => { $olMenu.innerHTML = "" })
      this.term.forEach(t => {
        const $li = document.createElement("li");
        console.log(e.this)
        $li.onclick = function (this) {
          console.log("Resultado select", t)
          e.data.status = t
          
        }
        $li.innerHTML = `<a>${t}</a>`
        $olMenu.appendChild($li)

      })

    }
  }

  onGridReady(e) {
    this.api = e.api
    this.columnApi = e.columnApi
  }
  onCellValueChanged(e) {
    console.log(e.value)
    console.log(e)
  }
  getSelectedRows() {
    try {
      this.agGrid.gridOptions.rowData.forEach((service: Service) => {
        this.sService.createService(service).subscribe(res => {
          console.log(res)
        })
      })
    } catch (error) {
      console.log(error)
    }


  }
  columnMaker(nombreCol): object {
    return { field: nombreCol, filter: true };
  }
} */
