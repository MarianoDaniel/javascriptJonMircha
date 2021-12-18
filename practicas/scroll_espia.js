const d = document
export default function scrollSpy() {
    const $sections = d.querySelectorAll("section[data-scroll-spy]")
    const cb = (entries) => {
        //console.log("Entries", entries)
        entries.forEach(entry => {
            const id = entry.target.getAttribute("id")
            if (entry.isIntersecting) {
                d.querySelector(`a[data-scroll-spy][href="#${id}"]`).
                    classList.add("active")
            } else {
                d.querySelector(`a[data-scroll-spy][href="#${id}"]`).
                    classList.remove("active")
            }
        })
    }
    const observer = new IntersectionObserver(cb, {
        //root la omitimos y toma por defecto el document
        //root margin reducimos o aumentamos el area de interacción, en este caso necesitamos reducirla para que no toque los section cercanos
        //rootMargin:"-250px"
        //Hasta que tenemos el 50 por ciento de la visualización o entre minimos y máximos, este caso que se vea entre el 50 y el 75 por ciento
        threshold:[0.5,0.75],
    })
    $sections.forEach(el => observer.observe(el))
}