console.log("********************************************")
console.log("**************destructuración*********")

let numbers = [1, 2, 3]
//sin destructiración
let uno = numbers[0]
let dos = numbers[1]
let tres = numbers[2]

console.log(uno, dos, tres)

//con destructuración

const [one, two, three] = numbers

console.log(one, two, three)

let person = {
    firstName: "Mariano",
    surName: "Avico",
    age: "34"
}

let { firstName, surName, age } = person

console.log(firstName, surName, age)