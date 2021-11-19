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