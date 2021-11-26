//BOM: Métodos

//window.alert("Alerta")
//window.confirm("Confirmación")
//window.prompt("Aviso")
//alert("Alerta")
//confirm("Confirmación")
//prompt("Aviso")

const $btnAbrir = document.getElementById("abrir-ventana"),
    $btnCerrar = document.getElementById("cerrar-ventana"),
    $btnImprimir = document.getElementById("imprimir-ventana")

let ventana;
$btnAbrir.addEventListener("click", e => {
    ventana = open("https://jonmircha.com")
    console.log(ventana)
})
$btnCerrar.addEventListener("click", e => {
    ventana.close()
})
$btnImprimir.addEventListener("click", e => {
    window.print()
})
