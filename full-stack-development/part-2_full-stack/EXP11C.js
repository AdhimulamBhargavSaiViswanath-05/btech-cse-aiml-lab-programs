// Import the 'fs' module to work with the file system
const fs = require('fs');

// Define the content to be written to the file
const content = [
  'HTML',
  'CSS',
  'Javascript',
  'Typescript',
  'MongoDB',
  'Express.js',
  'React.js',
  'Node.js'
].join('\n');  // Join each element with a newline

// Write the content to src.txt
fs.writeFile('src.txt', content, (err) => {
  if (err) {
    console.error('Error writing to file:', err);
    return;
  }
  console.log('src.txt has been created successfully!');
});