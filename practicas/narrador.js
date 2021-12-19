const d = document,
    w = window;

export default function speechReader() {
    const $speechSelect = d.getElementById("speech-select"),
        $speechTextarea = d.getElementById("speech-text"),
        $speechBtn = d.getElementById("speech-btn"),
        speechMessage = new SpeechSynthesisUtterance

    let voices = []

    d.addEventListener("DOMContentLoaded", e => {
        //es necesario agregarle el evento voiceschanged a speechSynthesis para poder utilizar el getVoices()
        w.speechSynthesis.addEventListener("voiceschanged", e => {
            //Le cargo las voces
            voices = w.speechSynthesis.getVoices()
            voices.forEach(v => {
                const $option = d.createElement("option")
                $option.value = v.name
                $option.textContent = `${v.name} - ${v.lang}`
                $speechSelect.appendChild($option)

            })
        })
    })
    //este evento es para cargar en el campo voice de speechMessage, la elegida en el select. Esto es porque hay que definir con qué vos va a hablar el programa.
    d.addEventListener("change", e => {
        if (e.target === $speechSelect) {
            speechMessage.voice = voices.find(voice => voice.name === e.target.value)
            //console.log(speechMessage)
        }
    })
    d.addEventListener("click", e => {
        if (e.target === $speechBtn) {
            speechMessage.text = $speechTextarea.value
            w.speechSynthesis.speak(speechMessage)
        }
    })
}