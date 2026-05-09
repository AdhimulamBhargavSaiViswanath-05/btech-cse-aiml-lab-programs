// Import Mongoose
const mongoose = require("mongoose");

// Step 1: Connect to MongoDB
mongoose.connect("mongodb://127.0.0.1:27017/studentDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("✅ MongoDB Connected Successfully"))
.catch(err => console.log("❌ Connection Error: ", err));

// Step 2: Define Schema
const studentSchema = new mongoose.Schema({
  roll_no: Number,
  name: String,
  course: String,
  marks: Number
});

// Step 3: Create Model
const Student = mongoose.model("Student", studentSchema);

// Step 4: CRUD Operations

// (A) CREATE – Insert Documents
async function createStudents() {
  const data = await Student.insertMany([
    { roll_no: 1, name: "Bhargav", course: "FSD", marks: 95 },
    { roll_no: 2, name: "Sai", course: "AI", marks: 85 },
    { roll_no: 3, name: "Ram", course: "CSE", marks: 90 }
  ]);
  console.log("🟢 Inserted Records:", data);
}

// (B) READ – Retrieve Documents
async function readStudents() {
  const data = await Student.find();
  console.log("📘 All Students:", data);
}

// (C) UPDATE – Modify Documents
async function updateStudent() {
  const data = await Student.updateOne(
    { name: "Sai" },
    { $set: { marks: 88 } }
  );
  console.log("🟡 Updated Record:", data);
}

// (D) DELETE – Remove Documents
async function deleteStudent() {
  const data = await Student.deleteOne({ name: "Ram" });
  console.log("🔴 Deleted Record:", data);
}

// Step 5: Call Functions Sequentially
async function runCRUD() {
  await createStudents();
  await readStudents();
  await updateStudent();
  await deleteStudent();
  await readStudents();
}

runCRUD();



//output:

// PS C:\Users\DELL\OneDrive\Documents\FSD 2.0 Practice> node exp4a.js
// (node:2764) [MONGODB DRIVER] Warning: useNewUrlParser is a deprecated option: useNewUrlParser has no effect since Node.js Driver version 4.0.0 and will be removed in the next major version
// (Use `node --trace-warnings ...` to show where the warning was created)
// (node:2764) [MONGODB DRIVER] Warning: useUnifiedTopology is a deprecated option: useUnifiedTopology has no effect since Node.js Driver version 4.0.0 and will be removed in the next major version
// ✅ MongoDB Connected Successfully
// 🟢 Inserted Records: [
//   {
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     _id: new ObjectId('6905df890d8fa438820876a6'),
//     __v: 0
//   },
//   {
//     roll_no: 2,
//     name: 'Sai',
//     course: 'AI',
//     marks: 85,
//     _id: new ObjectId('6905df890d8fa438820876a7'),
//     __v: 0
//   },
//   {
//     roll_no: 3,
//     name: 'Ram',
//     course: 'CSE',
//     marks: 90,
//     _id: new ObjectId('6905df890d8fa438820876a8'),
//     __v: 0
//   }
// ]
// 📘 All Students: [
//   {
//     _id: new ObjectId('69047342918bf409b5cebea4'),
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95
//   },
//   {
//     _id: new ObjectId('69047342918bf409b5cebea5'),
//     name: 'Charan',
//     course: 'AI',
//     marks: 85
//   },
//   {
//     _id: new ObjectId('69047342918bf409b5cebea6'),
//     name: 'Umesh',
//     course: 'CSE (Honors)',
//     marks: 90
//   },
//   {
//     _id: new ObjectId('6905d6c4665e251f6ede4113'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905d6c4665e251f6ede4114'),
//     roll_no: 2,
//     name: 'Venkatesh',
//     course: 'AI',
//     marks: 88,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df11abf167ee3adba5f1'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df11abf167ee3adba5f2'),
//     roll_no: 2,
//     name: 'Sai',
//     course: 'AI',
//     marks: 88,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df890d8fa438820876a6'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df890d8fa438820876a7'),
//     roll_no: 2,
//     name: 'Sai',
//     course: 'AI',
//     marks: 85,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df890d8fa438820876a8'),
//     roll_no: 3,
//     name: 'Ram',
//     course: 'CSE',
//     marks: 90,
//     __v: 0
//   }
// ]
// 🟡 Updated Record: {
//   acknowledged: true,
//   modifiedCount: 0,
//   upsertedId: null,
//   upsertedCount: 0,
//   matchedCount: 1
// }
// 🔴 Deleted Record: { acknowledged: true, deletedCount: 1 }
// 📘 All Students: [
//   {
//     _id: new ObjectId('69047342918bf409b5cebea4'),
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95
//   },
//   {
//     _id: new ObjectId('69047342918bf409b5cebea5'),
//     name: 'Charan',
//     course: 'AI',
//     marks: 85
//   },
//   {
//     _id: new ObjectId('69047342918bf409b5cebea6'),
//     name: 'Umesh',
//     course: 'CSE (Honors)',
//     marks: 90
//   },
//   {
//     _id: new ObjectId('6905d6c4665e251f6ede4113'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905d6c4665e251f6ede4114'),
//     roll_no: 2,
//     name: 'Venkatesh',
//     course: 'AI',
//     marks: 88,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df11abf167ee3adba5f1'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df11abf167ee3adba5f2'),
//     roll_no: 2,
//     name: 'Sai',
//     course: 'AI',
//     marks: 88,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df890d8fa438820876a6'),
//     roll_no: 1,
//     name: 'Bhargav',
//     course: 'FSD',
//     marks: 95,
//     __v: 0
//   },
//   {
//     _id: new ObjectId('6905df890d8fa438820876a7'),
//     roll_no: 2,
//     name: 'Sai',
//     course: 'AI',
//     marks: 85,
//     __v: 0
//   }
// ]
// PS C:\Users\DELL\OneDrive\Documents\FSD 2.0 Practice> 