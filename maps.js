//Map son objetos que nos sierven para almacenar valores asociados. Es muy parecido a un objeto primitivo, se usa como una colección de datos que están relacionados entre sí.
//No es un objeto primitivo, es un objeto iterador
//Son objetos que nos permiten tener colecciones llave valor
//*pero la diferencia es que podemos generar una llave con cualquier tipo 


let mapa = new Map() 

//Agregar valores ---> llave valor

mapa.set("nombre","mariano")
mapa.set("apellido", "avico")
mapa.set("edad", 34)

console.log(mapa)

console.log(mapa.size)
console.log(mapa.has("correo"))
console.log(mapa.has("nombre"))
console.log(mapa.get("nombre"))

//Sobreescribir valores

mapa.set("nombre","Daniel")

console.log(mapa)

//Borrar valores

mapa.delete("apellido")
console.log(mapa)


//* le escribo claves que no sean cadena de texto

mapa.set(19,"diecinueve")
mapa.set(false,"falso")
mapa.set({},{})
console.log(mapa)
//Se debe convertir en array para iterarlo
let mapaToArray = Array.from(mapa)
console.log("mapa to array", mapaToArray)

for(let [key,value] of mapa){
    //[key,value] es destructiración
    console.log(`llave: ${key}, valor: ${value}`)
}

const mapa2 = new Map([
    ["nombre","malena"],
    ["edad","infinito"],
    ["animal", "perro"],
    [null,"nulo"]
])

console.log(mapa2)

//en una lista las llaves en otras los valores

const llavesMapa2 = [...mapa2.keys()]
const valoresMapa2 = [...mapa2.values()]

console.log(llavesMapa2)
console.log(valoresMapa2)