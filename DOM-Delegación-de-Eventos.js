// DOM: Delegación de Eventos

function flujoEventos(e) {
    console.log(`Hola te saluda ${this}, el click lo originó ${e.target.className}`)
}

//Un detalle importante es que vamos a evitar la propagación, porque el evento está asignado al document

//acá tenemos un solo lisener para cada caso porque se le asigna al document
document.addEventListener("click", (e) => {
    console.log("Click en", e.target)

    if (e.target.matches(".eventos-flujo div")) {
        flujoEventos(e)
    }
    if (e.target.matches(".eventos-flujo a")) {
        alert("Hola soy tu amigo")
        e.preventDefault()
    }
})