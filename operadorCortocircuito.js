console.log("********************************************")
console.log("**************Operador cortocircuito*********")
//nueva forma
/* function saludar(nombre = 'desconocido'){
    console.log(`Hola ${nombre}`)
} */
//forma antigua, se usa todavía
function saludar(nombre ){
    nombre = nombre || 'desconocido'
    console.log(`Hola ${nombre}`)
}
function saludar2(nombre ){
    nombre = nombre  && 'desconocido'
    console.log(`Hola ${nombre}`)
}


saludar("Mariano")
saludar()
saludar2("Mariano")
saludar2()