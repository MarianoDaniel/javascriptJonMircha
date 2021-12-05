const d = document,
    w = window;

export default function responsiveMedia(id, mq, mobileContent, desktopContent) {
    let brackpoint = w.matchMedia(mq)
    const responsive = e => {
        if (e.matches) {
            d.getElementById(id).innerHTML = desktopContent
        }else{
            d.getElementById(id).innerHTML = mobileContent 

        }
    }
    brackpoint.addEventListener('change', responsive)
    //para que tome los cambios ni bien carga la página
    responsive(brackpoint)
}