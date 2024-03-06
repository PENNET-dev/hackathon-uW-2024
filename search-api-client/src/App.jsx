import { useState } from 'react'
import './App.css'
import Avatar from '@mui/material/Avatar'
import { useEffect } from 'react'
import { PlayArrow, Stop } from '@mui/icons-material'

function App() {
  const [count, setCount] = useState(0)

  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [hasAudio, setHasAudio] = useState(false); // New state variable
  const [audio, setAudio] = useState(null); // New state variable
  let chunks = [];
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const _MediaRecorder = new MediaRecorder(stream);
        _MediaRecorder.ondataavailable = function (e) {
          chunks.push(e.data);
        }
        _MediaRecorder.onstop = function (e) {
          let blob = new Blob(chunks); //, { 'type': 'audio/ogg; codecs=opus' });
          let audioURL = URL.createObjectURL(blob);
          console.log(audioURL);
          // Now you can use audioURL for audio source or you can read it as bytes using FileReader
          let reader = new FileReader();
          reader.onloadend = function () {
            console.log("setAudio", reader.result); // This is your file bytes
            setAudio(reader.result);
          }
          reader.readAsArrayBuffer(blob);
        }

        setMediaRecorder(_MediaRecorder);
      });
  }, []);

  const startRecording = () => {
    mediaRecorder.start();
    setRecording(true);
    setHasAudio(false);
  };

  const stopRecording = () => {
    mediaRecorder.stop();
    setRecording(false);
    setHasAudio(true);
  };

  // useState for results, default null
  const [results, setResults] = useState(null)

  // function formatPercentage() to format as 4 digit percentage:
  const formatPercentage = (value) => {
    if (value === null) {
      return null;
    }
    return `${(value * 100).toFixed(4)}%`
  }

  const checkKeywords = async () => {
    // Get the target from the radio buttons
    const target = document.querySelector('input[name="target"]:checked').value

    const _arrayBuffer = audio;
    // _arrayBuffer is ArrayBuffer; convert it to base64
    const _bytes = new Uint8Array(_arrayBuffer);
    let binary = '';
    for (let i = 0; i < _bytes.byteLength; i++) {
      binary += String.fromCharCode(_bytes[i]);
    }
    const base64String = window.btoa(binary);

    // Define the request body
    const body = {
      search_audio_data: base64String,
      target_file_path: 'God1.wav'
    };

    // Make the POST request
    fetch('http://192.168.86.27:5000/api/search', {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.text())
      .then(data =>
        setResults(data)
      )
      .catch(error => console.error('Error:', error));
  }

  // A simple react component with the following features:
  // 1. A header with a title
  // 2. An audio upload form 
  // 3. A button to send the audio file to the server
  // 4. A set of 5 radio buttons to select the target audio file
  // 5. A results pane with large font to display and icon and the % results.
  // 6. A footer with a github banner and link
  return (
    <div className="App">
      <header className="App-header">
        Keyword checker
      </header>
      <main>
        <label htmlFor="audio">Upload Audio</label>

        <div>
          <button onClick={startRecording} disabled={recording}>
            <PlayArrow />
          </button>
          <button onClick={stopRecording} disabled={!recording}>
            <Stop />
          </button>
        </div>
        {recording &&
          <div>
            {/* Show red rectangle with white border that reads "Recording" */}
            <div style={{
              width: '100px',
              height: '50px',
              backgroundColor: 'red',
              border: '2px solid white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              Recording
            </div>
          </div>}

        <button type="submit" onClick={checkKeywords} disabled={!hasAudio}>Search</button>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target1" name="target" value="target1" style={{ width: '1in', height: '1in' }} />
            <label htmlFor="target1">Target 1</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target2" name="target" value="target2" style={{ width: '1in', height: '1in' }} />
            <label htmlFor="target2">Target 2</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target3" name="target" value="target3" style={{ width: '1in', height: '1in' }} />
            <label htmlFor="target3">Target 3</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target4" name="target" value="target4" style={{ width: '1in', height: '1in' }} />
            <label htmlFor="target4">Target 4</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target5" name="target" value="target5" style={{ width: '1in', height: '1in' }} />
            <label htmlFor="target5">Target 5</label>
          </div>
        </div>
        <div>
          {Boolean(results) && results >= 0.4 && <>
            {/* Add green checkmark emoji inside of Avatar */}
            <Avatar sx={{ bgcolor: 'green' }}>✔</Avatar>
          </>}
          {Boolean(results) && results < 0.4 && <>
            {/* Add red X emoji inside of Avatar */}
            <Avatar sx={{ bgcolor: 'red' }}>✖</Avatar>
          </>}
        </div>
        <div>
          <p>Results: {formatPercentage(results)}</p>
        </div>
      </main>
    </div>
  )
}

export default App
