
//interface especial a la que podemos acceder siempre que el dato sea iterable.
 
const iterable = [22,33,55,66,77,88,99] //"hola mundo" tambien es un iterable y el iterador es de tipo string
//Accedemos al iterador del iterable
const iterador = iterable[Symbol.iterator]()

console.log(iterable)
console.log(iterador)
//console.log(iterador.next()) // next devuelve un objeto: {value: 1, done: false} el primer valor del array y el "done: flase" significa que todavía quedan cosas por recorrer

//sería un caos hacerlo manual

/* console.log(iterador.next()) 
console.log(iterador.next()) 
console.log(iterador.next()) 
console.log(iterador.next()) 
console.log(iterador.next()) 
console.log(iterador.next()) 
console.log(iterador.next()) //{value: undefined, done: true} */

//puedo meter los .next en un ciclo

let next = iterador.next()

while(!next.done){
  console.log(next.value)
  next = iterador.next()
  //cada objeto devuelto
  console.log(next)

}



