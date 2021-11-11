console.log(this)
console.log(window)
console.log(this === window)

this.nombre = "Contexto Global"
console.log(this.nombre)

function imprimir() {
    console.log(this.nombre)
}
imprimir()

const obj = {
    nombre: "Contexto Objeto",
    imprimir: function () {
        console.log(this.nombre)
    }
}

obj.imprimir()

const obj2 = {
    nombre: "Contexto Objeto 2",
    imprimir
}

obj2.imprimir()

const obj3 = {
    nombre: "Contexto Objeto 3",
    imprimir: () => {
        console.log(this.nombre)
    }
}
//la arrow function apunta al objeto global, mantiene un enlace del contexto en el que ha sido creado el objeto donde aparece. La arrow function no maneja su propio scope 
obj3.imprimir()

function Persona(nombre) {
    this.nombre = nombre;

/*     return function () {
        console.log(this.nombre)
    } */
    
    return () => console.log(this.nombre)

}

const p = new Persona("Mariano")
//Como las function crean su propio scope no encuentra a la propiedad nombre y se va a buscarla en el contexto padre, en este caso el objeto window. devolviendo "contexto global"
p()