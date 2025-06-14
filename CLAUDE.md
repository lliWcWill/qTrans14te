# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QTranslate is a Streamlit-based bilingual translation application that provides instant English ↔ Spanish translation with advanced text-to-speech capabilities. The application combines Groq's AI models for translation and transcription with ElevenLabs' TTS service to create a comprehensive multilingual communication tool.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main application
streamlit run app.py

# Run the application with enhanced speech features
streamlit run app_with_speech.py
```

## Core Architecture

### Translation Engine (`translation_engine.py`)
- **Language Detection**: Uses Groq's Llama 3.3 70B model to auto-detect English/Spanish input
- **Bidirectional Translation**: Translates with conversational style (includes slang like "no manches", "órale")
- **Audio Transcription**: Uses Groq's Whisper large-v3-turbo model for speech-to-text

### Audio System (`audio_handler.py`, `audio_player.py`)
- **Voice Management**: 22+ English/Spanish voices loaded from CSV with gender, accent metadata
- **TTS Generation**: ElevenLabs eleven_flash_v2_5 model for fast (~75ms) audio generation
- **Custom Audio Player**: HTML5 player with waveform visualization, progress bar, autoplay support

### Main Application (`app.py`)
- **Dual Recording Methods**: Native Streamlit audio input + microphone recorder fallback
- **Auto-transcription**: Seamless speech-to-text integration in translation workflow
- **Voice Selection**: Gender-based (male/female) voice categorization with accent filtering

## API Configuration

Required environment variables in `.env`:
- `GROQ_API_KEY`: For translation and transcription services
- `ELEVEN_LABS_API_KEY`: For text-to-speech generation

## Key Features

- **Auto-detection Translation**: Automatically detects input language and translates to opposite language
- **Conversational Translation Style**: Uses casual, slang-heavy translations for natural communication
- **Voice Recording**: Multiple recording options with auto-transcription
- **Advanced TTS**: Voice selection by gender, accent (Mexican, Colombian, American, etc.)
- **Modern UI**: Dark theme with gradient backgrounds, neon accents, custom audio player

## Voice Database

The application uses a CSV-based voice database (`reference/22spanish_voices_complete - spanish_voices_complete.csv`) containing:
- Voice names with gender indicators (👨/👩)
- Accent information (Mexican, Colombian, American, etc.)
- Voice descriptions and characteristics
- ElevenLabs voice IDs for API calls

## Translation Models Used

- **Translation/Detection**: Groq Llama 3.3 70B (fast, accurate language processing)
- **Transcription**: Groq Whisper large-v3-turbo (multilingual speech-to-text)
- **Text-to-Speech**: ElevenLabs eleven_flash_v2_5 (ultra-fast voice synthesis)

## Development Notes

- The application maintains extensive session state for seamless user experience
- Logging is implemented across all components (API, transcription, UI, audio)
- Auto-transcription triggers immediately when audio is recorded
- TTS generation can be set to auto-generate or manual trigger
- The custom audio player provides visual feedback with animated waveforms