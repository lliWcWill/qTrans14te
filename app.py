import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import mic_recorder
from streamlit_option_menu import option_menu
from translation_engine import TextTranslator
from audio_handler import TextToSpeechHandler
from audio_player import create_audio_player
from config import LOGGERS
import time

# Get UI logger
ui_logger = LOGGERS['ui']

# --- Page Config & Styling ---
st.set_page_config(
    page_title="Bilingual Text",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        margin: 1rem 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Translate button (Groq orange gradient) */
    .translate-btn > button {
        background: linear-gradient(135deg, #F55036, #e63946) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(245, 80, 54, 0.3), inset 0 1px 0 0 rgba(255,255,255,0.2) !important;
    }
    .translate-btn > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(245, 80, 54, 0.5), inset 0 1px 0 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #ff6b55, #f73947) !important;
    }
    .translate-btn > button:disabled {
        background: #404040 !important;
        color: #666666 !important;
        box-shadow: none !important;
        transform: none !important;
        cursor: not-allowed !important;
    }
    

    /* Speak button (orange gradient) */
    .speak-btn > button {
        background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
        color: #0f0f0f !important;
        box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3), inset 0 1px 0 0 rgba(255,255,255,0.2) !important;
    }
    .speak-btn > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.5), inset 0 1px 0 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #ff7b45, #f7a31e) !important;
    }
    
    /* Dictate button (orange gradient) */
    .dictate-btn > button {
        background: linear-gradient(135deg, #ff6b35, #ff4500) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3), inset 0 1px 0 0 rgba(255,255,255,0.2) !important;
    }
    .dictate-btn > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.5), inset 0 1px 0 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #ff7b45, #ff5500) !important;
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
    }
    
    /* Hide the native Streamlit voice button container */
    #hidden-voice-btn-container,
    #hidden-voice-btn-container * {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        top: -9999px !important;
        left: -9999px !important;
        pointer-events: none !important;
    }
    
    /* Hide the white iframe from mic recorder when not actively recording */
    .stCustomComponentV1[data-testid="stCustomComponentV1"] iframe {
        background: transparent !important;
        border: none !important;
    }
    
    /* Style the mic recorder container to prevent white flashing */
    .stCustomComponentV1.st-emotion-cache-1tvzk6f {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State & Handlers ---
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'translation_direction' not in st.session_state:
    st.session_state.translation_direction = ""
if 'target_language' not in st.session_state:
    st.session_state.target_language = ""
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'audio_status' not in st.session_state:
    st.session_state.audio_status = ""
if 'audio_error' not in st.session_state:
    st.session_state.audio_error = ""
if 'clear_messages' not in st.session_state:
    st.session_state.clear_messages = False
# Note: Only using mic recorder now, but keeping for consistency
if 'recording_method' not in st.session_state:
    st.session_state.recording_method = None
if 'selected_voice' not in st.session_state:
    st.session_state.selected_voice = None
if 'message_timestamp' not in st.session_state:
    st.session_state.message_timestamp = 0
if 'tts_debug_logs' not in st.session_state:
    st.session_state.tts_debug_logs = []
if 'show_voice_modal' not in st.session_state:
    st.session_state.show_voice_modal = False
if 'autoplay_enabled' not in st.session_state:
    st.session_state.autoplay_enabled = True
if 'last_auto_generated_voice' not in st.session_state:
    st.session_state.last_auto_generated_voice = None
if 'audio_loading' not in st.session_state:
    st.session_state.audio_loading = False
if 'page_reload' not in st.session_state:
    st.session_state.page_reload = True
if 'tts_in_progress' not in st.session_state:
    st.session_state.tts_in_progress = False
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'ready_to_translate' not in st.session_state:
    st.session_state.ready_to_translate = False
if 'last_processed_audio' not in st.session_state:
    st.session_state.last_processed_audio = None
if 'male_voice_selector' not in st.session_state:
    st.session_state.male_voice_selector = "Select a voice..."
if 'female_voice_selector' not in st.session_state:
    st.session_state.female_voice_selector = "Select a voice..."
if 'tts_text' not in st.session_state:
    st.session_state.tts_text = ""

@st.cache_resource
def get_translator():
    ui_logger.info("Initializing TextTranslator instance.")
    return TextTranslator()

@st.cache_resource
def get_tts_handler():
    ui_logger.info("Initializing TextToSpeechHandler instance.")
    try:
        return TextToSpeechHandler()
    except Exception as e:
        ui_logger.error(f"Failed to initialize TTS handler: {e}")
        return None

translator = get_translator()
tts_handler = get_tts_handler()

# --- Main UI ---
st.html(f"""
<div class="main-header" style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <div style="background: none !important; -webkit-background-clip: initial !important; -webkit-text-fill-color: #FFD700 !important; color: #FFD700 !important; font-size: 2.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); margin-bottom: -0.5rem;">⚡</div>
    <h1 style="font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #00d4ff, #0099cc, #006d99); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);">
        <span style="background: none !important; -webkit-background-clip: initial !important; -webkit-text-fill-color: #F55036 !important; color: #F55036 !important; font-weight: 800; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">q</span><span style="color: #00d4ff !important; -webkit-background-clip: unset !important; -webkit-text-fill-color: unset !important; background-clip: unset !important;">Translate</span>
    </h1>
    <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.2rem; font-weight: 400;">Voice-Powered Translation</p>
    <div style="margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; opacity: 0.9;">
        <span style="color: #F55036; font-weight: 800; font-size: 1.4rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">Groq</span>
        <span style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; font-weight: 500;">Powered</span>
    </div>
</div>

""")

# Audio Recording Section
st.markdown('<div class="audio-section">', unsafe_allow_html=True)
st.markdown("### 🎤 Record Voice")

# Clear status messages when new recording starts
def clear_audio_messages():
    # Only clear if not doing TTS
    if not st.session_state.get('tts_in_progress', False):
        st.session_state.audio_status = ""
        st.session_state.audio_error = ""
        st.session_state.message_timestamp = 0

def clear_audio():
    """Clear audio player state and generated audio"""
    log_tts_debug("Clearing audio player state")
    
    # Clear audio-related session state
    if 'generated_audio_path' in st.session_state:
        del st.session_state.generated_audio_path
    if 'generated_audio_voice' in st.session_state:
        del st.session_state.generated_audio_voice
    
    # Set a flag to prevent immediate auto-generation after clearing
    st.session_state.audio_just_cleared = True
    
    st.session_state.audio_played = False
    st.session_state.audio_loading = False
    st.session_state.tts_in_progress = False
    st.session_state.show_voice_modal = False
    st.session_state.page_reload = True  # Reset for next audio generation
    
    # Reset voice selection to prevent auto-generation
    st.session_state.last_auto_generated_voice = None
    
    # Clear audio messages
    clear_audio_messages()
    
    # Force a rerun to update the UI
    st.rerun()

# Debug logging function for TTS events
def log_tts_debug(message):
    timestamp = time.time()
    debug_msg = f"[{timestamp:.2f}] TTS: {message}"
    st.session_state.tts_debug_logs.append(debug_msg)
    ui_logger.info(debug_msg)
    # Keep only last 10 debug messages
    if len(st.session_state.tts_debug_logs) > 10:
        st.session_state.tts_debug_logs = st.session_state.tts_debug_logs[-10:]

# Helper function to generate voice audio
def generate_voice_audio(selected_voice, tts_handler):
    """Generate audio for selected voice with simplified logic"""
    # Use edited text if available, otherwise use original translation
    text_to_speak = st.session_state.get('tts_text', st.session_state.translated_text)
    if not tts_handler or not text_to_speak:
        return False
    
    log_tts_debug(f"Generating audio for voice: {selected_voice}")
    
    try:
        # Mark TTS as in progress to prevent recording interference
        st.session_state.tts_in_progress = True
        
        # Clear any status messages but preserve transcription
        if not st.session_state.get('tts_in_progress', False):
            st.session_state.audio_status = ""
            st.session_state.audio_error = ""
        
        # Get voice_id directly from the voice name (works for both languages)
        voice_id = get_voice_id_from_name(selected_voice, tts_handler)
        
        if not voice_id:
            log_tts_debug(f"Voice ID not found for: {selected_voice}")
            st.session_state.tts_in_progress = False
            return False
        
        # Generate audio directly with voice_id (no language mapping needed)
        audio_data = tts_handler.generate_audio_with_voice_id(
            text_to_speak, 
            voice_id,
            selected_voice
        )
        
        # TTS completed successfully
        st.session_state.tts_in_progress = False
        st.session_state.audio_loading = False
        
        if audio_data:
            # Store audio data for display
            st.session_state.generated_audio_path = audio_data
            st.session_state.generated_audio_voice = selected_voice
            st.session_state.selected_voice = selected_voice  # Remember the voice
            st.session_state.audio_played = True  # Enable restart option
            st.session_state.page_reload = False  # Enable autoplay on next render
            log_tts_debug("Audio generated successfully")
            return True
        else:
            log_tts_debug("TTS returned no audio data")
            return False
    except Exception as e:
        # Reset TTS flags on error
        st.session_state.tts_in_progress = False
        st.session_state.audio_loading = False
        log_tts_debug(f"TTS error: {e}")
        return False

# Helper function to get voice_id from voice name
def get_voice_id_from_name(voice_name, tts_handler):
    """Get voice_id from voice display name - works across all languages"""
    # Search in both english and spanish voice dictionaries
    for lang in ['english', 'spanish']:
        if lang in tts_handler.voices and voice_name in tts_handler.voices[lang]:
            return tts_handler.voices[lang][voice_name]['voice_id']
    return None

# Helper function to get voice info from voice name
def get_voice_info_from_name(voice_name, tts_handler):
    """Get voice info from voice display name - works across all languages"""
    # Search in both english and spanish voice dictionaries
    for lang in ['english', 'spanish']:
        if lang in tts_handler.voices and voice_name in tts_handler.voices[lang]:
            return tts_handler.voices[lang][voice_name]
    return None

# Auto-dismiss messages after 3 seconds (but not during TTS)
current_time = time.time()
if (st.session_state.message_timestamp > 0 and 
    (current_time - st.session_state.message_timestamp) > 3 and 
    not st.session_state.get('tts_in_progress', False)):
    clear_audio_messages()

# Beautiful native audio input - only recording method
audio_data = None

# Only show recording when TTS is not in progress
if (not st.session_state.get('tts_in_progress', False) and 
    not st.session_state.get('audio_loading', False)):
    audio_data = st.audio_input("🎤 Dictate")
else:
    audio_data = None

# Process beautiful native audio input if available
if audio_data is not None and not st.session_state.get('tts_in_progress', False):
    st.session_state.recording_method = 'native'
    
    # Check if this is new audio by comparing with last processed
    audio_bytes = audio_data.read()
    audio_hash = hash(audio_bytes) if audio_bytes else None
    
    if audio_hash and audio_hash != st.session_state.get('last_processed_audio'):
        # Only show recording status if not doing TTS
        if not st.session_state.get('tts_in_progress', False):
            if not st.session_state.audio_status:
                st.session_state.audio_status = "Audio recorded successfully!"
                st.session_state.message_timestamp = current_time
            
            # Show auto-dismissing status
            if st.session_state.audio_status and st.session_state.message_timestamp > 0:
                st.toast(st.session_state.audio_status, icon='🎉')
            if st.session_state.audio_error:
                st.error(st.session_state.audio_error)
        
        # Auto-transcribe when audio is recorded (only new audio)
        with st.spinner("Auto-transcribing audio..."):
            ui_logger.info("Auto-transcribing recorded audio")
            try:
                transcribed_text = translator.transcribe_audio(audio_bytes)
                if not transcribed_text.startswith("Error"):
                    st.session_state.transcribed_text = transcribed_text
                    st.session_state.input_text = transcribed_text  # Also set input_text directly
                    st.session_state.ready_to_translate = True
                    st.session_state.audio_status = f"Transcribed: '{transcribed_text[:100]}...'"
                    st.session_state.message_timestamp = time.time()
                    # Don't mark as processed - this allows fresh recording on next interaction
                    # st.session_state.last_processed_audio = audio_hash  # REMOVED to enable auto-clear
                    # Don't rerun - let natural flow continue
                else:
                    st.session_state.audio_error = transcribed_text
                    # Don't rerun - let natural flow continue
            except Exception as e:
                st.session_state.audio_error = f"Auto-transcription failed: {str(e)}"
                ui_logger.error(f"Auto-transcription error: {e}")

# Reset recording method when no audio is present
if audio_data is None:
    if st.session_state.recording_method is not None:
        st.session_state.recording_method = None
        clear_audio_messages()

st.markdown('</div>', unsafe_allow_html=True)

# Text Input Section - Show transcribed text or allow manual input
display_text = st.session_state.get('transcribed_text', '') or st.session_state.input_text
input_text = st.text_area(
    "Enter English or Spanish text:",
    height=150,
    placeholder="Type or paste your text here, or use the recorder above...",
    key="input_text_area",
    value=display_text
)

# Update session state when text area changes
if input_text != st.session_state.input_text:
    st.session_state.input_text = input_text
    # Clear transcribed text if user manually edits
    if st.session_state.get('transcribed_text') and input_text != st.session_state.transcribed_text:
        st.session_state.transcribed_text = ""
        st.session_state.ready_to_translate = bool(input_text.strip())

# Button Layout - Centered Translate Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Check if there's text to translate
    has_text = bool(input_text.strip())
    button_disabled = not has_text
    
    st.markdown('<div class="translate-btn">', unsafe_allow_html=True)
    if st.button("⚡ Translate", 
                use_container_width=True, 
                key="translate_btn",
                disabled=button_disabled):
        # Reset recording method
        st.session_state.recording_method = None
        clear_audio_messages()
        # Close any open TTS modals when translating
        st.session_state.show_voice_modal = False
        log_tts_debug("Translate button clicked - TTS modal closed")
        
        with st.spinner("Translating..."):
            ui_logger.info("Translate button clicked. Calling engine.")
            translated, direction = translator.detect_and_translate(input_text)
            st.session_state.translated_text = translated
            st.session_state.translation_direction = direction
            
            # Determine target language for TTS
            if "English → Spanish" in direction:
                st.session_state.target_language = "spanish"
            elif "Spanish → English" in direction:
                st.session_state.target_language = "english"
            else:
                st.session_state.target_language = ""
            
            # Reset auto-generation tracker for new translation
            st.session_state.last_auto_generated_voice = None
            
            # Clear transcription state after translation
            st.session_state.transcribed_text = ""
            st.session_state.ready_to_translate = False
            st.session_state.last_processed_audio = None  # Reset audio processing
            
            ui_logger.info(f"Translation received. Direction: {direction}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if button_disabled:
        st.caption("Enter text or record audio to enable translation")

# --- Output Section (Conditional) ---
if st.session_state.translated_text:
    st.markdown("---")
    
    st.markdown(f"### Translation Result ({st.session_state.translation_direction})")
    
    # The output text box - editable and tracked
    edited_text = st.text_area(
        "Translated Text",
        value=st.session_state.translated_text,
        height=150,
        key="output_text_area",
        label_visibility="collapsed",
        help="Edit this text and it will be used for voice generation"
    )
    
    # Update the text that will be sent to TTS
    if edited_text != st.session_state.translated_text:
        st.session_state.tts_text = edited_text
    else:
        st.session_state.tts_text = st.session_state.translated_text
    
    # Center the Copy button under the text box
    copy_col1, copy_col2, copy_col3 = st.columns([1, 1, 1])
    
    with copy_col2:
        # Enhanced copy button using components with proper clipboard permissions
        # Pre-escape the text outside the f-string to avoid backslash issues
        text_to_copy = st.session_state.get('tts_text', st.session_state.translated_text)
        escaped_text = text_to_copy.replace('`', '\\`').replace('\\', '\\\\').replace('\n', '\\n')
        
        copy_button_html = f"""
        <div class="copy-btn-container">
            <button class="copy-btn" onclick="copyToClipboard()">
                📋 Copy
            </button>
        </div>

        <script>
        async function copyToClipboard() {{
            const text = `{escaped_text}`;
            
            try {{
                // Try the modern Clipboard API first
                if (navigator.clipboard && window.isSecureContext) {{
                    await navigator.clipboard.writeText(text);
                    showFeedback('Copied!');
                }} else {{
                    // Fallback for older browsers or insecure contexts
                    const textArea = document.createElement('textarea');
                    textArea.value = text;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    textArea.style.top = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    
                    const successful = document.execCommand('copy');
                    document.body.removeChild(textArea);
                    
                    if (successful) {{
                        showFeedback('Copied!');
                    }} else {{
                        showFeedback('Copy failed');
                    }}
                }}
            }} catch (err) {{
                console.error('Copy failed:', err);
                showFeedback('Copy failed');
            }}
        }}

        function showFeedback(message) {{
            const button = document.querySelector('.copy-btn');
            const originalText = button.innerHTML;
            button.innerHTML = '✅ ' + message;
            button.style.background = 'rgba(0, 255, 0, 0.3)';
            
            setTimeout(() => {{
                button.innerHTML = originalText;
                button.style.background = 'rgba(0, 212, 255, 0.2)';
            }}, 2000);
        }}
        </script>

        <style>
        .copy-btn-container {{
            display: flex;
            justify-content: flex-end;
            margin-top: 1rem;
            position: relative;
            z-index: 10;
        }}
        .copy-btn {{
            background: rgba(0, 212, 255, 0.2);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            color: #00d4ff;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 600;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .copy-btn:hover {{
            background: rgba(0, 212, 255, 0.4);
            transform: scale(1.05);
        }}
        </style>
        """

        components.html(copy_button_html, height=80)
    
    # Modern Voice Selection Interface
    st.markdown("---")
    
    # Voice selection header with status indicator
    voice_header_col1, voice_header_col2 = st.columns([3, 1])
    with voice_header_col1:
        st.markdown("### 🎤 Voice Selection")
    with voice_header_col2:
        if st.session_state.get('audio_loading', False):
            st.markdown("🔄 *Generating...*")
        elif st.session_state.get('audio_played', False):
            st.markdown("✅ *Audio Ready*")
        else:
            st.markdown("⏳ *Select Voice*")
    
    # Autoplay toggle in the top right
    autoplay_col1, autoplay_col2 = st.columns([3, 1])
    with autoplay_col2:
        st.session_state.autoplay_enabled = st.toggle(
            "🔄 Auto-generate",
            value=st.session_state.autoplay_enabled,
            help="Automatically generate audio when selecting a voice"
        )
    
    if tts_handler and st.session_state.translated_text:
        # Create voice cards using option_menu
        with st.container():
            # Get ALL voices from BOTH languages and separate by gender only
            male_voices = []
            female_voices = []
            
            # Get voices from both English and Spanish 
            all_voice_options = []
            if tts_handler.voices.get('english'):
                all_voice_options.extend(list(tts_handler.voices['english'].keys()))
            if tts_handler.voices.get('spanish'):
                all_voice_options.extend(list(tts_handler.voices['spanish'].keys()))
                
                for voice in all_voice_options:
                    # Try getting voice info from either language
                    voice_info = None
                    for lang in ['english', 'spanish']:
                        if lang in tts_handler.voices and voice in tts_handler.voices[lang]:
                            voice_info = tts_handler.voices[lang][voice]
                            break
                    
                    if voice_info:
                        gender = voice_info.get('gender', '').lower()
                        # Clean display name (remove emoji)
                        display_name = voice.replace("👨 ", "").replace("👩 ", "")
                        
                        if gender == 'male':
                            male_voices.append((display_name, voice))
                        elif gender == 'female':
                            female_voices.append((display_name, voice))
                
                # Create Man | Woman columns
                col_male, col_female = st.columns(2)
                
                selected_voice = None
                selected_voice_info = None
                
                # Callback to clear opposite selectbox
                def on_male_selected():
                    if st.session_state.male_voice_selector != "Select a voice...":
                        st.session_state.female_voice_selector = "Select a voice..."
                
                def on_female_selected():
                    if st.session_state.female_voice_selector != "Select a voice...":
                        st.session_state.male_voice_selector = "Select a voice..."
                
                with col_male:
                    st.markdown("**👨 Man**")
                    if male_voices:
                        male_options = ["Select a voice..."] + [name for name, _ in male_voices]
                        selected_male = st.selectbox(
                            "Choose male voice:",
                            options=male_options,
                            key="male_voice_selector",
                            label_visibility="collapsed",
                            on_change=on_male_selected
                        )
                        
                        if selected_male != "Select a voice...":
                            # Reset clear flag when user makes a selection
                            st.session_state.audio_just_cleared = False
                            # Clear any stale status messages only (not transcription)
                            if not st.session_state.get('tts_in_progress', False):
                                st.session_state.audio_status = ""
                                st.session_state.audio_error = ""
                            # Find the full voice name
                            for display_name, full_name in male_voices:
                                if display_name == selected_male:
                                    selected_voice = full_name
                                    # Get voice info using simplified helper
                                    selected_voice_info = get_voice_info_from_name(full_name, tts_handler)
                                    break
                    else:
                        st.info("No male voices available")
                
                with col_female:
                    st.markdown("**👩 Woman**")
                    if female_voices:
                        female_options = ["Select a voice..."] + [name for name, _ in female_voices]
                        selected_female = st.selectbox(
                            "Choose female voice:",
                            options=female_options,
                            key="female_voice_selector", 
                            label_visibility="collapsed",
                            on_change=on_female_selected
                        )
                        
                        if selected_female != "Select a voice...":
                            # Reset clear flag when user makes a selection
                            st.session_state.audio_just_cleared = False
                            # Clear any stale status messages only (not transcription)
                            if not st.session_state.get('tts_in_progress', False):
                                st.session_state.audio_status = ""
                                st.session_state.audio_error = ""
                            # Find the full voice name
                            for display_name, full_name in female_voices:
                                if display_name == selected_female:
                                    selected_voice = full_name
                                    # Get voice info using simplified helper
                                    selected_voice_info = get_voice_info_from_name(full_name, tts_handler)
                                    break
                    else:
                        st.info("No female voices available")
                
                # Show selected voice details
                if selected_voice and selected_voice_info:
                    voice_description = selected_voice_info.get('description', 'Professional voice')
                    st.caption(f"**{selected_voice}** - {voice_description[:100]}{'...' if len(voice_description) > 100 else ''}")
                
                # Only show generation options if a voice is selected
                if selected_voice:
                    # Auto-generate audio if autoplay is enabled and voice changed (and not just cleared)
                    text_to_speak = st.session_state.get('tts_text', st.session_state.translated_text)
                    if (st.session_state.autoplay_enabled and 
                        text_to_speak and 
                        st.session_state.get('last_auto_generated_voice') != selected_voice and
                        not st.session_state.get('audio_just_cleared', False)):
                        
                        # Mark this voice as being auto-generated to prevent re-runs
                        st.session_state.last_auto_generated_voice = selected_voice
                        
                        # Set loading state to prevent mic activation
                        st.session_state.audio_loading = True
                        with st.spinner(f"🔊 Auto-generating audio with {selected_voice}..."):
                            success = generate_voice_audio(selected_voice, tts_handler)
                            if success:
                                st.success(f"🎵 Audio ready with {selected_voice}")
                                # Force rerun to display player with autoplay
                                st.rerun()
                            else:
                                st.error("Failed to generate audio. Please try again.")
                                # Reset on failure so user can try again
                                st.session_state.last_auto_generated_voice = None
                                st.session_state.audio_loading = False
                    
                    # Manual generate button (only appears when voice is selected)
                    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
                    with generate_col2:
                        # Clean display name for button
                        button_display_name = selected_voice.replace("👨 ", "").replace("👩 ", "")
                        if st.button(
                            f"🔊 Generate with {button_display_name}", 
                            key="manual_generate_btn", 
                            type="primary",
                            use_container_width=True,
                            disabled=not st.session_state.get('tts_text', st.session_state.translated_text)
                        ):
                            # Set loading state to prevent mic activation
                            st.session_state.audio_loading = True
                            with st.spinner(f"🔊 Generating audio with {selected_voice}..."):
                                success = generate_voice_audio(selected_voice, tts_handler)
                                if success:
                                    st.success(f"🎵 Audio generated with {selected_voice}")
                                    # Don't rerun - let natural flow continue
                                else:
                                    st.error("Failed to generate audio. Please try again.")
                                    st.session_state.audio_loading = False
                else:
                    # No voice selected - show placeholder message
                    st.info("👆 Select a voice from the dropdowns above to generate audio")
    else:
        # TTS not available
        st.warning("🎤 Text-to-speech service is not available. Please check your ElevenLabs API key.")
        st.button("🎤 TTS Unavailable", disabled=True, use_container_width=True)

# Add restart functionality after audio plays
if 'audio_played' not in st.session_state:
    st.session_state.audio_played = False

# Display custom audio player if audio was generated
if st.session_state.get('generated_audio_path') and st.session_state.get('audio_played', False):
    st.markdown("---")
    
    # Download button above the audio player
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
    
    with button_col2:
        # Read the audio file for download
        with open(st.session_state.generated_audio_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        # Create filename with voice name and timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        voice_name = st.session_state.get('generated_audio_voice', 'audio').replace(' ', '_').replace('👨', '').replace('👩', '')
        filename = f"qtranslate_{voice_name}_{timestamp}.mp3"
        
        # Download button
        st.download_button(
            label="💾 Save Audio",
            data=audio_bytes,
            file_name=filename,
            mime="audio/mpeg",
            key=f"download_{timestamp}",
            use_container_width=True,
            type="primary"
        )
    
    # Audio player status indicator
    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        st.markdown("### 🎵 Audio Player")
    with status_col2:
        if st.session_state.get('audio_loading', False):
            st.markdown("🔄 *Loading...*")
        else:
            st.markdown("✅ *Ready*")
    
    # Enhanced audio player with autoplay support
    autoplay_enabled = st.session_state.get('autoplay_enabled', False) and not st.session_state.get('page_reload', True)
    
    # Show autoplay message if enabled
    if autoplay_enabled:
        st.info("🔄 Autoplay is enabled - audio will start automatically")
    
    create_audio_player(
        st.session_state.generated_audio_path, 
        text=f"Translation with {st.session_state.get('generated_audio_voice', 'Selected Voice')}",
        autoplay=autoplay_enabled
    )
    
    # Mark that this is no longer a page reload
    st.session_state.page_reload = False

# Show restart option after TTS has been used
if st.session_state.get('audio_played', False):
    st.markdown("---")
    col_restart = st.columns([1, 2, 1])[1]  # Center the restart button
    with col_restart:
        if st.button("🔄 Start New Translation", key="restart_btn", use_container_width=True):
            # Clear all translation-related session state
            st.session_state.translated_text = ""
            st.session_state.translation_direction = ""
            st.session_state.target_language = ""
            st.session_state.input_text = ""
            st.session_state.show_voice_modal = False
            st.session_state.audio_played = False
            st.session_state.selected_voice = None
            st.session_state.tts_debug_logs = []
            st.session_state.last_auto_generated_voice = None
            # Clear voice selectors
            st.session_state.male_voice_selector = "Select a voice..."
            st.session_state.female_voice_selector = "Select a voice..."
            st.session_state.tts_text = ""
            # Clear new transcription state
            st.session_state.transcribed_text = ""
            st.session_state.ready_to_translate = False
            # Clear audio player state
            if 'generated_audio_path' in st.session_state:
                del st.session_state.generated_audio_path
            if 'generated_audio_voice' in st.session_state:
                del st.session_state.generated_audio_voice
            clear_audio_messages()
            log_tts_debug("Application restarted - all state cleared")
            ui_logger.info("Chat restarted by user")
            st.rerun()

# Debug section (only show if there are debug logs and in development)
if st.session_state.tts_debug_logs:
    with st.expander("🔧 TTS Debug Info", expanded=False):
        for log_msg in st.session_state.tts_debug_logs[-5:]:  # Show last 5 messages
            st.text(log_msg)