var fs = require("fs");
var data = fs.readFileSync('input.txt');
console.log(data.toString());
let i=1;
while(i<=5)
{
    console.log("The number is "+i);i++;
}