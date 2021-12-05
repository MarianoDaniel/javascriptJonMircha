const d = document
export default function responsiveTester(form) {
    const $form = d.getElementById(form)
    //me guardo la referencia de la ventana window.open
    let tester

    d.addEventListener("submit", e => {
        //otra forma de ver quien generó el evento
        if (e.target === $form) {
            e.preventDefault()
            //Se puede acceder a las etiquetas que tiene el formulario adentro a través del punto y luego el nombre del atributo name ---> en este caso direccion. Posteriormente, como yo quiero el valor y no la etiqueta, le agrego el .value
            //Le paso el alto y el ancho de la misma manera que el parámetro direccion
            tester = window.open($form.direccion.value, "tester", `innerWidth=${$form.ancho.value}, innerHeight=${$form.alto.value}`)
        }
    })
    d.addEventListener("click", e => {
        if (e.target === $form.cerrar) tester.close()
    })
}