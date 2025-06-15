<div align="center">

# ⚡ qTranslate

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io) [![Groq](https://img.shields.io/badge/Groq-API-orange.svg)](https://groq.com) [![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-purple.svg)](https://elevenlabs.io) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Voice-Powered Translation with AI**

</div>

<div align="center">
  <img src="reference/Screenshot from 2025-06-14 22-52-57.png" alt="qTranslate Main Interface" width="70%" />
</div>

A real-time translation app that combines speech recognition, AI translation, and text-to-speech capabilities. Powered by Groq's lightning-fast language models and ElevenLabs' premium voice synthesis.

## Features

**🎤 Voice Input**
- Record audio directly in the browser
- Auto-transcription with Groq Whisper
- Auto-clear recorder for seamless workflow

**⚡ Smart Translation**
- Instant language detection (English ↔ Spanish)
- Powered by Groq's Llama 3.3 70B model
- Ctrl+Enter keyboard shortcut support

**🎵 Premium Audio Output**
- 50+ high-quality voices (male/female)
- Auto-generation with voice selection
- Downloadable MP3 files with timestamps
- Editable text for custom voice generation

**💡 Enhanced UX**
- Real-time notifications
- Clean, modern interface
- Mobile-friendly design
- Auto-play functionality

## Translation Results

<div align="center">
  <img src="reference/Screenshot from 2025-06-14 22-55-12.png" alt="Translation Results" width="70%" />
</div>

## Quick Start

### Prerequisites

- Python 3.11+
- Groq API key
- ElevenLabs API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lliWcWill/qTrans14te.git
   cd qTrans14te
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   GROQ_API_KEY=your_groq_api_key_here
   ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

### Voice Translation
1. Click the microphone to record your voice
2. Speak in English or Spanish
3. Audio is automatically transcribed and translated
4. Select a voice to hear the translation

### Text Translation
1. Type or paste text in the input field
2. Press "Translate" or use Ctrl+Enter
3. Edit the translated text if needed
4. Generate audio with your preferred voice

### Audio Export
1. Select any voice to generate audio
2. Click "Save Audio" to download MP3
3. Files include voice name and timestamp

## API Configuration

### Groq Setup
- Get your API key from [Groq Console](https://console.groq.com)
- Used for language detection, translation, and transcription
- Models: Llama 3.3 70B, Whisper Large V3 Turbo

### ElevenLabs Setup
- Get your API key from [ElevenLabs](https://elevenlabs.io)
- Used for high-quality text-to-speech
- Supports 50+ premium voices in multiple accents

## Architecture

```
├── app.py                 # Main Streamlit application
├── translation_engine.py  # Groq API integration
├── audio_handler.py       # ElevenLabs TTS integration
├── audio_player.py        # Custom audio player component
├── config.py             # Configuration and logging
└── requirements.txt      # Python dependencies
```

## Technologies

- **Frontend**: Streamlit with custom CSS/JavaScript
- **Translation**: Groq Llama 3.3 70B
- **Speech Recognition**: Groq Whisper Large V3 Turbo
- **Text-to-Speech**: ElevenLabs API
- **Audio Processing**: Native browser APIs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Groq](https://groq.com) for ultra-fast AI inference
- [ElevenLabs](https://elevenlabs.io) for premium voice synthesis
- [Streamlit](https://streamlit.io) for the web framework

---

<div align="center">
  <strong>Built with ❤️ for seamless communication</strong>
</div>