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