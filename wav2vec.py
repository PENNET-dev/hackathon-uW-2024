# Pip commands to install all necessary packages:
"""
pip install SpeechRecognition
pip install pyttsx3
pip install torchaudio
pip install torch
pip install transformers
pip install librosa

# Sox is not supported on Windows
pip install soundfile
pip install setuptools
"""

import numpy as np
import pyttsx3
import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import Wav2Vec2FeatureExtractor
import librosa
import soundfile as sf
from scipy.spatial.distance import cosine


engine = pyttsx3.init()

# Declare empty male/female voice ID placeholder:
maleVoice = "KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
femaleVoice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
# Get list of voices
voices = engine.getProperty('voices')
# Print each voice's name string:
for voice in voices:
    print(voice.id)
# # Select a male/female voice.id by searching for "female" in the name:
# for voice in voices:
#     if "Zira" in voice.name:
#         print("Zira found")
#         femaleVoice = voice.id
#         break
#     if "David" in voice.name:
#         maleVoice = voice.id
#         break
print("Voices:", maleVoice, femaleVoice)
    
def generate_wav_file(text, output_file, voice, rate=150):
    # Set sampling rate to 16000 for wav2vec:
    engine.setProperty('rate', rate)  # Adjust the speaking rate if needed
    engine.setProperty('voice', voice)  # Set the voice to the specified voice
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    # Resample the wav to 16000 using librosa: (to match wav2vec requirements):
    y, sr = librosa.load(output_file, sr=16000)
    sf.write(output_file, y, sr)

# # Generate the WAV file with a male voice
# generate_wav_file("In the beginning", "inTheBeginning1.wav", voice=maleVoice)
# # Generate the WAV file with a female voice
# generate_wav_file("In the beginning", "inTheBeginning2.wav", voice=femaleVoice)

## ---

# # Use wav2vec package to extract features vectors from each wav:
# # Load the pre-trained model and processor
# processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
# model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
# # Define a function to extract feature vectors from a WAV file
# def extract_feature_vectors(wav_file):
#     waveform, sample_rate = torchaudio.load(wav_file)
#     print(waveform.shape, sample_rate)
#     input_values = processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_values
#     with torch.no_grad():
#         logits = model(input_values).logits
#     return logits


def extract_feature_vectors(wav_file):
    audio, sampling_rate = torchaudio.load(wav_file, normalize=True)
    extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=sampling_rate, padding_value=0.0, do_normalize=True, return_attention_mask=True)
    # Extract features
    features = extractor(audio, return_tensors="pt", padding=True).input_values
    return features


# --- --- ---
sample1 = extract_feature_vectors("jesus1.wav").squeeze().numpy()
print(sample1)

sample2 = extract_feature_vectors("jesus2.wav").squeeze().numpy()
print(sample2)

# # Calcualte the cosine similarity between the two feature vectors:
# # Convert BatchFeature objects to tensors
# inTheBeginning1features_tensor = inTheBeginning1features
# inTheBeginning2features_tensor = inTheBeginning2features
# # Calculate the cosine similarity between the two feature vectors


def compute_similarity(search_vectors, target_vectors):
    # search_vectors and target_vectors are arrays. Pad to make same length
    if len(search_vectors) > len(target_vectors):
        target_vectors = np.pad(target_vectors, (0, len(search_vectors) - len(target_vectors)))
    elif len(search_vectors) < len(target_vectors):
        search_vectors = np.pad(search_vectors, (0, len(target_vectors) - len(search_vectors)))
    
    similarity = (1 - cosine(target_vectors, search_vectors) )
    return similarity


similarity = compute_similarity(sample1, sample2)
print(similarity)
