# Keyword checking for Low-Resource Languages

Audio is a primary part of the human/computer interaction requried for Oral Bible Translation (OBT).  And some Bible translation efforts target "low resource languages".  As such, Bible translation software must understand spoken audio from low resource languages.

Here, we propose a model to recognize individual words in Dholuo.

Here, "low resource languages" is understood as any language that does not have open, available models for LLM, speech-to-text, and text-to-speech.

By requiring a "stable" model, we require the solution to be independent of tone, volume, speed, or the speaker's gender.

---

Files:
`2024_uW_Hackathon_Exploration.ipynb` - Jupyter notebook (Python)

`naiive-feature-extraction.py` - Compare: Off the shelf feature extraction.
`librosa features.py` - Compare: simple librosa feature extraction.
`wav2vec.py` - Compare: wav2vec feature extraction.

API and Client:
`host.py` - Flask host for API
`search-api-client\` - API client (Vite + React)

.
