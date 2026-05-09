const express = require('express');
const app = express();
const port = 3000;


app.get('/', (req, res) => {
  res.send('This is a get route method');
});

app.post('/User', (req, res) => {
  res.send('This is a POST route method');
});


app.put('/about', (req, res) => {
  res.send('This is a PUT route method');
});

app.delete('/delete',(req, res) => {
  res.send('This is a delete route method');
});


app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});


// GET http://localhost:3000/ → "This is a get route method"

// POST http://localhost:3000/User → "This is a POST route method"

// PUT http://localhost:3000/about → "This is a PUT route method"

// DELETE http://localhost:3000/delete → "This is a delete route method"