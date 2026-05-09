// Install first: npm install express express-session cookie-parser
const express = require("express");
const session = require("express-session");
const cookieParser = require("cookie-parser");
const app = express();
const PORT = 3000;
// Middleware
app.use(cookieParser());
app.use(session({
    secret: "mySecretKey",
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 60000 }  // 1 minute session
}));
// Route to set session
app.get("/set", (req, res) => {
    req.session.username = "Bhargav"; // store value in session
    res.send("Session data is set! <a href='/get'>Check it</a>");
});
// Route to get session
app.get("/get", (req, res) => {
    if (req.session.username) {
        res.send(`Stored session value: ${req.session.username}`);
    } else {
        res.send("No session data found. <a href='/set'>Set again</a>");
    }
});
// Route to destroy session
app.get("/destroy", (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            res.send("Error destroying session");
        } else {
            res.clearCookie("connect.sid");
            res.send("Session destroyed!");
        }
    });
});
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
