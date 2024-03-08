import { Fragment, useState } from 'react'
import './App.css'
import Avatar from '@mui/material/Avatar'
import { useEffect } from 'react'
import { PlayArrow, Stop } from '@mui/icons-material'
import { AudioRecorder } from 'react-audio-voice-recorder';
import { Button, Stack, Typography } from '@mui/material'


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
    return `${(value * 100).toFixed(4)}`
  }

  const [resultsIsMatch, setResultsIsMatch] = useState(false);
  useEffect(() => {
    if (results != null) {

      // search_results is a dictionary; find the highest value and store the key in top_result
      let top_result = Object.keys(results.search_results).reduce((a, b) => results.search_results[a] > results.search_results[b] ? a : b);
      // console.log("top_result", top_result);
      top_result = top_result.split('.')[0];
      // Remove trailing number from top_result with regex:
      top_result = top_result.replace(/\d+$/, '');
      // console.log("top_result", top_result);

      // If top result == the selected radio button, set resultsIsMatch to true
      if (results.similarity > 0.50 && top_result === document.querySelector('input[name="target"]:checked').value) {
        setResultsIsMatch(true);
      } else {
        setResultsIsMatch(false);
      }
    }
  }, [results])

  const [topResults, setTopResults] = useState([]);
  useEffect(() => {
    if (results != null) {
      // Sort the top results dictionary by value and setTopResults
      let sortedResults = Object.keys(results.search_results).sort((a, b) => results.search_results[b] - results.search_results[a]);

      // For each element in sortedResults, first split on "." then remove the trailing number with regex
      sortedResults = sortedResults.map((result) => {
        result = result.split('.')[0];
        result = result.replace(/\d+$/, '');
        return result;
      });

      // Put the keys back in a new dictionary, with the original values:
      let newResults = {};
      for (let i = 0; i < sortedResults.length; i++) {
        newResults[sortedResults[i]] = results.search_results[results.search_results[sortedResults[i]] + "1.wav"];
      }
      // console.log("newResults", newResults);

      // console.log("sortedResults", sortedResults);
      setTopResults(sortedResults);
    } else {
      setTopResults([]);
    }
  }, [results])

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
      // console.log("audioBlob", audioBlob);
      reader.readAsDataURL(audioBlob);
    })
      .then(base64data => {
        // console.log(base64data);
        // Get the target from the radio buttons
        const target = document.querySelector('input[name="target"]:checked').value

        // Define the request body
        const body = {
          search_audio_data: base64data,
          target_file_path: target + "1.wav"
        };

        // Make the POST request
        fetch('http://192.168.86.27:5000/api/search', {
          method: 'POST',
          body: JSON.stringify(body),
          headers: { 'Content-Type': 'application/json' },
        })
          .then(response => response.json())
          .then(data => {
            // console.log("results", data);
            setResults(data)
          })
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
        Keyword Checker
      </header>
      <main>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" onClick={() => { setResults(null) }} id="target1" name="target" value="inTheBeginning" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target1">Beginning</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" onClick={() => { setResults(null) }} id="target2" name="target" value="God" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target2">God</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" onClick={() => { setResults(null) }} id="target3" name="target" value="jesus" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target3">Jesus</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" onClick={() => { setResults(null) }} id="target4" name="target" value="wilderness" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target4">Wilderness</label>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <input type="radio" onClick={() => { setResults(null) }} id="target5" name="target" value="word" style={{ width: '0.5in', height: '0.5in' }} />
            <label htmlFor="target5">Word</label>
          </div>
        </div>

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
            downloadOnSavePress={false}
            downloadFileExtension="webm"
          />
        </div>

        <div className="centeredFlexbox" style={{ paddingTop: "1rem" }}>
          <Button variant='contained' type="submit" onClick={checkKeywords}>Search</Button>
        </div>
        {results != null &&
          <Stack sx={{ mt: 3, mb: 0 }} spacing={2} direction="column" display="flex" alignItems="center" justifyContent="center">
            <div className="centeredFlexbox">
              {results && resultsIsMatch && <>
                {/* Add green checkmark emoji inside of Avatar */}
                <Avatar sx={{ bgcolor: 'green' }}>✔</Avatar>
              </>}
              {results && !resultsIsMatch && <>
                {/* Add red X emoji inside of Avatar */}
                <Avatar sx={{ bgcolor: 'red' }}>✖</Avatar>
              </>}
            </div>
            <div>
              <Typography sx={{ color: "#c0c0c0" }}>Similarity: {formatPercentage(results.similarity)}</Typography>
            </div>
          </Stack>}
        {results != null &&
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <Typography variant="h6" sx={{ color: "#505050" }}>Likely Matches:</Typography>
            {topResults.map((result, index) => {
              return (<Fragment key={index}>
                <Typography sx={{ textTransform: "capitalize" }}>
                  {result}
                  {index == 0 && result == document.querySelector('input[name="target"]:checked').value ? " ✔" : ""}
                </Typography>
              </Fragment>)
            }
            )}
          </div>}
      </main >
    </div >
  )
}

export default App
