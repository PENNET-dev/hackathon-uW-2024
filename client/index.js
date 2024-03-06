import fetch from 'node-fetch';
import fs from 'fs';

// Define the request body
const body = {
    search_audio_data: fs.readFileSync('../wilderness1.wav').toString('base64'),
    target_file_path: 'God1.wav'
};

// Make the POST request
fetch('http://192.168.86.27:5000/api/search', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: { 'Content-Type': 'application/json' },
})
.then(response => response.text())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));