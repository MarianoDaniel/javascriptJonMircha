console.log("Ejercicios")

function cuentaLetras(texto) {
    valor = 0
    for (elemento of texto) {
        valor++
    }
    return valor
}

/* resultado = cuentaLetras("Hola")
console.log(resultado) */

function recortaTextoSegunNumero(texto, numero) {
    let i = 0
    let txt = ""
    for (const el of texto) {
        i++
        if (i <= numero) {
            txt +=el
        }

    }
    console.log(txt)
}
recortaTextoSegunNumero("hola",4)

