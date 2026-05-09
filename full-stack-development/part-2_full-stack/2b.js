const express = require('express');
const app = express();
// Set EJS as template engine
app.set('view engine', 'ejs');
// Middleware to parse form data
app.use(express.urlencoded({ extended: true }));
// Show the form
app.get('/', (req, res) => {
  res.render('form');  // renders views/form.ejs
});

// Handle form submission
app.post('/submit', (req, res) => {
  const { name, email } = req.body;
  res.render('result', { name, email }); // send data to result.ejs
});
// Start server
app.listen(3000, () => console.log('Server running at http://localhost:3000'));
