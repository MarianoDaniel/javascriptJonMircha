var hola = "Hola Mundo"
let hello = "Hello world"
console.log(hola)
console.log(hello)
console.log(window.hola)
console.log(window.hello)
console.log
    ("*********************Var************************")
//Se almacena en el objeto window
//Ambito bloque
var musica = "Rock"
console.log("Variable Música antes del bloque", musica)
//Esto es un bloque
// con var el navegador saca la variable del bloque 
{
    var musica = "Pop"
    console.log("Variable Música dentro del bloque", musica)

}
console.log("Variable Música después del bloque", musica)
console.log
    ("*********************Let************************")
//Ejemplo con let
var musica = "Rock2"
console.log("Variable Música antes del bloque2", musica)
//Esto es un bloque
{
    let musica = "Pop2"
    console.log("Variable Música dentro del bloque2", musica)

}
console.log("Variable Música después del bloque2", musica)
console.log("-----------------------------------")
console.log("*************CONST******************")
console.log("*****************Objetos Primitivos******************")
console.log("Los objetos primitivos no pueden cambiar con const")
const a = "soy un valor primitivo"
console.log("Valor de a no puede cambiar:", a)

//-----> a = "Quiero cambiar de valor y no puedo"
//lo comento porque el navegador avisa que no se puede ///cambiar una constante
console.log("*****************Objetos Compuestos******************")
//Los objetos compuestos pueden cambiar con const

const objeto = {
    nombre: "Mariano",
    apellido: "Avico"
}
console.log("Muestro un objeto guardado por const", objeto)

console.log("Le agrego un campo email")
//agrego una propiedad nueva en objeto
objeto.email = "avicomariano@gmail.com"
console.log("elemento email agregado", objeto)
console.log("esto sí está permitido porque const sigue conteniendo o haciendo referencia a un objeto, independientemente de si se agregan o se quitan las propiedades")
console.log("----------------*----------------")
console.log("Con los array pasa lo mismo")
const array = ["hola", "como", "va"]
console.log("Array", array)
console.log("Le agrego otro elemento")
array.push("todo bien")
console.log("Array con nuevo elemento", array)

console.log("*****************Objeto String******************")
let usuario = "mariano,avico,avicomariano@gmail.com"
let nombre = "Mariano"
let apellido = "Avico"
let saludo = new String("Hola mundo")
let lorem = "               Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse cursus dui in nisl pharetra vestibulum. Sed sed tempor est. In hac habitasse platea dictumst. Vestibulum luctus efficitur metus, ut congue risus imperdiet ac. Pellentesque sed nunc                interdum, facilisis nulla eu, tincidunt urna. Pellentesque blandit magna lorem, non tempor libero viverra quis. Etiam quis ligula a leo venenatis accumsan non et orci. Praesent placerat accumsan dolor, quis porta lorem sodales quis. Suspendisse id est eleifend, fringilla lacus ut, egestas lectus. Donec at dolor metus. Nunc finibus nisi id eros pretium tempor. Mauris nec dui egestas, egestas mauris vitae, elementum erat. Vestibulum id metus ac elit auctor semper sit amet eget augue.                "
console.log(nombre, apellido, saludo)
console.log(
    nombre.length + "\n" +
    apellido.length + "\n" +
    saludo.length + "\n" +
    nombre.toUpperCase() + "\n" +
    apellido.toLowerCase() + "\n" +
    "Encuentra la palabra amet en el texto de lorem: uso del lorem.includes('amet') devuelve el booleano:",
    lorem.includes("amet") + "\n" +
    "Antes del trim" + "\n" +
    lorem + "\n" +
    "Después del trim " + "\n" +
    lorem.trim() + "\n" +
    "Split: convierte una cadena de textos en array según el criterio: puede ser que quiera generar cada elemento del array en base a una ',' si por ej me llegan todos los datos de un usuario de la siguiente manera 'mariano,avico,avicomariano@gmail.com'" + "\n" +
    "resultado de usuario con usuario.split(", ")",
    usuario.split(",")
)
//Función declarada
function estoEsUnaFuncion() {
    console.log("uno")
    console.log("dos")
    console.log("tres")
}
//Invocación de función
estoEsUnaFuncion()

function unaFuncionQueDevuelveValor() {
    console.log("uno")
    console.log("dos")
    console.log("tres")
    return "La función retorna una cadena de texto"
}
let valorFuncion = unaFuncionQueDevuelveValor()
console.log(valorFuncion)

//con parámetros
function saludar(nombre = "Desconocido", edad = 0) {
    console.log(`Hola mi nombre es ${nombre} y tengo ${edad} años`)
}
/* saludar("Mariano", 34)
saludar() */

//Funciones Declaradas vs funciones Expresadas

//DECLARADAS:
//Lo primero que ordena javascript son variables y funciones, entonces va a elevar la función declarada function funcionDeclarada(){}.... siempre van a quedar abajo las llamadas
funcionDeclarada()

function funcionDeclarada() {
    console.log("Esto es una función declarada, puede invocarse en cualquier parte de nuestro código, incluso antes de que la función sea declarada")
}

//EXPRESADAS:
//Crear una función y asignarsela a una variable
//función anonima

//funcionExpresada()

const funcionExpresada = function () {
    console.log("Esto es una función expresada, es decir, una funcion que se le ha asignado como valor a una variable, si invocamos esta función antes de su definición JS nos dirá...'Cannot access 'funcionExpresada' before initialization'")
}
funcionExpresada()
console.log("*****************Array ******************")
const array1 = Array.of("x", "y", "z", 9, 8, 7)
console.log(array1)
//llena todos los campos con true en este caso  
const d = Array(10).fill(true)

const colores = ["rojo", "verde", "azul"]

colores.forEach((el, index) => {
    console.log(`<li id=${index}>${el}</li>`)
})

