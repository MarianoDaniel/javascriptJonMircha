const d = document,
    n = navigator;
export default function webCam(id) {
    const $video = d.getElementById(id)
    if (n.mediaDevices.getUserMedia) {
        n.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(strem => {
                console.log(strem)
                //con srcObject le puedo pasar el objeto entero a la etiqueta, pero si yo nada mas lo dejo así al momento que se prende la camara solo queda una foto... si quiero que el video se vea hay que ejecutare el método play
                $video.srcObject = strem
                $video.play()
            }).catch(err => console.log(`Sucedió un error! ${err}`))
    }
}