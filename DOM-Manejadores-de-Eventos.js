//Curso JavaScript: 72. DOM: Manejadores de Eventos
//las funciones que se ejecutan en un evento se llaman manejadores o escuchadores, event handler etc..
//Manejador del evento
function holaMundo() {
    console.log("hola mundo")
    alert("Hola mundo")
    //cuando una función se convierte en manejador podemos acceder a ese evento en sí $event
    console.log(event)
}

//evento semantico. Solo se puede agregar un evento con un handler, si le agrego otro pisa el anterior
const $eventoSemantico = document.getElementById("evento-semantico")
$eventoSemantico.onclick = holaMundo

//Diferentes funciones a un mismo elemento: tenemos manejadores múltiples

const $eventoMultiple = document.getElementById("evento-multiple")
$eventoMultiple.addEventListener("click", holaMundo)
$eventoMultiple.addEventListener("click", (e) => {
    alert("Hola mundo manejador de eventos múltiple")
    console.log(e)
    console.log(e.type)
    console.log(e.target)
})
