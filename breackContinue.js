console.log("********************************************")
console.log("**************breack y continue*********")

//breack y continuos no se puede utilizar en los metodos de los arreglos solo en estructiras de control como swith for while... 
const num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

for (let i = 0; i < num.length; i++) {
    if (i === 5) {
        break;
    }
    console.log(i)
}

for (let i = 0; i < num.length; i++) {
    if (i === 5) {
        continue;
    }
    console.log(i)
}