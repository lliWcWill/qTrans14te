import streamlit as st
from st_audiorec import st_audiorec
from translation_engine import TextTranslator
from config import LOGGERS

# Get UI logger
ui_logger = LOGGERS['ui']

# --- Page Config & Styling ---
st.set_page_config(
    page_title="Bilingual Text",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS (Exact copy from CLAUDE.md)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d2d2d 100%);
        color: #e0e0e0;
    }
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #0099cc, #006d99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    .main-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
        font-weight: 400;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
        color: #0f0f0f !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3), inset 0 1px 0 0 rgba(255,255,255,0.2) !important;
        margin: 1rem 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5), inset 0 1px 0 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #00e5ff, #00aadd) !important;
    }
    .language-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #404040;
        box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.1), 0 4px 15px rgba(0,0,0,0.3);
    }
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        border: 1px solid #404040 !important;
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
    }
    .copy-btn-container {
        display: flex;
        justify-content: flex-end;
        margin-top: -2.5rem;
        margin-right: 1rem;
        position: relative;
        z-index: 10;
    }
    .copy-btn {
        background: rgba(0, 212, 255, 0.2);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 0.5rem;
        padding: 0.5rem;
        color: #00d4ff;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .copy-btn:hover {
        background: rgba(0, 212, 255, 0.4);
        transform: scale(1.1);
    }
    .audio-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #404040;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State & Translator ---
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'translation_direction' not in st.session_state:
    st.session_state.translation_direction = ""
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

@st.cache_resource
def get_translator():
    ui_logger.info("Initializing TextTranslator instance.")
    return TextTranslator()

translator = get_translator()

# --- Main UI ---
st.markdown(f"""
<div class="main-header">
    <h1 class="main-title">✍️ Bilingual Text</h1>
    <p class="main-subtitle">Instant Text & Speech Translation</p>
    <div style="margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; opacity: 0.9;">
        <span style="color: #F55036; font-weight: 800; font-size: 1.4rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">Groq</span>
        <span style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; font-weight: 500;">Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Audio Recording Section
st.markdown('<div class="audio-section">', unsafe_allow_html=True)
st.markdown("### 🎤 Record Your Voice")
st.markdown("Click the record button below to dictate your text:")

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    with st.spinner("Transcribing speech..."):
        ui_logger.info("Audio recorded. Starting transcription.")
        transcribed_text = translator.transcribe_audio(wav_audio_data)
        
        if not transcribed_text.startswith("Error"):
            st.session_state.transcribed_text = transcribed_text
            ui_logger.info(f"Transcription successful: '{transcribed_text[:50]}...'")
            st.success("Speech transcribed successfully!")
        else:
            st.error(transcribed_text)

st.markdown('</div>', unsafe_allow_html=True)

# Text Input Section
input_text = st.text_area(
    "Enter English or Spanish text:",
    height=150,
    placeholder="Type or paste your text here...",
    value=st.session_state.transcribed_text,
    key="input_text_area"
)

# Update transcribed text when input changes
if input_text != st.session_state.transcribed_text:
    st.session_state.transcribed_text = ""

col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    if st.button("⚡ Translate", use_container_width=True):
        if input_text:
            with st.spinner("Translating..."):
                ui_logger.info("Translate button clicked. Calling engine.")
                translated, direction = translator.detect_and_translate(input_text)
                st.session_state.translated_text = translated
                st.session_state.translation_direction = direction
                ui_logger.info(f"Translation received. Direction: {direction}")
        else:
            st.toast("Please enter some text to translate or record your voice.")

# --- Output Section (Conditional) ---
if st.session_state.translated_text:
    st.markdown("---")
    
    st.markdown(f"### Translation Result ({st.session_state.translation_direction})")
    
    # The output text box - it's hidden until there's a translation
    st.text_area(
        "Translated Text",
        value=st.session_state.translated_text,
        height=150,
        key="output_text_area",
        label_visibility="collapsed"
    )
    
    # Custom copy button
    escaped_text = st.session_state.translated_text.replace("'", "\\'").replace("\n", "\\n").replace("\\", "\\\\")
    st.markdown(
        f"""
        <div class="copy-btn-container">
            <button class="copy-btn" onclick="navigator.clipboard.writeText('{escaped_text}')">
                📋 Copy
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )