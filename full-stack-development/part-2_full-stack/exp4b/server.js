// Import dependencies
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

// Initialize app
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Step 1: Connect to MongoDB
mongoose.connect("mongodb://127.0.0.1:27017/studentDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("✅ MongoDB Connected Successfully"))
.catch(err => console.log("❌ Connection Error:", err));

// Step 2: Define Schema and Model
const studentSchema = new mongoose.Schema({
  name: String,
  course: String,
  marks: Number,
});

const Student = mongoose.model("Student", studentSchema);

// Step 3: Define RESTful API Routes

// Create (POST)
app.post("/api/students", async (req, res) => {
  const student = new Student(req.body);
  const result = await student.save();
  res.json(result);
});

// Read (GET)
app.get("/api/students", async (req, res) => {
  const data = await Student.find();
  res.json(data);
});

// Update (PUT)
app.put("/api/students/:id", async (req, res) => {
  const data = await Student.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(data);
});

// Delete (DELETE)
app.delete("/api/students/:id", async (req, res) => {
  const data = await Student.findByIdAndDelete(req.params.id);
  res.json({ message: "Student Deleted", data });
});

// Step 4: Start Server
const PORT = 4000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
