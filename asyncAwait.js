/**
 * Funciones asincronas, van a esperar a que algo termine para seguir ejecutando el proceso
 */

function cuadradoPromise(value) {
    if (typeof value !== "number") return Promise.reject(`Error: el valor ${value} no es un número`)
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve({
                value,
                result: value * value
            })
        }, 1000);
    })
}

async function funcionAsincronaDeclarada() {
    try {
        console.log("inicio Async Function")
        let obj = await cuadradoPromise(0)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(1)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(2)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise("3")
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(4)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(5)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)


    } catch (error) {
        console.error(error)
    }
}
funcionAsincronaDeclarada()

const funcionAsincronaExpresada = async () => {
    try {
        console.log("inicio Async Function")
        let obj = await cuadradoPromise(6)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(7)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise("8")
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(9)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(10)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)
        obj = await cuadradoPromise(11)
        console.log(`Async Function: ${obj.value}, ${obj.result}`)


    } catch (error) {
        console.error(error)
    }
}
funcionAsincronaExpresada()

function sumaPromise(valor) {
    if (typeof valor != Number) Promise.reject(`Error: ${valor} no es un número`)
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve({
                valor,
                result: valor + valor
            })
        }, 1000);
    })
}

async function usaPromesaSuma() {
    try {
        let suma = await sumaPromise(5)
        console.log(`contenido de la promesa: Valor ${suma.valor}, resultado ${suma.result}`)
        suma = await sumaPromise(6)
        console.log(`contenido de la promesa: Valor ${suma.valor}, resultado ${suma.result}`)
        suma = await sumaPromise(7)
        console.log(`contenido de la promesa: Valor ${suma.valor}, resultado ${suma.result}`)
    } catch (error) {

    }

}

usaPromesaSuma()