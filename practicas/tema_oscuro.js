const d = document
export default function darkTheme(btn, classDark) {
    let localS = localStorage.getItem("theme")
    const $themeBtn = d.querySelector(btn),
        $selectors = d.querySelectorAll("[data-dark]");//corchetes para apuntar a un data-atribute
    //Me guardo los emojis en variables para poder compararlos en el if
    let moon = "🌙",
        sun = "🌞";
        //cuando carga me fijo en el localStorage si ya tiene el theme moon
        if (localS === "dark-mode") {
            //recorro el nodo y le agrego la clase dark a todos los elementos seleccionados
            $selectors.forEach(el => {
                console.log(el)
                el.classList.add(classDark)
            })
            $themeBtn.textContent = sun
        }
    //Delegación de eventos --> va al document y después evaluo con if
    d.addEventListener("click", e => {
        if (e.target.matches(btn)) {
            console.log($themeBtn.textContent)
            //con texContent miro el contenido de la etiqueta para poder preguntar en el if 
            if ($themeBtn.textContent === moon) {
                //recorro el nodo y le agrego la clase dark a todos los elementos seleccionados
                $selectors.forEach(el => {
                    console.log(el)
                    el.classList.add(classDark)
                })
                $themeBtn.textContent = sun
                localStorage.setItem("theme", "dark-mode")
            } else {
                $selectors.forEach(el => {
                    el.classList.remove(classDark)
                })
                $themeBtn.textContent = moon
                localStorage.setItem("theme", "")


            }
        }
    })


}