const d = document,
    w = window;
export default function smartVideo() {
    const $videos = d.querySelectorAll("video[data-smart-video]")
    const cb = (entries) => {
        entries.forEach(entry => {
            //acordate que para conseguir la etiqueta video tenes que ir a target. Ya que el observable se lo asignaste a esa etiqueta y por lo tanto a ella es a quien el observable hacer referencia. 
            //console.log(entry)
            if (entry.isIntersecting) {
                entry.target.play() //Métodos y propiedades https://www.w3schools.com/tags/ref_av_dom.asp
            } else {
                entry.target.pause()
            }
            w.addEventListener("visibilitychange", e => {
                //en este caso target hace referencia a document por eso puedo acceder a la propiedad visibilityState, también podría usar directamente d.visibilityState
                e.target.visibilityState === "hidden"
                    ? entry.target.pause()
                    : entry.target.play()
            })
        })
    }

    const observer = new IntersectionObserver(cb, { threshold: 0.5 })
    $videos.forEach(v => observer.observe(v))
}