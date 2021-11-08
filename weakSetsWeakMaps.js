//hermanos pequeños del map y del set
//solamente pueden almacenar referencias débiles, es decir, las llaves deven ser de tipo objeto. No son iterables, no se puede borrar todo de un tirón (no se puede usar el clear), tampoco podemos verificar su tamaño.(no tiene len ni size) Los recolecta el recolector del navegador una vez que son utilizados

/* const ws = new WeakSet()

let valor1 = { valor1: 1 }
let valor2 = { valor2: 2 }
let valor3 = { valor3: 3 }

ws.add(valor1)
ws.add(valor2)
console.log(ws)
console.log(ws.has(valor1))
console.log(ws.has(valor3))
ws.delete(valor2)
ws.add(valor3)
ws.add(valor2) */

/* 
setInterval(() => {
    console.log(ws)
}, 1000); */

//luego de 5 segundos, cuando los valores son nulos, el garbaje colector del navegador los borra de la memoria y ya no aparecen en el console del interval
/* setTimeout(() => {
    valor1 = null
    valor2 = null
    valor3 = null
    console.log(valor1)
}, 5000); */


//WeakMap

//Esto acá no se puede hacer como en el map común, tiene que ser de tipo objeto
/* const wm = new WeakMap([
    ["nombre", "MaLeNa"],
    ["edad","infinito"],
    ["animal","perro"],
    [null,"nulo"]

]) */


/* // Execute a callback on everything stored inside an object
function execRecursively(fn, subject, _refs = null){
  if(!_refs)
    _refs = new WeakSet();

  // Avoid infinite recursion
  console.log(_refs)
  if(_refs.has(subject))
    return;

  fn(subject);
  if("object" === typeof subject){
    _refs.add(subject);
    for(let key in subject)
      execRecursively(fn, subject[key], _refs);
  }
}

const foo = {
  foo: "Foo",
  bar: {
    bar: "Bar"
  }
};

foo.bar.baz = foo; // Circular reference!
execRecursively(obj => console.log(obj), foo); */

const wm = new WeakMap()
let llave1 = {}
let llave2 = {}
let llave3 = {}

wm.set(llave1,1)
wm.set(llave2,2)
console.log(wm)

console.log(wm.has(llave3))
console.log(wm.has(llave2))

console.log(wm.get(llave3))
console.log(wm.get(llave2))