//Tipo de dato similar a un array pero de datos unicos. Osea, no hacepta duplicados de tipos nativos... objetos y array se le pueden pasar muchos porque cada uno de ellos tiene una referencia distinta.

const set = new Set([1, 2, 3, 3, 4, 5, true, false, false, {}, {}, "hola", "HOLa"])
console.log(set)
console.log(set.size)


const set2 = new Set()

set2.add(1)
set2.add(2)
set2.add(2)
set2.add(3)
set2.add(true)
set2.add(false)
set2.add(true)
set2.add({})
set2.add({})
set2.add([])
set2.add([])

console.log(set2.size)
console.log(set2)

const arr = [1,2,3,4,4,4,5,6,7,7,8]

const set3 = new Set(arr)

console.log(set3)
console.log("Recorriendo set")

for (item of set){
    console.log(item)
}


console.log("Recorriendo set 2")

set2.forEach(item => console.log(item))

//para ver la posición tenemos que convertirlo en un arreglo

let setToArray = Array.from(set)
console.log(setToArray)
console.log(setToArray[0])
console.log(setToArray[1])

//Método set para eliminar valores

set.delete("HOLa")

console.log(set)

//Metodo has que comprueba si el valor existe dentro de la colección de datos


console.log(set.has("hola"))
console.log(set.has(19))

set2.clear()

console.log(set2)

//Este tipo de dato podría servir por ej, si estás creando un catalogo de películas unicas...ya que no guardan repetidas (siempre y cuando sean datos nativos) o en una base de datos de correos electrónicos en la verificación de un usuario