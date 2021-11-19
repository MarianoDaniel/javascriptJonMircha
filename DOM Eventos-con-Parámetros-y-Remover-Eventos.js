//DOM: Eventos con Parámetros y Remover Eventos

function saludar(nombre = "Desconocido") {
    //nombre = prompt("indique su nombre")
    alert(`Hola ${nombre}`)
}

const $eventoMultiple = document.getElementById("evento-multiple")
//Para pasar parámetros utilizamos como handler function una función anonima o arrow
$eventoMultiple.addEventListener("click", () => {
    saludar()
    saludar("Mariano")
})

//Remover eventos
const $eventRemove = document.getElementById("evento-remover")

const removerDobleClick = (e) => {
    alert(`Removiendo el evento de tipo ${e.type}`)
    $eventRemove.removeEventListener("dblclick", removerDobleClick)
    $eventRemove.disabled = true
}

$eventRemove.addEventListener("dblclick", removerDobleClick)
