//JSON : JavaScript Object Notation. Es un formato ligero de intercambio de datos
//https://www.json.org/json-es.html
console.log(JSON)
//parse convierte un json a objeto js
console.log(JSON.parse("{}"))
console.log(JSON.parse("[1,2,3]"))
console.log(JSON.parse("true"))
console.log(JSON.parse("false"))
console.log(JSON.parse("19"))
//console.log(JSON.parse("'Hola Mundo'"))
//console.log(JSON.parse("undefined"))
console.log(JSON.parse("null"))
//convierte un obj js a json
console.log(JSON.stringify({}))
console.log(JSON.stringify({x:2,y:3}))