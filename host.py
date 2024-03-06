import base64
import io
from flask import Flask, jsonify, request
import librosa
import search  # assuming philip.py is in the same directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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
    # Open the raw search_audio_data content with librosa (it is byte data not a file path)
    search_audio_data, search_sample_rate = librosa.load(search_audio_data, sr=None)
    print("Comparing for", target_file_path)
    similarities = search.compute_similarity_api(search_audio_data, search_sample_rate, target_file_path)
    return jsonify(similarities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)