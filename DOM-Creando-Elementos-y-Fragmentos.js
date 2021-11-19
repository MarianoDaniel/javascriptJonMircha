//Curso JavaScript: 68. DOM: Creando Elementos y Fragmentos

const $figure = document.createElement("figure"),
    $img = document.createElement("img"),
    $figcaption = document.createElement("figcaption"),
    $figcaptionText = document.createTextNode("Animals"),
    $cards = document.querySelector(".cards");

$img.setAttribute("src", "https://placeimg.com/200/200/animals")
$img.setAttribute("alt", "Animals")
$figure.classList.add("card")

$figcaption.appendChild($figcaptionText)
$figure.appendChild($img)
$figure.appendChild($figcaption)
$cards.appendChild($figure)

//Crear dinamicamente un conjunto de elementos. Como si se hiciera una petición y tendríamos que renderizar varios elementos

const estaciones = ["Primavera", "Verano", "Otoño", "Invierno"]
$ul = document.createElement("ul")

document.write("<h3>Estaciones del Año</h3>")
//Le agrego la etiqueta al body 
document.body.appendChild($ul)
//recorro el array para poder renderizar varios elementos
estaciones.forEach(el => {
    //creo la etiqueta li que va a estar dentro de up
    $li = document.createElement("li")
    //le asigno a las etiquetas el valor de cada estación
    $li.textContent = el
    //Agrego el li a ul
    $ul.appendChild($li)
})

//otra forma de hacer lo anterior

const continentes = ["África", "América", "Asia", "Europa", "Oceanía"]
$ul2 = document.createElement("ul")
document.write("<h3>Continentes del mundo</h3>")
document.body.appendChild($ul2)
$ul2.innerHTML = ""
continentes.forEach(el => $ul2.innerHTML += `<li>${el}</li>`)

//El problema de lo de arriba es que si es para pocos elementos, no hay problema, pero cuando tengo que renderizar una gran cantidad de elementos que, por ej, vienen de una petición, sería mejor utilizar una técnica que agarra un fragmento del dom, le carga todos los elementos en memoria y cuando termina se lo inyecta al DOM de una sola vez

//FRAGMENTOS // FORMA ÓPTIMA PARA TRABAJAR


const meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]
const $ul3 = document.createElement("ul"),
    //Creación del fragmento
    $fragment = document.createDocumentFragment();
//como es un fragmento del DOM no se puede utilizar innerHTML

//Itero sobre los elementos
meses.forEach(el => {
    //creo un elemento li
    const $li = document.createElement("li")
    //Le agrego los elementos a ese li 
    $li.textContent = el
    //Le asigno esta etiqueta a fragment
    $fragment.appendChild($li)
})

document.write("<h3>Meses del año</h3>")
//Agrego a $ul3 el fragmento del DOM con todos los elementos que le metí 
$ul3.appendChild($fragment)
//por último se realiza la inyección de un tirón al DOM, evitando las inyecciones continuas que hacíamos en el foreach anterior a este ejemplo
document.body.appendChild($ul3)