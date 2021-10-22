console.log("********************************************")
console.log("**************Iterables*********")
const yo = {
    nombre: "Mariano",
    apellido: "Avico",
    edad: 34
}
//for in nos permite recorrer propiedades de un objeto
for (const property in yo) {
    console.log(`Key: ${property}, Value: ${yo[property]} `)
}

//mientras que for of me permite rrecorrer todos los elementos //de cualquier objeto que sea iterable
const numeros= Array.of(10,20,30,40,50,60,70,80,90,100)
console.log(numeros)
for(const elemento of numeros){
console.log(elemento)
}

let cadena = "Hola Mundo"

for(const caracter of cadena){
    console.log(caracter)
} 