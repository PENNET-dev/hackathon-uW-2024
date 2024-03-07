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

import os
import numpy as np
import pyttsx3
import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import Wav2Vec2FeatureExtractor
import librosa
import soundfile as sf
from scipy.spatial.distance import cosine


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



# Load audio file
def load_audio(audioSampleFilePath): #, sr=64000, duration=0.13):
    assert os.path.isfile(audioSampleFilePath), f"No file at {audioSampleFilePath}"
    print(os.path.getsize(audioSampleFilePath))
    data, sample_rate = librosa.load(audioSampleFilePath)
    return data, sample_rate


def extract_feature_vectors(wav_file):
    audio, sampling_rate = torchaudio.load(wav_file, normalize=True)
    extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=sampling_rate, padding_value=0.0, do_normalize=True, return_attention_mask=True)
    # Extract features
    features = extractor(audio, return_tensors="pt", padding=True).input_values
    return features

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


# --- --- ---
sample1 = extract_feature_vectors("God3.wav").squeeze().numpy()
print(sample1)

sample2 = extract_feature_vectors("jesus2.wav").squeeze().numpy()
print(sample2)

similarity = compute_similarity(sample1, sample1)
print(similarity)


# --- --- ---

filePrefix = "/content/drive/MyDrive/Colab Notebooks/2024 - unfoldingWord Hackathon/"
filePrefix = ""


# mfcc_vectors is a DICTIONARY like this: {'filename': [feature_vector]}
# target_vectors are the feature vectors of the target file
def compute_similarities(feature_vectors, target_vectors):
    targetLength = len(target_vectors)
    
    # Truncate feature vectors to the minimum length:
    feature_vectors = [vec[:targetLength] for vec in feature_vectors]
    # Pad the feature vectors to the max length:
    feature_vectors = [np.pad(vec, (0, targetLength - len(vec))) for vec in feature_vectors]
        
    similarities = [1 - cosine(target_vectors, vec2) for vec2 in feature_vectors]
    # Loop through filepaths by index and associate the same index from similarities dictionary
    namedSimilarities = {filePaths[i]: similarities[i] for i in range(len(filePaths))}
    # Sort by descending similarity:
    namedSimilarities = dict(sorted(namedSimilarities.items(), key=lambda item: item[1], reverse=True))
    return namedSimilarities


filePaths = ['God1.wav', 'God2.wav', 'God3.wav',
         'inTheBeginning1.wav', 'inTheBeginning2.wav', 
         'jesus1.wav', 'jesus2.wav', 
         'wilderness1.wav', 'wilderness2.wav']

target_file_path = 'God3.wav'

# Loop filePaths calling calc_plot_mfcc_features for each filePath:
features = [extract_feature_vectors(filePrefix + filePath).squeeze().numpy() for filePath in filePaths]
target_features = extract_feature_vectors(filePrefix + target_file_path).squeeze().numpy()

similarities = compute_similarities(features, target_features)
print(similarities)

print()
print()
print("Similar to " + target_file_path + ":")
# Print similarities in this format: "filename: similarity
for key, value in similarities.items():
    print(f"{key}: {value}")
