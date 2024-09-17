# Installation Instructions

1. Create a conda environment and activate it
```bash
conda create -n talk-to-manifesto python=3.10 -y
conda activate talk-to-manifesto
```

2. Install the dependencies
```bash
pip install poetry
poetry install
```

## Prerequisites
Rename `.env.default` to `.env` and fill in the constants defined in the file.

# How To Run

## Text-to-Speech
```bash
poetry run python -m ai_hub.modules.tts.hf_tts
```

## Speech-to-Text
```bash
poetry run python -m ai_hub.modules.stt.hf_stt
```
