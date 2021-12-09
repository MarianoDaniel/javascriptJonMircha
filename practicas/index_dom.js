import scrollTopButton from "./botton_scroll.js";
import countdown from "./cuenta_regresiva.js";
import userDeviceInfo from "./deteccion_dispositivos.js";
import networkStatus from "./deteccion_red.js";
import webCam from "./deteccion_webcam.js";
import hamburguerMenu from "./menu_hamburguesa.js";
import responsiveMedia from "./objeto_responsive.js";
import { relojYalarma, alarm } from "./reloj_y_alarma.js";
import responsiveTester from "./responsive_tester.js";
//import { shortcuts } from "./teclado.js";
import { moveBall } from "./teclado.js";
import darkTheme from "./tema_oscuro.js";

//Vamos a cargarlo con el DOMContentLoaded
const d = document
d.addEventListener("DOMContentLoaded", e => {
    //le paso las clases y el parámetro menú a para que al presionarlo se cierre el panel
    hamburguerMenu(".panel-btn", ".panel", ".menu a")
    relojYalarma("#iniciar-reloj", "#detener-reloj", "#panel-reloj p", "#panel-reloj")
    alarm("assets/alarm.mp3", "#iniciar-alarma", "#detener-alarma")
    countdown(
        "countdown",
        "May 23,2022 03:23:19",
        "Feliz cumpleaños amigo y docente digital 🤓🤓🤓")
    scrollTopButton(".scroll-top-btn")
    darkTheme(".dark-theme-btn", "dark-mode")
    responsiveMedia(
        "youtube",
        "(min-width: 1024px)",
        `<a href="https://www.youtube.com/watch?v=6IwUl-4pAzc&list=PLvq-jIkSeTUZ6QgYYO3MwG9EMqC-KoLXA&index=91" target="_blank" rel ="noopener"> Ver Video </a>`,
        `<iframe width="560" height="315" src="https://www.youtube.com/embed/6IwUl-4pAzc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`)
    responsiveMedia(
        "gmaps",
        "(min-width: 1024px)",
        `<a href="https://goo.gl/maps/JNUneA2tSVfMYpecA" target="_blank" rel ="noopener"> Ver Mapa </a>`,
        `<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3284.0168878894424!2d-58.383759084106686!3d-34.603734465007335!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4aa9f0a6da5edb%3A0x11bead4e234e558b!2sObelisco!5e0!3m2!1sen!2sar!4v1638629167603!5m2!1sen!2sar" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>`)
    responsiveTester("responsive-tester")
    userDeviceInfo("user-device")
    webCam("webcam")
})
d.addEventListener("keydown", e => {
    //shortcuts(e)
    moveBall(e, ".ball", ".stage")
})
networkStatus()