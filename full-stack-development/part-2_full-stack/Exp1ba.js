const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

let data = [
    { name: "Bhargav", pwd: "Sai" },
    { name: "Viswanath", pwd: "Sai" }
];

// Accept data
app.post('/data', (req, res) => {
    data.push(req.body);
    res.send('data added');
});

// Retrieve the data
app.get('/data', (req, res) => {
    res.json(data);
});

// Delete data
app.delete('/data/:index', (req, res) => {
    data.splice(req.params.index, 1);
    res.send('data deleted');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
