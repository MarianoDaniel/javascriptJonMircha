//Mecanismo que te permite crear un objeto basado en un objeto literal inicial

//En vez de utilizar clases utilizo un objeto literal

//el proxi recibe el objeto literal y va a realizar una copia que va a permitir la realización de ciertas operaciones como validaciones de propiedades o tipos de datos dentro de la copia del objeto inicial
//Es un medio de vinculación   entre el objeto y la nueva instancia y todo eso se administra a través de un objeto especial que tiene el proxi que se llama handler 


//Objeto literal 

const persona = {
    nombre: "",
    apellido: "",
    edad: 0
}

const manejador = {
    // En este método podemos establecer las validaciones
    set(obj,prop,valor){  
        console.log(obj)
        if (Object.keys(obj).indexOf(prop) === -1){
            return console.error(`La propiedad "${prop}" no existe en el objeto persona`)
        }  
        
        obj[prop] = valor    

    }
}
const mariano = new Proxy(persona, manejador)
mariano.nombre = "Mariano"
mariano.apellido = "Avico"
mariano.edad = 34
mariano.twitter = "@mariano"

// Se vincula con el objeto de origen y le agrega propiedades, pero se puede validar en el objeto manejador para que esto y otras cosas más no pasen
console.log(persona)