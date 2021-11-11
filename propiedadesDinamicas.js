
let aleatorio = Math.round(Math.random()*100 + 5)
const objUsuarios = {
    propiedad: "Valor",
    [`id_${aleatorio}`]:"Valor Aleatorio"
}
console.log(objUsuarios)
const usuarios = ["jon","irma","miguel","cala","kenai"]

usuarios.forEach((usuario,index)=> {
  objUsuarios[`id_${index}`]= usuario  
})

console.log(objUsuarios)
