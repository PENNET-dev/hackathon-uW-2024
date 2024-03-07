import base64
import io
import os
from flask import Flask, jsonify, request
import librosa
import search  # assuming philip.py is in the same directory
from flask_cors import CORS
import subprocess
from pydub import AudioSegment
from io import BytesIO
from pydub import AudioSegment
from pyogg import OpusFile
from io import BytesIO
import tempfile
from pydub import AudioSegment
import io

from pydub import AudioSegment
import tempfile
import io

def convert_webm_to_wav(file_bytes):
    file_like_object = io.BytesIO(file_bytes)
    sound = AudioSegment.from_file(file_like_object, format="webm")
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=".") as tf:
        temp_name = tf.name
    
    sound.export(temp_name, format="wav")
    
    return temp_name



app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.after_request
def add_cors_headers(response):
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

@app.route('/api/search', methods=['POST'])
def compute_similarities_api():
    data = request.get_json()
    
    # Read parameters from the request:
    # search_audio_data is base64 encoded audio file:
    search_audio_data = data.get('search_audio_data')
    target_file_path = data.get('target_file_path')
    
    # Decode base64 into Tuple[np.ndarray, float] using standard python libraries:
    search_audio_data = base64.b64decode(search_audio_data)
    search_audio_data = io.BytesIO(search_audio_data)
    search_audio_data = convert_webm_to_wav(search_audio_data.getvalue())
    
    # Open the raw search_audio_data content with librosa (it is byte data not a file path)
    search_audio_data, search_sample_rate = librosa.load(search_audio_data, sr=None)
    print("Comparing for", target_file_path)
    similarities = search.compute_similarity_api(search_audio_data, search_sample_rate, target_file_path)
    return jsonify(similarities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)