import fetch from 'node-fetch';
import fs from 'fs';

// Read the WAV file and convert it to base64
const wavFile = fs.readFileSync('../wilderness2.wav');
const base64Wav = wavFile.toString('base64');

// Define the request body
const body = {
    search_audio_data: base64Wav,
    search_sample_rate: 16000,  // Replace with your actual sample rate
    target_file_path: 'wilderness1.wav'
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