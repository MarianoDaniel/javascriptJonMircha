import { App } from "./App.js";
import {api} from "./helpers/wp_api.js"
let API = api()
document.addEventListener("DOMContentLoaded", App)
window.addEventListener("hashchange", () => {
    API.page = 1;
    App();
})