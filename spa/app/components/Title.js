import { api } from "../helpers/wp_api.js"
export function Title() {
    let API = api()
    const $h1 = document.createElement("h1");
    $h1.innerHTML = `
    <a href="${API.DOMAIN}" target="_blank" rel="noopener">
    ${API.NAME.toUpperCase()}
    </a>
    
    `
    return $h1
}