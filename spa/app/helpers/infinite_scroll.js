import { PostCard } from "../components/PostCard.js";
import { SearchCard } from "../components/SearchCard.js";
import { ajax } from "./ajax.js";
import { api } from "./wp_api.js";
const API = api()
export async function infiniteScroll() {
    const d = document,
        w = window;
    let query = localStorage.getItem("wpSearch"),
        apiURL,
        Component;

    w.addEventListener("scroll", async e => {
        let { scrollTop, clientHeight, scrollHeight } = d.documentElement, //de acá saco el alto y el ancho para detecta cuando llego al final de la página
            { hash } = w.location;

        /*  console.log(scrollTop, clientHeight, scrollHeight, hash) */

        if (scrollTop + clientHeight >= scrollHeight) {
            API.page++;
            if (!hash || hash === "#/") {
                apiURL = `${API.POSTS}$page=${API.page}`;
                Component = PostCard;
            } else if (hash.includes("#/search")) {
                apiURL = `${API.SEARCH}${query}&page=${API.page}`
                Component = SearchCard;

            }
        } else {
            return false;
        }
        d.querySelector(".loader").style.display = "block"

        await ajax({
            url: apiURL,
            cbSuccess: (posts) => {
                let html = "";
                posts.forEach(post => html += Component(post));
                d.getElementById("main").insertAdjacentHTML("beforeend", html)
                d.querySelector(".loader").style.display = "none"
            }
        })
    })
}