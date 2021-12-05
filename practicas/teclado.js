const d = document
let x = 0,
    y = 0;
export function moveBall(e, ball, stage) {
    const $ball = d.querySelector(ball),
        $stage = d.querySelector(stage),
        //Colisiones
        limitsBall = $ball.getBoundingClientRect(),
        limitStage = $stage.getBoundingClientRect();


    //función que va a recibir la dirección y en base a eso se toman las decisiones


    switch (e.keyCode) {
        case 37:
            if (limitsBall.left > limitStage.left) {
                e.preventDefault()
                x--
            }

            break;
        case 38:
            if (limitsBall.top > limitStage.top) {
                e.preventDefault()
                y--
            }


            break;
        case 39:
            if (limitsBall.right < limitStage.right) {
                e.preventDefault()
                x++
            }

            break;
        case 40:
            if (limitsBall.bottom < limitStage.bottom) {
                e.preventDefault()
                y++
            }

            break;

        default:
            break;

    }
    $ball.style.transform = `translate(${x * 10}px, ${y * 10}px)`

}

/* export function shortcuts(e) {
    console.log(e.type)
    console.log(e.key)
    console.log(e.keyCode)
    console.log(`ctrl: ${e.ctrlKey}`)
    console.log(`alt: ${e.altKey}`)
    console.log(`shift: ${e.shiftKey}`)
    console.log(e)

    if (e.key === "a" && e.altKey) {
        alert("Haz lanzado una alerta con el Teclado")
    }
    if (e.key === "c" && e.altKey) {
        confirm("Haz lanzado una confirmación con el Teclado")
    }
    if (e.key === "p" && e.altKey) {
        prompt("Haz lanzado un aviso con el Teclado")
    }
} */