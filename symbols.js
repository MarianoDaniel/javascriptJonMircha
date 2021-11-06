/**Nuevos tipos de datos en javascript: Suelen usarse para identificar propiedades de objetos, para evitar coliciones, sobreescrituras */

const NOMBRE = Symbol("Nombre")
const SALUDAR = Symbol("Saludo")
const persona = {
    [NOMBRE]: "Mariano",
    edad:34
}

console.log(persona)
console.log(persona[NOMBRE])

//Funcines con symbol

persona[SALUDAR] = function () {
    console.log("Hola!")
}
console.log(persona)
persona[SALUDAR]()

for (const key in persona) {
console.log(`key: ${key}, value: ${persona[key]}`)
    
}
//las propiedades de tipo symbol no se listan

//Método para ver si un objeto tiene propiedades de tipo symbol

console.log(Object.getOwnPropertySymbols(persona))