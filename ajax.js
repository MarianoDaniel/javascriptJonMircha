//Función anonima auto ejecutable,pequños modulos en javascript. Vamos a encapsular el código que corresponda con cada objeto (fetch, XMLHttpRequest)
//XMLHttpRequest
(() => {
    //1- lo instancio
    const xhr = new XMLHttpRequest(),
        $xhr = document.getElementById("xhr"),
        $fragment = document.createDocumentFragment();

    //le agrego un avento
    xhr.addEventListener("readystatechange", e => {
        if (xhr.readyState != 4) return
        if (xhr.status >= 200 && xhr.status < 300) {
            //convertimos la respuesta a JSON
            let json = JSON.parse(xhr.responseText)
            json.forEach(element => {
                const $li = document.createElement("li")
                $li.innerHTML = `${element.name} -- ${element.email} -- ${element.phone}`
                $fragment.appendChild($li)
            });
            $xhr.appendChild($fragment)
        } else {
            console.log("Error")
            let message = xhr.statusText || "Ocurrió un error"
            $xhr.innerHTML = `Error ${xhr.status}: ${message}`
        }

    })
    //le digo con qué método y a que URL voy a hacer la petición
    //xhr.open("GET", "https://jsonplaceholder.typicode.com/users")
    xhr.open("GET", "/users.json")
    //envío la petición
    xhr.send()
})();
//FETCH
(() => {
    const $fetch = document.getElementById("fetch"),
        $fragment = document.createDocumentFragment();
    fetch("https://jsonplaceholder.typicode.com/users")
        //al mandarle la promesa va a funcionar el catch
        .then((res) => res.ok ? res.json() : Promise.reject(res))
        .then(json => {
            //capturo el body
            //console.log(json)
            json.forEach(element => {
                const $li = document.createElement("li")
                $li.innerHTML = `${element.name} -- ${element.email} -- ${element.phone}`
                $fragment.appendChild($li)
            });
            $fetch.appendChild($fragment)
        })
        .catch(err => {
            let message = err.statusText || "Ocurrió un error"
            $fetch.innerHTML = `Error ${err.status}: ${message}`
        })
        .finally(() => console.log("Esto se va a ejecuter independientemente de la respuesta de la promesa Fetch"))
})();
//FETCH + ASYNC AWAIT
(() => {
    const $fetchAsync = document.getElementById("fetch-async"),
        $fragment = document.createDocumentFragment();

    async function getData() {
        try {
            let res = await fetch("https://jsonplaceholder.typicode.com/users")
            json = await res.json()
            //if(!res.ok) throw new Error("Ocurrió un Error al solicitar los datos")
            if (!res.ok) throw { status: res.status, statusText: res.statusText }
            json.forEach(element => {
                const $li = document.createElement("li")
                $li.innerHTML = `${element.name} -- ${element.email} -- ${element.phone}`
                $fragment.appendChild($li)
            });
            $fetchAsync.appendChild($fragment)
        } catch (err) {
            //console.log(err)
            let message = err.statusText || "Ocurrió un error"
            $fetchAsync.innerHTML = `Error ${err.status}: ${message}`
        } finally {

        }
    }
    getData()
})();
//AXIOS
(() => {
    const $axios = document.getElementById("axios"),
        $fragment = document.createDocumentFragment();

    axios.get("https://jsonplaceholder.typicode.com/users")
        .then(res => {
            //console.log(res)
            let json = res.data
            json.forEach(element => {
                const $li = document.createElement("li")
                $li.innerHTML = `${element.name} -- ${element.email} -- ${element.phone}`
                $fragment.appendChild($li)
            });
            $axios.appendChild($fragment)
        })
        .catch((err) => {
            console.log(err)
            //error.response propiedad que otorga axios para observar el estado
            let message = err.response.statusText || "Ocurrió un error"
            $axios.innerHTML = `Error ${err.response.status}: ${message}`
        })
        .finally(() => { "Esto se va a ejecuter independientemente del resultado de Axios" })
})();
//AXIOS + ASYNC AWAIT
(() => {
    const $axiosAsync = document.getElementById("axios-async"),
        $fragment = document.createDocumentFragment();
    async function getData() {
        try {
            let res = await axios.get("https://jsonplaceholder.typicode.com/users"),
                json = res.data;
            console.log(json)
            json.forEach(el => {
                const $li = document.createElement("li")
                $li.innerHTML = `${el.name} -- ${el.email} -- ${el.phone}`
                $fragment.appendChild($li)
            })
            $axiosAsync.appendChild($fragment)
        } catch (err) {
            let message = err.response.statusText || "Ocurrió un error"
            $axiosAsync.innerHTML = `Error ${err.response.status}: ${message}`
        } finally {

        }
    }
    getData()
})();