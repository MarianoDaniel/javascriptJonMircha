console.log("********************************************")
console.log("**************Arrow Function*********")

const saludar = nombre => console.log(`Hola ${nombre}`)
saludar("Mariano")

const suma = (a, b) => a + b
console.log(suma(8, 9))


const numeros = [1, 2, 3, 4, 5, 6, 7]

numeros.forEach((el, index) => console.log(`El ${el} esta en la posición ${index}`))

const perreque = {
    nombre: "Firulai",
    ladrar() {
        console.log(this)
    }
}
//Si utilizo una arrow function en un objeto y le pido el this.. me trae el objeto window porque la arrow hace referencia al objeto padre que contiene todo lo demás 

const perreque = {
    nombre: "Firulai",
    ladrar: () => {
        console.log(this)
    }
}
perreque.ladrar()
