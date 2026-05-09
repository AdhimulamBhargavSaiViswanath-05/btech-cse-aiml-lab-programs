// const express = require('express');
// const app = express();
// const port = 3000;
// app.set('view engine', 'ejs');
// app.set('views', './views');
// app.set('views', __dirname + '/views');
// app.get('/', (req, res) => {
//     res.render('index');
// });
// app.listen(port, () => {
//     console.log(`Server running at http://localhost:${port}`);
// });

const { name } = require('ejs');
const express = require('express');
const app = express();
const port = 3000;
app.set('view engine', 'ejs');
app.get('/', (req, res) => {
    res.render('index', {name: "Bhargav", items: ["item1", "item2", "item3"]});
});
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});