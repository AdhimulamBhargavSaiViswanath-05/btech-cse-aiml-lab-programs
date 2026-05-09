// Authentication.js
const express = require("express");
const session = require("express-session");
const cookieParser = require("cookie-parser");
const path = require("path");

const app = express();

// Middleware setup
app.use(express.urlencoded({ extended: true })); // parse form data globally
app.use(cookieParser());
app.use(
    session({
        secret: "your-secret-key",
        resave: false,
        saveUninitialized: false,
        cookie: { httpOnly: true }, // secure cookie handling
    })
);

// Middleware to check if the user is authenticated
const isAuthenticated = (req, res, next) => {
    if (req.session.user) {
        next();
    } else {
        res.redirect("/login");
    }
};

// Routes
app.get("/", (req, res) => {
    res.send("Welcome to the Express.js Session and Cookies Example!");
});

app.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname, "login.html"));
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;

    // Check if the provided credentials are valid
    if (username === "admin" && password === "admin") {
        // Store user data in the session
        req.session.user = username;

        // (Optional) set your own cookie
        res.cookie("sessionId", req.sessionID, { httpOnly: true });

        res.redirect("/profile");
    } else {
        res.send("Invalid credentials. Please try again.");
    }
});

app.get("/profile", isAuthenticated, (req, res) => {
    // Retrieve user data from the session
    const username = req.session.user;
    res.send(`Welcome, ${username}! <br><a href="/logout">Logout</a>`);
});

app.get("/logout", (req, res) => {
    // Destroy the session and redirect to the login page
    req.session.destroy(() => {
        res.clearCookie("sessionId"); // clears custom cookie if set
        res.redirect("/login");
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
