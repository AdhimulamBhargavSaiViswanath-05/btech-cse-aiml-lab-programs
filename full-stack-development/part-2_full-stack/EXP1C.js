const express = require('express');
const app = express();
const port = 3000;

// Middleware to check login credentials
function loginCheck(req, res, next) {
    if (req.query.username === 'admin' && req.query.password === '1234') {
        next();
    } else {
        res.status(401).send('Unauthorized user: invalid credentials');
    }
}

// Protected route
app.get('/dashboard', loginCheck, (req, res) => {
    res.send('Welcome to our dashboard');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
