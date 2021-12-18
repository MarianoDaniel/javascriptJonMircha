const d = document,
    n = navigator;
export default function getGeolocation(id) {
    const $id = d.getElementById(id),
        //enableHighAccuracy acelera hardware para tener una mejor lectura
        //maximunAge para que no se guarde en caché. Para que cuando busque no tenga como referencia la anterior
        options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximunAge: 0
        };
    const success = (position) => {
        let coords = position.coords
        $id.innerHTML = `
        <p>Tu posición actual es:</p>
        <ul>
            <li>Latitud: <b>${coords.latitude}</b></li>
            <li>Longitud: <b>${coords.longitude}</b></li>
            <li>Precisión: <b>${coords.accuracy}</b> Metros</li>            
        </ul>
        <a href="https://www.google.com/maps/@${coords.latitude},${coords.longitude},20z" target="_blank" rel="noopener">Ver en Google Maps</a>
        `
    }

    const error = (err) => {
        $id.innerHTML = `<p><mark>Error code ${err.code}: ${err.message}</mark></p>`
        console.log(`Error code ${err.code}: ${err.message}`)
    }

    n.geolocation.getCurrentPosition(success, error, options)
}