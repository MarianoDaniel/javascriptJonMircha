// DOM: stopPropagation & preventDefault 
const $divsEventos = document.querySelectorAll(".eventos-flujo div"),
    $linkEventos = document.querySelector(".eventos-flujo a")

function flujoEventos(e) {
    console.log(`Hola te saluda ${this.className}, el click lo originó ${e.target.className}`)
    //Evitar la propagación, es un método del evento
    e.stopPropagation()
}


$divsEventos.forEach(div => {
    div.addEventListener("click", flujoEventos)
})

//prevent Default
$linkEventos.addEventListener("click", (e) => {
    alert("Hola soy tu amigo y docente digital... Jonathan Mircha")
    console.log(e)
    e.preventDefault()
    e.stopPropagation()
})