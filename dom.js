/* //manejar html con javascript
//del ojb window cuelgan todas las apis del navegador

console.log(window.document)
console.log(document)
console.log(document.head)
console.log(document.body)
console.log(document.documentElement)
console.log(document.doctype)
console.log(document.charset)
console.log(document.title)
console.log(document.links)
console.log(document.images)
console.log(document.forms)
console.log(document.styleSheets)
//si me imprime 2 scripts uno puede deberse al live server
console.log(document.scripts)
setTimeout(() => {
console.log(document.getSelection().toString())    
}, 3000);
document.write("<h2>Hola mundo desde el DOM</2>") */

/* console.log(document.getElementsByTagName("li"))
console.log(document.getElementsByClassName("card"))
console.log(document.getElementsByName("nombre"))
//Los tres anteriores fueron remplazados por los sigientes operadores

//1:
//hay que especificar si se trata de un id, una clase o un nombre anteponiendole el signo correspondiente, en este caso #
console.log(document.querySelector("#menu"))
//trae 1 elemento
console.log(document.querySelector("a"))

//2:
//trae todos los elementos
console.log(document.querySelectorAll("a"))
document.querySelectorAll("a").forEach(el => {
    console.log(el)
})
//También está el siguiente operador
console.log(document.getElementById("menu"))

console.log(document.querySelectorAll(".card")[2])
//Traeme todas las listas del menu
console.log(document.querySelectorAll("#menu li"))



//Curso JavaScript: 63. DOM: Atributos y Data-Attributes

console.log(document.documentElement.lang)
console.log(document.documentElement.getAttribute("lang"))
//Me trae toda la url porque utilicé el punto (.href)
console.log(document.querySelector(".link-dom").href)
//si utilizo el método getAtribute, me trae el valor del href
console.log(document.querySelector(".link-dom").getAttribute("href"))

//Cambiando el valor de los atributos

document.documentElement.lang = "es"
console.log(document.documentElement.lang)
//también tenemos un método para setear el valor
document.documentElement.setAttribute("lang", "en")
console.log(document.documentElement.lang)

//Me guardo el elemento html en una variable. Buena práctica anteponerle $
const $linkDOM = document.querySelector(".link-dom")

$linkDOM.setAttribute("target", "_blank")
//La pestaña que se abre no tiene relación con la anterior 
$linkDOM.setAttribute("rel", "noopener")

//Puedo preguntar si mi elemento tiene un atributo
console.log($linkDOM.hasAttribute("rel"))

//Borrar un atributo
$linkDOM.removeAttribute("rel")

console.log($linkDOM.hasAttribute("rel"))


//Podemos crear nuestros propios atributos, siempre y cuando utilicemos la palabra data más el -  (data-)

console.log($linkDOM.getAttribute("data-description"))

//Todos los data atribute los guarda en un dataset
console.log($linkDOM.dataset)
console.log($linkDOM.dataset.description)
$linkDOM.setAttribute("data-description", "Modelo de objeto del documento")
console.log($linkDOM.dataset.description)
//con la notación del punto
$linkDOM.dataset.description = "Suscribete a mi canal y comparte"
console.log($linkDOM.dataset.description)


//Curso JavaScript: 64. DOM: Estilos y Variables CSS
//Acá si es importante acceder con la notación del punto ya que me permite acceder a todas las propiedades, getAtribute no

//Obteniendo estilos
console.log($linkDOM.style)
console.log($linkDOM.getAttribute("style"))
console.log($linkDOM.style.backgroundColor)
//getComputedStyle mapea tal cual lo lee el navegador por ej si 1 rem lo lee a 16 px
console.log(window.getComputedStyle($linkDOM))
console.log(window.getComputedStyle($linkDOM).getPropertyValue("color"))

//Estableciendo valores

$linkDOM.style.setProperty("text-decoration", "none")
$linkDOM.style.setProperty("display", "block")
//también se puede hacer con la notación del punto

$linkDOM.style.width = "50%"
$linkDOM.style.textAlign = "center"
$linkDOM.style.marginLeft = "auto"
$linkDOM.style.marginRight = "auto"
$linkDOM.style.padding = "1rem"
$linkDOM.style.borderRadius = "5rem"

//En el listado se ven todas las propiedades que cambié
console.log($linkDOM.style)

//Cadena de texto con todos los atributos que agregué en style
console.log($linkDOM.getAttribute("style"))

//Variables CSS - Custom Properties

const $html = document.documentElement,
    $body = document.body;

//accediendo a las propiedades(variables) del selector root 
let varDarkColor = getComputedStyle($html).getPropertyValue("--dark-color")
let varyellowColor = getComputedStyle($html).getPropertyValue("--yellow-color")
console.log(varDarkColor,varyellowColor)

//Utilizo las variables para agregarselas a algunas propiedades del body

$body.style.backgroundColor = varDarkColor
$body.style.color = varyellowColor

//modificando las variables css --> obtengo el html -->accedo a su elemento style --> hago set 
$html.style.setProperty("--dark-color","#000")
//con lo anterior cambiamos de valor la variable del root pero todavía no le cargamos este nuevo valor a varDarkColor, por lo que sigue teniendo el valor anterior
varDarkColor = getComputedStyle($html).getPropertyValue("--dark-color")
//ya tengo mi nuevo valor, pero quiero que cambie mi body, por lo que tengo que volver a agregarle esta variable con este nuevo valor que acabo de asignarle
$body.style.backgroundColor = varDarkColor  */


