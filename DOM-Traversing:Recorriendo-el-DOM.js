
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
