console.log("********************************************")
console.log("**************Objeto Console*********")


console.log(console)
console.error("Esto es un error")
console.warn("Esto es un aviso")

let nombre = 'Mariano',
    apellido = 'Avico',
    edad = 34

console.log(`Hola mi nombre es %s %s y tengo %s años.`, nombre, apellido, edad)

console.clear()

console.log(window)
console.log(document)
//Muestra todas las propiedades objetos metodos atributos del
//document
console.dir(document)

console.clear()

console.group("Los cursos de jon en YouTube")
console.log("Curso de JavaScript")
console.log("Curso de NodeJs")
console.groupEnd()

console.clear()

console.table(Object.entries(console).sort())
console.clear()

const numeros= [1,2,3,4,5,6,7],
vocales=['a','e','i','o','u']

console.table(numeros)
console.table(vocales)

const perro = {
    nombre:'Marafiotti',
    raza:'champinion',
    color:'transparente'
}

console.table(perro)

console.clear()

console.time("Cuanto tiempo tarda mi código")
const arreglo = Array(1000000)
for(let i =0; i<arreglo.length; i++){
    arreglo[i] = i
}
console.timeEnd("Cuanto tiempo tarda mi código")
//console.log(arreglo)