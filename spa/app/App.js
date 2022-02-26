import { Header } from "./components/Header.js";
import { Loader } from "./components/Loader.js";
import { Main } from "./components/Main.js";
import { Router } from "./components/Router.js";
import { infiniteScroll } from "./helpers/infinite_scroll.js";

export function App() {
    const d = document,
        $root = d.getElementById("root");
    $root.textContent = null;
    $root.appendChild(Header());
    $root.appendChild(Main());
    $root.appendChild(Loader());

    Router();
    infiniteScroll();
}

