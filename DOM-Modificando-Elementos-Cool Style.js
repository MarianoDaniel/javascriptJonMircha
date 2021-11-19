//Curso JavaScript: 71. DOM: Modificando Elementos (Cool Style)

//insertAdjacent...
/*  insertAdjacent(position,el)
insertAdjacent(position,html)
insertAdjacent(position,text) */

//Posiciones:
/*  beforebegin(hermano anterior)
afterbegin(primer hijo)
beforeednd(ultimo hijo)
afterend(hermano siguiente)  */

const $cards = document.querySelector(".cards"),
    $newCard = document.createElement("figure");

let $contentCard = `
<img src="https://placeimg.com/200/200/any" alt="Any"
<figcaption></figcaption>
`
//le agrego una nueva clase
$newCard.classList.add("card")

$newCard.insertAdjacentHTML("beforeend", $contentCard)
$newCard.querySelector("figcaption").insertAdjacentText("afterbegin", "Any")
$cards.insertAdjacentElement("afterbegin", $newCard)