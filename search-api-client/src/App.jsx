import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  // checkKeywords function: POST the audio file to the server and get the results
  const checkKeywords = async () => {
    // Get the audio file from the form
    const audio = document.getElementById('audio').files[0]
    // Get the target from the radio buttons
    const target = document.querySelector('input[name="target"]:checked').value

    // Define the request body
    const body = {
      search_audio_data: audio,
      target_file_path: 'God1.wav'
    };

    // Make the POST request
    fetch('http://192.168.86.27:5000/api/search', {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.text())
      .then(data => alert(data))
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
        <input type="file" id="audio" name="audio" accept=".wav" />
        <button type="submit" onClick={checkKeywords}>Search</button>
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
          <img src={reactLogo} className="App-logo" alt="reactLogo" />
          <p>Results: 100%</p>
        </div>
      </main>
    </div>
  )
}

export default App
