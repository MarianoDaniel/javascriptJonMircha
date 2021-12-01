import hamburguerMenu from "./menu_hamburguesa.js";
import { relojYalarma, alarm } from "./reloj_y_alarma.js";
//import { shortcuts } from "./teclado.js";
import { moveBall } from "./teclado.js";

//Vamos a cargarlo con el DOMContentLoaded
const d = document
d.addEventListener("DOMContentLoaded", e => {
    //le paso las clases y el parámetro menú a para que al presionarlo se cierre el panel
    hamburguerMenu(".panel-btn", ".panel", ".menu a")
    relojYalarma("#iniciar-reloj", "#detener-reloj", "#panel-reloj p", "#panel-reloj")
    alarm("assets/alarm.mp3", "#iniciar-alarma", "#detener-alarma")
})
d.addEventListener("keydown", e => {
    //shortcuts(e)
    moveBall(e, ".ball", ".stage")
})
