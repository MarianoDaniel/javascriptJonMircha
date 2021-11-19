//manejar html con javascript
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
document.write("<h2>Hola mundo desde el DOM</2>")

console.log(document.getElementsByTagName("li"))
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