//Curso JavaScript: 65. DOM: Clases CSS
/* 
const $card = document.querySelector(".card")
console.log($card)

//acceder al valor del atributo class
console.log($card)
console.log($card.className)
console.log($card.classList)
console.log($card.classList.contains("rotate-45"))
//agregando clases
$card.classList.add("rotate-45")
console.log($card.classList.contains("rotate-45"))
//Ya figuran los 2 elementos
console.log($card.className)
console.log($card.classList)

//Remuevo clase
$card.classList.remove("rotate-45")
//Verifico que lo haya borrado
console.log($card.classList.contains("rotate-45"))
$card.classList.toggle("rotate-45")
console.log($card.classList.contains("rotate-45"))
$card.classList.toggle("rotate-45")
console.log($card.classList.contains("rotate-45"))
$card.classList.toggle("rotate-45")
console.log($card.classList.contains("rotate-45"))
//no agrega la clase sino que pisa el valor (rotate-135 pisa a rotate-45)
$card.classList.replace("rotate-45", "rotate-135")
console.log($card.classList)
//Manipular varias clases al mismo tiempo
$card.classList.add("opacity-80","sepia")
$card.classList.remove("opacity-80","sepia")
$card.classList.toggle("opacity-80","sepia") */

//Curso JavaScript: 66. DOM: Texto y HTML

const $whatisDOM = document.getElementById("que-es")
let text = `
 <p> El Modelo de Objetos del Documento(<b><i>DOM-DocumentObject Model </i></b>) es un API para documentos HTML y XML
 </p>
 <p>
 Éste proveé ua representación estructural del document, permitiendo modificar su contenido y presentación visual mediaten código JS
 </p>
 <p>
 <mark>
 El DOM no es parte de la especificación de JavaScript, es una API para los navegadores.
 </mark>
 </p>
`
//innerText no reconoce las característica de HTML (No forma parte del standar)
$whatisDOM.innerText = text
//Tampoco interpreta las etiquetas html. Es para utilizar solo texto
$whatisDOM.textContent = text
//Interpreta HTML
$whatisDOM.innerHTML = text
//Remplaza el elemento del dom por el contenído que le agregas. 
$whatisDOM.outerHTML = text


//Curso JavaScript: 67. DOM Traversing: Recorriendo el DOM
//Propiedades que nos da el DOM para poder recorrer los diferentes elementos de un nodo

//Vamos a utilizar las propiedades que nos sirven para recorrer los elementos

const $cards = document.querySelector(".cards")

console.log($cards)
//Hacer referencia a sus hijos

console.log($cards.children)
console.log($cards.children[3])

// quién es el padre
console.log($cards.parentElement)

//Obtener el primero y el último del elemento hijo
console.log($cards.firstElementChild)
console.log($cards.lastElementChild)

//Elementos anterior y siguientes al que estoy parado

console.log($cards.previousElementSibling)
console.log($cards.nextElementSibling)

//Hay métodos para los elementos y para los nodos, si uso el de los nodos se escribe igual solo que elimino la palabra Element del medio. Esto seguro me trae los espacios de salto de linea, son nodos. por ej:
console.log($cards.previousSibling)

//Busca el padre más cercano del selector que le pasemos por parámetro
console.log($cards.children[3].closest("section"))


//Curso JavaScript: 68. DOM: Creando Elementos y Fragmentos





