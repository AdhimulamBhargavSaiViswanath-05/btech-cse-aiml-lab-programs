const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello! This is data sent over HTTP.\n');
});

server.listen(3000, () => {
    console.log('Server is running at http://localhost:3000');


    const options = {
        hostname: 'localhost',
        port: 3000,
        path: '/',
        method: 'GET'
    };

    const req = http.request(options, (res) => {
        let data = '';

        console.log(`Status Code: ${res.statusCode}`);

        // When data is received in chunks
        res.on('data', (chunk) => {
            data += chunk;
        });

        // When the whole response is received
        res.on('end', () => {
            console.log('Response from server:', data);
        });
    });

    // Handle client-side error
    req.on('error', (error) => {
        console.error('Error occurred:', error);
    });

    req.end(); // Finalize the request
});
