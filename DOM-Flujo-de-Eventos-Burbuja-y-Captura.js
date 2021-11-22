//DOM: Flujo de Eventos (Burbuja y Captura) 

const $divsEventos = document.querySelectorAll(".eventos-flujo div")
console.log($divsEventos)

function flujoEventos(e) {
    console.log(`Hola te saluda ${this.className}, el click lo originó ${e.target.className}`)
}

$divsEventos.forEach(div => {
    //fase de burbuja
    //div.addEventListener("click",flujoEventos) //si le agrego false hace lo mismo, está así por defaul
    //Fase de captura
    div.addEventListener("click", flujoEventos, true)

    //options
    /*     div.addEventListener("click",flujoEventos, {
            capture:true,
            once:true
        }) */
})