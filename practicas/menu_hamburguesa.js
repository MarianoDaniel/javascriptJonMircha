export default function hamburguerMenu(panelBtn, panel, menuLink) {
    //Utilizamos delegación de eventos para evitar la propagación
    const d = document
    d.addEventListener("click", e => {
        //le agregamos un operador o con el botón más * (como se hace en css) para que contemple todo el tontenido del botón también. Esto es porque no puedo sino apretar todo el botón, solo los bordes que corresponden a el omitiendo lo de adentro.
        if (e.target.matches(panelBtn) || e.target.matches(`${panelBtn} *`)) {
            //si machea le tengo que agregar la clase is-active para que active el panel
            d.querySelector(panel).classList.toggle("is-active")
            d.querySelector(panelBtn).classList.toggle("is-active")

        }
        if (e.target.matches(menuLink)) {
            //Le saca las clases una vez que me lleva a la sección elegída. Esto quita el panel. 
            d.querySelector(panel).classList.remove("is-active")
            d.querySelector(panelBtn).classList.remove("is-active")
        }
    })
}