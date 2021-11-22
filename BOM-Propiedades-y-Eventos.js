//BOM: Propiedades y Eventos
//No es estandar aunque ya no hay problema.
//Son una serie de métodos y objetos que cuelgan de window


window.addEventListener("resize", (e) => {
    console.clear()
    console.log("**************Evento Resize*************")
    //Propiedad innerWidth va a hacer referencia al ancho del view port de la ventana
    console.log(window.innerWidth)
    //Lo mismo para la altura
    console.log(window.innerHeight)
    //Ancho del navegador
    console.log(window.outerWidth)
    //Alto del navegador
    console.log(window.outerHeight)

    console.log(e)
})
//Evento Scroll
window.addEventListener("scroll", e => {
    //para que vaya borrando los valores anteriores y no ensucie la consola
    console.clear()
    console.log("**************Evento Scroll***********")
    console.log("Evento Scroll", e)
    //Scroll
    console.log("Scroll X", window.scrollX)
    console.log("Scroll Y", window.scrollY)
})

//Evento Load: Se dispara y hasta que haya cargado todo no se ejecuta (espera hojas de estilo, scripts...etc)

window.addEventListener("load", e => {
        console.log("**************Evento load***********")
        console.log("Evento load", e)
        //Scroll
        console.log("Scroll X", window.screenX)
        console.log("Scroll Y", window.screenY)
})

// DOMContentLoaded: Es una mejor práctica. Es mucho más eficiente trabajar con este evento.(no espera a que carguen las hojas de estilo... las imagenes etc)

document.addEventListener("DOMContentLoaded", e => {
    console.log("**************Evento DOMContentLoaded***********")
    console.log("Evento load", e)
    //Scroll
    console.log("Scroll X", window.screenX)
    console.log("Scroll Y", window.screenY)
})