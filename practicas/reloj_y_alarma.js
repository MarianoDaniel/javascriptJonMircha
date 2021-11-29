//Solo se puede tener una función por default, si quiero más las tengo que declarar primero y exportar después. 
export function relojYalarma(btnIniciar, btnDetener, panelRelojTexto, panelReloj) {
    const d = document
    d.addEventListener("click", e => {
        const panel = document.querySelector(panelReloj)
        const $btnInicio = document.querySelector(btnIniciar)
        if (e.target.matches(btnIniciar)) {
            panel.hidden = false
            $btnInicio.disabled = true
            setInterval(() => {
                const date = new Date().toLocaleTimeString()
                document.querySelector(panelRelojTexto).innerHTML = `<h3>${date}</h3>`
            }, 1000);
        }
        if (e.target.matches(btnDetener)) {
            $btnInicio.disabled = false
            panel.hidden = true
        }
    })

}
export function alarm(sound, btnPlay, btnStop) {
    const doc = document
    let alarmTempo;
    const $alarm = doc.createElement("audio")
    $alarm.src = sound
    doc.addEventListener("click", e => {
        if (e.target.matches(btnPlay)) {
            //Me lo guardo en una variable para después poder cancelarlo, por eso la declaro afuera, para poder cancelarla en el if de abajo
            alarmTempo = setTimeout(() => {
                $alarm.play()
            }, 2000);
            e.target.disabled = true
        }
        if (e.target.matches(btnStop)) {
            clearTimeout(alarmTempo)
            $alarm.pause()
            //la alarma vuelve a 0
            $alarm.currentTime = 0
            doc.querySelector(btnPlay).disabled = false
        }
    })
}
