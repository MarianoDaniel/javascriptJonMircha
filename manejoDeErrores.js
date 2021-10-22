console.log("********************************************")
console.log("***********Manejo de errores*********")

try {
    console.log("En el try se agrega el código a evaluar")
    noExiste;
    console.log("Segundo mensaje en el try")
} catch (error) {
    console.log("Captura cualquier error surgido o lanzado en el try", error)

} finally {
    console.log("finally se ejecuta siempre al final de un bloque try-catch")
}

console.log("********************************************")

//Personalizar mensajes de error

try {
    let numero = 10
    if (isNaN(numero)) {
        throw new Error("el caractér introducido no es un número")
    }
    console.log(numero * numero)
} catch (error) {
    console.log(`Se produjo el siguiente error: ${error}`)
}