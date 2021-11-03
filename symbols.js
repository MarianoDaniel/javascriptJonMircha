/**Nuevos tipos de datos en javascript: Suelen usarse para identificar propiedades de objetos, para evitar coliciones, sobreescrituras */

const NOMBRE = Symbol()

const persona = {
    [NOMBRE]: "Mariano"
}