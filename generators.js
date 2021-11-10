//los generadores sirven para volver iterable una función. 
function* iterable() {
    yield "Hola"
    console.log("Hola consola")
    yield "Hola 2"
    console.log("Seguimos con más instrucciones de nuestro código")
    yield "Hola 3"
    yield "Hola 4"
}

let iterador = iterable()
/* console.log(iterador.next())
console.log(iterador.next())
console.log(iterador.next())
console.log(iterador.next())
console.log(iterador.next()) */

//lo automatizamos

/* for (let y of iterador) {
    console.log(y)
} */

const arr = [...iterable()]
console.log(arr)

//asincronía con generadores

function cuadrado(valor) {
    setTimeout(() => {
       return console.log({ valor, resultado: valor * valor })
    }, Math.random() * 1000);
}


function* generador(){
    console.log("Inicia generador")
    yield cuadrado(2)
    yield cuadrado(3)
    yield cuadrado(4)
    yield cuadrado(5)
    yield cuadrado(6)
}

    let gen = generador()
    console.log(gen)

    for (let y of gen){
        console.log(y)
    }
/*
//MDN Example:

function* foo(index) {
    while (index < 2) {
      yield index;
      index++;
    }
  }

  const iterator = foo(0);

  console.log(iterator.next().value);
  // expected output: 0

  console.log(iterator.next().value);
  // expected output: 1
   */