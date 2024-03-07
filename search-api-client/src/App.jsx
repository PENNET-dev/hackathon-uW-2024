import { useState } from 'react'
import './App.css'
import Avatar from '@mui/material/Avatar'
import { useEffect } from 'react'
import { PlayArrow, Stop } from '@mui/icons-material'
import { AudioRecorder } from 'react-audio-voice-recorder';


function App() {
  const [count, setCount] = useState(0)

  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);

  const startRecording = () => {
    setRecording(true);
  };

  const stopRecording = () => {
    setRecording(false);
  };

  const addAudioElement = (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = url;
    audio.controls = true;
    // document.body.appendChild(audio);
    setAudioBlob(blob);
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
    // Get the file from the audio input
    const file = null;
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        // The result attribute contains the file's data as a base64 encoded string
        let base64data = reader.result.split(',')[1]; // Split on comma to remove the Data URL declaration part
        resolve(base64data);
      };
      reader.onerror = reject;
      console.log("audioBlob", audioBlob);
      reader.readAsDataURL(audioBlob);
    })
      .then(base64data => {
        console.log(base64data);
        // Get the target from the radio buttons
        const target = document.querySelector('input[name="target"]:checked').value

        // Define the request body
        const body = {
          search_audio_data: base64data,
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
      });
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
        <div className="recorder-container">
          <AudioRecorder
            onRecordingComplete={addAudioElement}
            audioTrackConstraints={{
              noiseSuppression: true,
              echoCancellation: true,
              autoGainControl: true,
              channelCount: 1,
              sampleRate: 16000,
            }}
            downloadOnSavePress={true}
            downloadFileExtension="webm"
          />
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


        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target1" name="target" value="target1" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target1">Beginning</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target2" name="target" value="target2" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target2">God</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target3" name="target" value="target3" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target3">Jesus</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target4" name="target" value="target4" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target4">Wilderness</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" id="target5" name="target" value="target5" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target5">Word</label>
          </div>
        </div>
        <div className="centeredFlexbox" style={{paddingTop: "1rem"}}>
          <button type="submit" onClick={checkKeywords}>Search</button>
        </div>
        <div className="centeredFlexbox">
          {Boolean(results) && results >= 0.65 && <>
            {/* Add green checkmark emoji inside of Avatar */}
            <Avatar sx={{ bgcolor: 'green' }}>✔</Avatar>
          </>}
          {Boolean(results) && results < 0.65 && <>
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
