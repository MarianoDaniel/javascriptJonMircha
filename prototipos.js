console.log("********************************************")
console.log("**************Prototipos*********")

const animal = {
    nombre: "Snoopy",
    sonar() {
        console.log("Hago sonidos porque estoy vivo")
    }
}

const animal2 = {
    nombre: "Lola Bunny",
    sonar() {
        console.log("Hago sonidos porque estoy vivo")
    }
}

console.log(animal)
console.log(animal2)

//Función contructora

function Animal(nombre, genero) {
    this.nombre = nombre
    this.genero = genero

    this.sonar = function () {
        console.log("Hago sonidos porque estoy vivo")
    }
}


//Función constructora donde asignamos los métodos al prototipo no a la función como tal

function Animal(nombre, genero) {
    this.nombre = nombre
    this.genero = genero
}
//Método agregado al prototipo de la funcion constructora

Animal.prototype.sonar = function () {
    console.log("Hago sonidos porque estoy vivo")
}



//Herencia prototípica

function Perro(nombre, genero, tamanio) {
    this.super = Animal
    this.super(nombre, genero)
    this.tamanio = tamanio
}

//Perro está heredando de Animal
Perro.prototype = new Animal()
Perro.prototype.constructor = Perro


const snoopy = new Perro("Snoopy", "Macho", "Mediano"),
    lolaBunny = new Animal("Lola Bunny", "Hembra")
console.log(snoopy)
console.log(lolaBunny)
snoopy.sonar()

//Sobreescritura del Método del prototipo padre en el hijo

Perro.prototype.sonar = function () {
    console.log("Soy un perro y mi sonido es un ladrido")
}
snoopy.sonar()
//Se agrega un método al prototipo

Perro.prototype.ladrar = function () {
    console.log("Guau Guau")
}
snoopy.ladrar()

console.log(snoopy)
