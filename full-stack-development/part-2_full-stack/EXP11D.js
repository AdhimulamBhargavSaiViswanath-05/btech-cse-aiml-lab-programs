// Import the built-in 'url' module
const url = require('url');

// Define the URL to be parsed
// const webAddress = 'https://www.locolhost:8080/path/page?name=arjun&course=nodejs#section2';
const webAddress = 'https://www.linkedin.com/in/adhimulambhargavsaiviswanath/';
// Parse the URL using the legacy url.parse() method
const parsedUrl = url.parse(webAddress, true);

// Display all components of the URL
console.log("=== Parsed URL Components ===");
console.log("Full URL       :", parsedUrl.href);
console.log("Protocol       :", parsedUrl.protocol);
console.log("Host           :", parsedUrl.host);
console.log("Hostname       :", parsedUrl.hostname);
console.log("Port           :", parsedUrl.port);
console.log("Pathname       :", parsedUrl.pathname);
console.log("Search Query   :", parsedUrl.search);
console.log("Fragment/Hash  :", parsedUrl.hash);