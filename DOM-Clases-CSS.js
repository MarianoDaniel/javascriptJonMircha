//Curso JavaScript: 65. DOM: Clases CSS

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
$card.classList.toggle("opacity-80","sepia") 