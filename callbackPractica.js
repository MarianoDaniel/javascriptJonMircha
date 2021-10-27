function callbackSuma(value, callback) {
    setTimeout(() => { callback(value, value + value) }, 1000)
}

callbackSuma(5, (value, result) => {
    console.log(`Callback --> value: ${value} result: ${result} `)
    callbackSuma(6, (value, result) => {
        console.log(`Callback --> value: ${value} result: ${result} `)
        callbackSuma(7, (value, result) => {
            console.log(`Callback --> value: ${value} result: ${result} `)
            callbackSuma(8, (value, result) => {
                console.log(`Callback --> value: ${value} result: ${result} `)
                callbackSuma(9, (value, result) => {
                    console.log(`Callback --> value: ${value} result: ${result} `)
                })
            })
        })
    })
})