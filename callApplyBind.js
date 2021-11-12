this.lugar = "Contexto Global"

function saludar(saludo, aQuien) {
    console.log(`${saludo} ${aQuien} desde el ${this.lugar}`)
}

saludar("Qué tal", "Daniel")

const obj = {
    lugar: "Contexto Objeto"
}

saludar.call(obj, "Hola", "Mariano")
saludar.apply(obj, ["Adiós", "Mariano"])

this.nombre = "Windows"

const persona = {
    nombre: "Mariano",
    saludar:function(){
        console.log(`Hola ${this.nombre}`)
    }
}

persona.saludar()

const otraPersona = {
    saludar:persona.saludar.bind(persona)
}
otraPersona.saludar()