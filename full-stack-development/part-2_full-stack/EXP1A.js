const express = require('express');
const app = express();
const port = 3000;

// Basic route
app.get('/', (req, res) => {
    res.send('Welcome to the Home Page');
});

// Route with parameters
app.get('/user/:id', (req, res) => {
    res.send(`User ID from route parameter: ${req.params.id}`);
});

// Route with query parameters
// Example: http://localhost:3000/search?keyword=apple&limit=5
app.get('/search', (req, res) => {
    res.send(`Searching for: ${req.query.keyword}, Limit: ${req.query.limit}`);
});

// URL building and redirect
app.get('/go-to-user/:id', (req, res) => {
    res.redirect(`/user/${req.params.id}`);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});