import librosa
from scipy.spatial.distance import cosine
import numpy as np

def compute_mfcc(audio_path):
    y, sr = librosa.load(audio_path)
    y = y - np.mean(y)
    return librosa.feature.mfcc(y=y, sr=sr)

def compute_similarities1(filepaths, targetfilepath):
    mfcc_vectors = [compute_mfcc(path) for path in filepaths]
    target_vectors = compute_mfcc(targetfilepath)
    avg_mfcc_vectors = [np.mean(mfcc, axis=1) for mfcc in mfcc_vectors]
    target_avg_mfcc_vectors = np.mean(target_vectors, axis=1)
    similarities = [1 - cosine(target_avg_mfcc_vectors, vec2) for vec2 in avg_mfcc_vectors]
    # Loop through filepaths by index and associate the same index from similarities dictionary
    namedSimilarities = {filepaths[i]: similarities[i] for i in range(len(filepaths))}
    # Sort by descending similarity:
    namedSimilarities = dict(sorted(namedSimilarities.items(), key=lambda item: item[1], reverse=True))
    return namedSimilarities

def compute_similarities2(filepaths, targetfilepath):
    mfcc_vectors = [compute_mfcc(path) for path in filepaths]
    target_vectors = compute_mfcc(targetfilepath)
    
    if (len(mfcc_vectors) > len(target_vectors)):
        np.append(target_vectors, np.zeros(len(mfcc_vectors) - len(target_vectors)))
    elif (len(mfcc_vectors) < len(target_vectors)):
        np.append(mfcc_vectors, np.zeros(len(target_vectors) - len(mfcc_vectors)))
    print(mfcc_vectors, target_vectors)
    
    # mfcc_vectors is an array of feature vectors; find the max length of the feature vectors:
    maxLength = max([len(vec) for vec in mfcc_vectors])
    
    # Pad the feature vectors to the max length:
    mfcc_vectors = [np.pad(vec, (0, maxLength - len(vec))) for vec in mfcc_vectors]
    # Pad target_vectors if necessary, frst checking for length of target_vectors:
    if len(target_vectors) < maxLength:
        target_vectors = np.pad(target_vectors, (0, maxLength - len(target_vectors)))
    
    similarities = [1 - cosine(target_vectors, vec2) for vec2 in mfcc_vectors]
    # Loop through filepaths by index and associate the same index from similarities dictionary
    namedSimilarities = {filePaths[i]: similarities[i] for i in range(len(filePaths))}
    # Sort by descending similarity:
    namedSimilarities = dict(sorted(namedSimilarities.items(), key=lambda item: item[1], reverse=True))
    return namedSimilarities

# God1.wav
# God2.wav
# inTheBeginning1.wav
# inTheBeginning2.wav
# jesus1.wav
# jesus2.wav
# wilderness1.wav
# wilderness2.wav

filePrefix = "/content/drive/MyDrive/Colab Notebooks/2024 - unfoldingWord Hackathon/"
filePrefix = ""
filePaths = ['God1.wav', 'God2.wav', 
            'inTheBeginning1.wav', 'inTheBeginning2.wav', 
            'jesus1.wav', 'jesus2.wav', 
            'wilderness1.wav', 'wilderness2.wav']
# Add file prefix to each file path:
files = [filePrefix + path for path in filePaths]

target_file_path = 'wilderness1.wav'
similarities = compute_similarities1(files, target_file_path)
print(similarities)

print()
print()
print("Similar to " + target_file_path + ":")
# Print similarities in this format: "filename: similarity
for key, value in similarities.items():
    print(f"{key}: {value}")
