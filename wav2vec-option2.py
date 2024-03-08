from scipy.spatial.distance import cosine
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
import pyttsx3
import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import Wav2Vec2FeatureExtractor
import librosa
import soundfile as sf

# Initialize feature extractor and model
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

def extract_features(audio_file):
    audio, sampling_rate = torchaudio.load(audio_file, normalize=True)
    audio_input = feature_extractor(audio, return_tensors="pt", sampling_rate=sampling_rate).input_values 
    with torch.no_grad():
        features = model(audio_input).last_hidden_state
    return features

def calculate_similarity(file1, file2):
    features1 = extract_features(file1)
    features2 = extract_features(file2)
    return 1 - cosine(features1.mean(axis=1).numpy(), features2.mean(axis=1).numpy())

audio_file1 = "inTheBeginning1.wav"
audio_file2 = "inTheBeginning2.wav"

similarity = calculate_similarity(audio_file1, audio_file2)
print(similarity)