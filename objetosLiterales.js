console.log("********************************************")
console.log("**************Objetos literales*********")

//Forma de escribir atributos y métodos. Es una forma de asignarlos

let nombre = "Perro",
    edad = 7

const perro = {
    nombre: nombre,
    edad: edad,
    ladrar: function () {
        console.log("Guauuu Guauuu")
    }
}

console.log(perro)
perro.ladrar()

//con las nuevas caracteristicas se reutilizan las variables creadas anteriormente

const dog = {
    nombre,
    edad,
    raza: "Callejero",
    ladrar() {
        console.log("Guauu Guauuu Guaaauuuu")
    }
}
console.log(dog)
dog.ladrar()