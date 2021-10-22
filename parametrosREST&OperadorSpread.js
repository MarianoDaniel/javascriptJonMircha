console.log("********************************************")
console.log("**************REST Spread Operator*********")

//REST: forma de agregar parametros infinitos... cuando uno no sabe cuantos parámetro va a recibir


function sumar(a, b, ...c) {
    let resultado = a + b

    c.forEach(element => resultado += element)
    return resultado;
}

console.log(sumar(1, 2))
console.log(sumar(1, 2, 3))
console.log(sumar(1, 2, 3, 4))

//Spread Operator: 

const arr1 = [1, 2, 3, 4, 5]
const arr2 = [6, 7, 8, 9]

const arr3 = [...arr1, ...arr2]
console.log(arr3)