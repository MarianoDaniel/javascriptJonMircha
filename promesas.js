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

cuadradoPromise(5)
    .then(obj => {
        //console.log(obj)
        console.log(`Promise: ${obj.value}, ${obj.result}`)
        return cuadradoPromise(obj.result)
    }).then(obj2 => {
        console.log(`Promise2: ${obj2.value}, ${obj2.result} `)
    })
    .catch(err => console.error)




//Ejemplo de libro
/* var promise = step1()
    .then(function (value1) {
        return step2(value1);
    })
    .then(function (value2) {
        return step3(value2);
    })
    .then(function (value3) {
        return step4(value3);
    })
    .then(function (value4) {
        // Procesamiento cuando la ejecución de las cuatro funciones
        // asíncronas ha terminado
    }); */