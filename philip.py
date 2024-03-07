# Import all required packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct
import librosa
import soundfile as sf
import os
from scipy.spatial.distance import cosine
import noisereduce as nr

def calc_plot_mfcc_features(audio,
                             sample_rate,
                             alpha = 0.97,
                             NFFT=512,
                             low_freq_cut=10,
                             nfilt=40,
                             noise_floor_dB=-100,
                             frame_size=0.02,
                             frame_stride=0.02,
                             num_ceps=13,
                             figsize=(10, 5),
                             title= ''
                             ):

    # Pre-emphasis
    audio = np.append(audio[0], audio[1:] - alpha * audio[:-1])

    # Calculate frame length and frame step (convert from seconds to samples)
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))

    # Calculate the total number of frames
    num_frames = int(np.ceil(float(np.abs(len(audio) - frame_length)) / frame_step))

    # Pad audio signal
    pad_audio_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_audio_length - len(audio)))
    pad_audio = np.append(audio, z)

    # Initialize the frames
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_audio[indices.astype(np.int32, copy=False)]

    # Apply window function (Hamming)
    frames *= np.hamming(frame_length)

    # Perform FFT and calculate power spectrum
    #mag_frames = np.absolute(fft.fft(frames, NFFT))
    #pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))

    mag_frames = np.absolute(np.fft.fft(frames, NFFT))
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))

    # Take only up to (NFFT/2) + 1 elements after the FFT,
    # as those are the unique frequency components for real-valued signals.
    mag_frames = mag_frames[:, :NFFT//2 + 1]
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))

    # By setting low_freq_mel to the Mel equivalent of low_freq_cut (for ex. 80 Hz),
    # we ensure that the lowest band edge of your Mel filter bank starts at that freq.
    low_freq_mel = 2595 * np.log10(1 + low_freq_cut / 700.0)  # Convert Hz to Mel

    # Apply Mel filter banks
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])
        f_m = int(bin[m])
        f_m_plus = int(bin[m + 1])

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = 1 - (k - bin[m]) / (bin[m + 1] - bin[m])

    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
    filter_banks = 20 * np.log10(filter_banks)  # dB

    # Apply the noise floor
    filter_banks = np.where(filter_banks < noise_floor_dB, noise_floor_dB, filter_banks)

    # Normalize the Mel Filterbank Energies
    mean = np.mean(filter_banks, axis=0)
    std_dev = np.std(filter_banks, axis=0)
    std_dev[std_dev == 0] = 1e-10
    filter_banks -= mean
    filter_banks /= std_dev

    # Apply Discrete Cosine Transform (DCT)
    mfcc = dct(filter_banks,
            type=2,
            axis=-1,
            norm='ortho')[:, 1 : (num_ceps + 1)]  # Exclude 0th order coefficient (energy)

    # create a list of processed features
    processed_features = mfcc.flatten()
    processed_features = np.round(processed_features, 4)
    processed_features = processed_features.tolist()

    # Plotting the filter bank matrix
    plt.figure(figsize=figsize)
    plt.imshow(filter_banks, aspect='auto', cmap='coolwarm', origin='lower')
    plt.colorbar(label='Filter Bank Value')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Filter Index')
    plt.title(title+' - Mel Filter Banks')

    # # Plotting the MFCC
    # plt.figure(figsize=figsize)
    # plt.imshow(mfcc, cmap='coolwarm', origin='lower', aspect='auto', extent=[0, 49, 1, 13])
    # plt.colorbar(label='Coefficient Value')
    # plt.xlabel('Frame Index')
    # plt.ylabel('MFCC Coefficient Index')
    # plt.title(title+' - MFCC')
    # # plt.show()
    # plt.close()

    # We only look at 20 MFCC coefficients:
    return processed_features[:40]


# Load audio file
def load_audio(audioSampleFilePath): #, sr=64000, duration=0.13):
    assert os.path.isfile(audioSampleFilePath), f"No file at {audioSampleFilePath}"
    print(os.path.getsize(audioSampleFilePath))
    data, sample_rate = librosa.load(audioSampleFilePath)
    # Trim
    data, _ = librosa.effects.trim(data)
    # Remove noise floor
    data = nr.reduce_noise(y=data, sr=sample_rate)
    # Normalize signal
    data = librosa.util.normalize(data)
    
    return data, sample_rate



# --- --- ---

filePrefix = "/content/drive/MyDrive/Colab Notebooks/2024 - unfoldingWord Hackathon/"
filePrefix = ""
filePaths = ['God1.wav', 'God2.wav', 'God3.wav', 'God4.wav',
         'inTheBeginning1.wav', 'inTheBeginning2.wav', 
         'jesus1.wav', 'jesus2.wav', 
         'wilderness1.wav', 'wilderness2.wav']

target_file_path = 'God4.wav'

# Loop filePaths calling calc_plot_mfcc_features for each filePath:
features = []
for filePath in filePaths:
    audio_data, sample_rate = load_audio(filePrefix + filePath)
    current_mfcc = calc_plot_mfcc_features(
                        audio_data,
                        sample_rate,
                        alpha = 0.97,
                        NFFT=512,
                        low_freq_cut=10,
                        nfilt=32,
                        noise_floor_dB=-100,
                        frame_size=0.025,
                        frame_stride=0.02,
                        num_ceps = 13,
                        figsize = (8,4),
                        title=filePath)
    print(filePath, "Len = ", len(current_mfcc))
    features.append(current_mfcc)
    
    
target_audio_data, sample_rate = load_audio(filePrefix + target_file_path)
target_features = calc_plot_mfcc_features(
                        target_audio_data,
                        sample_rate,
                        alpha = 0.97,
                        NFFT=512,
                        low_freq_cut=10,
                        nfilt=32,
                        noise_floor_dB=-100,
                        frame_size=0.025,
                        frame_stride=0.02,
                        num_ceps = 13,
                        figsize = (8,4),
                        title=target_file_path
    )

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

similarities = compute_similarities(features, target_features)
print(similarities)

print()
print()
print("Similar to " + target_file_path + ":")
# Print similarities in this format: "filename: similarity
for key, value in similarities.items():
    print(f"{key}: {value}")
