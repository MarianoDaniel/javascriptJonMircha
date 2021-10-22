console.log("********************************************");
console.log("*******Funciones Anónimas Autoejecutables*********");
    /**
     * me dió un error y el motivo lo explican acá
     * https://stackoverflow.com/questions/31013221/typeerror-console-log-is-not-a-function/31013390
     * 
     * TypeError: console.log (...) no es una función

    Tenga en cuenta el (...)después del nombre de la función. Con ellos, se refiere al valor de retorno de la función.

     */
    //Funciones Anónimas Autoejecutables
    //entre parentesis para que tenga referencia en memoria
    //En esta función sí se pone punto y coma
   export const auto = (function (d,w,c) {
        console.log("Mi primer IIFE: inmdiatly invoque function executable")
     console.log(d,w,c)
     c.log("Este es un console.log")
    })(document,window,console);

  
