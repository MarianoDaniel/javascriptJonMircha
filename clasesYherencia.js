console.log("********************************************")
console.log("**************Clases y Herencia*********")

class Animal {
    constructor(nombre, genero) {
        this.nombre = nombre
        this.genero = genero
    }

    sonar() {
        console.log("Hago sonidos por que estoy vivo")
    }

    saludar() {
        console.log(`Hola me llamo ${this.nombre}`)
    }
}

const raton = new Animal("Splinter", "Macho"),
    perro = new Animal("Cuajinais", "Macho")

console.log(raton)
console.log(perro)

class Perro extends Animal {
    constructor(nombre, genero, tamanio) {
        super(nombre, genero)
        this.tamanio = tamanio
    }
    sonar(){
        console.log("Soy un perro y mi sonido es un ladrido")
    }
    ladrar(){
        console.log("Guauu Guauuu")
    }

//Un método estático se puede ejecutar sin necesidad de instanciar la clase

static queEres(){
    console.log("Soy el amigo del hombre")
}
}

const perro2 = new Perro("Scooby","Macho","Gigante")
console.log(perro2)
perro2.ladrar()
perro2.sonar() 
