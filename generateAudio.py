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

import pyttsx3
import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import Wav2Vec2FeatureExtractor
import librosa
import soundfile as sf

engine = pyttsx3.init()

# Declare empty male/female voice ID placeholder:
maleVoice = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
femaleVoice = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
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
print()
print("Voices:", maleVoice, femaleVoice)
print()
    
def generate_wav_file(text, output_file, voice, rate=150):
    engine = pyttsx3.init()
    # Set sampling rate to 16000 for wav2vec:
    engine.setProperty('rate', rate)  # Adjust the speaking rate if needed
    engine.setProperty('voice', voice)  # Set the voice to the specified voice
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    # Resample the wav to 16000 using librosa: (to match wav2vec requirements):
    y, sr = librosa.load(output_file, sr=16000)
    sf.write(output_file, y, sr)


# Generate the WAV file with a male voice
generate_wav_file("In the beginning", "inTheBeginning1.wav", voice=maleVoice)
# Generate the WAV file with a female voice
generate_wav_file("In the beginning", "inTheBeginning2.wav", voice=femaleVoice)

# Generate the WAV file with a male voice
generate_wav_file("Wilderness", "wilderness1.wav", voice=maleVoice)
# Generate the WAV file with a female voice
generate_wav_file("Wilderness", "wilderness2.wav", voice=femaleVoice)

# Generate the WAV file with a male voice
generate_wav_file("Jesus", "jesus1.wav", voice=maleVoice)
# Generate the WAV file with a female voice
generate_wav_file("Jesus", "jesus2.wav", voice=femaleVoice)

# Generate the WAV file with a male voice
generate_wav_file("God", "God1.wav", voice=maleVoice)
# Generate the WAV file with a female voice
generate_wav_file("God", "God2.wav", voice=femaleVoice)
