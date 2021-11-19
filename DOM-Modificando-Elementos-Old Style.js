//Curso JavaScript: 70. DOM: Modificando Elementos (Old Style)  

const $cards = document.querySelector(".cards"),
    $newCard = document.createElement("figure"),
    $cloneCards = $cards.cloneNode(true); //generar dinamicamente un clon

$newCard.innerHTML = `<img src= "https://placeimg.com/200/200/any" alt="Any"
<figcaption>Any</figcaption>
`
//le agrego una nueva clase
$newCard.classList.add("card")

//remplazamos un hijo. Se le pasa primero el nuevo y después el que va a ser remplazado
$cards.replaceChild($newCard, $cards.children[2])

//Si queremos insertar la card antes
$cards.insertBefore($newCard, $cards.firstElementChild)

//Para eliminar
$cards.removeChild($cards.lastElementChild)

//agrego al body el clon de cards
document.body.appendChild($cloneCards)