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