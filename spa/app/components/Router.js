import { api } from "../helpers/wp_api.js";
import { ajax } from "../helpers/ajax.js"
import { PostCard } from "./PostCard.js";
import { Post } from "./Post.js";
import { SearchCard } from "./SearchCard.js";
import { ContactForm } from "./ContactForm.js";

const API = api();
export async function Router() {
    const d = document,
        w = window,
        $main = d.getElementById("main");
    let { hash } = location;
    $main.innerHTML = null;
    if (!hash || hash === "#/") {
        await ajax({
            url: API.POST,
            cbSuccess: (posts) => {
                console.log(posts)
                let html = "";
                posts.forEach(post => html += PostCard(post));
                $main.innerHTML = html;
            }
        })

    } else if (hash.includes("#/search")) {
        let query = localStorage.getItem("wpSearch");
        if (!query) {
            document.querySelector(".loader").style.display = "none"
        };
        await ajax({
            url: `${API.SEARCH}${query}`,
            cbSuccess: (search) => {
                console.log(search)
                let html = "";
                if (search.length === 0) {
                    html = `
                    <p class="error">
                    No esxisten resultados de búsqueda para el término
                    <mark>${query}</mark>
                    </p>
                    `
                } else {
                    search.forEach(post => html += SearchCard(post))
                }
                $main.innerHTML = html;

            }
        })

    } else if (hash === "#/contacto") {
        $main.appendChild(ContactForm())
    } else {
        $main.innerHTML = "<h2>Acá va a cargar el contenido del Post previamente seleccionado</h2>"
        await ajax({
            url: `${API.POST}/${localStorage.getItem("wpPostId")}`,
            cbSuccess: (post) => {
                console.log(post)
                $main.innerHTML = Post(post)

                /*   let html = "";
                  posts.forEach(post => html += PostCard(post));
                  $main.innerHTML = html; */
            }
        })
    }
    d.querySelector(".loader").style.display = "none";

}