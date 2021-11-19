//Curso JavaScript: 69. DOM: Templates HTML

//Etiquetas que no se visualizan    

const $cards = document.querySelector(".cards"),
    $template = document.getElementById("template-card").content, //.content trae el contenido no la etiqueta
    $fragment = document.createDocumentFragment(),
    cardContent = [
        {
            title: "Tecnología",
            img: "https://placeimg.com/200/200/tech"
        },
        {
            title: "Animales",
            img: "https://placeimg.com/200/200/animals"
        },
        {
            title: "Arquitectura",
            img: "https://placeimg.com/200/200/arch"
        },
        {
            title: "Gente",
            img: "https://placeimg.com/200/200/people"
        },
        {
            title: "Naturaleza",
            img: "https://placeimg.com/200/200/nature"
        }
    ]

cardContent.forEach(el => {
    $template.querySelector("img").setAttribute("src", el.img)
    $template.querySelector("img").setAttribute("alt", el.title)
    $template.querySelector("figcaption").textContent = el.title

    //Vamos a clonar el template para poder generar varios y utilizarlos
    //Le pasamos true al segundo parametro para que copie toda la estructura, de locontrario solo copia la etiqueta
    //importa el modelo a seguir que está en el html
    let $clone = document.importNode($template, true)
    $fragment.appendChild($clone)
})
$cards.appendChild($fragment)
console.log($template)