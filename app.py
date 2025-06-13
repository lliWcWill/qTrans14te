import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import mic_recorder
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
if 'tts_in_progress' not in st.session_state:
    st.session_state.tts_in_progress = False
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'ready_to_translate' not in st.session_state:
    st.session_state.ready_to_translate = False

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
st.markdown(f"""
<div class="main-header">
    <h1 class="main-title">✍️ Bilingual Text</h1>
    <p class="main-subtitle">Instant Text Translation</p>
    <div style="margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; opacity: 0.9;">
        <span style="color: #F55036; font-weight: 800; font-size: 1.4rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">Groq</span>
        <span style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; font-weight: 500;">Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

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

# Debug logging function for TTS events
def log_tts_debug(message):
    timestamp = time.time()
    debug_msg = f"[{timestamp:.2f}] TTS: {message}"
    st.session_state.tts_debug_logs.append(debug_msg)
    ui_logger.info(debug_msg)
    # Keep only last 10 debug messages
    if len(st.session_state.tts_debug_logs) > 10:
        st.session_state.tts_debug_logs = st.session_state.tts_debug_logs[-10:]

# Auto-dismiss messages after 3 seconds
current_time = time.time()
if st.session_state.message_timestamp > 0 and (current_time - st.session_state.message_timestamp) > 3:
    clear_audio_messages()

# Method selection or detection
audio_data = None
audio_rec = None

# Use Streamlit's native audio input (perfect for Streamlit Cloud)
# Only show recording options when TTS is not in progress
if st.session_state.recording_method != 'mic' and not st.session_state.get('tts_in_progress', False):
    audio_data = st.audio_input("🎤 Dictate")
    
    if audio_data is not None:
        st.session_state.recording_method = 'native'
        
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
        
        audio_bytes = audio_data.read()
        
        # Auto-transcribe when audio is recorded
        if not st.session_state.get('transcribed_text') or st.session_state.transcribed_text == "":
            with st.spinner("Auto-transcribing audio..."):
                ui_logger.info("Auto-transcribing recorded audio")
                try:
                    transcribed_text = translator.transcribe_audio(audio_bytes)
                    if not transcribed_text.startswith("Error"):
                        st.session_state.transcribed_text = transcribed_text
                        st.session_state.ready_to_translate = True
                        st.session_state.audio_status = f"Transcribed: '{transcribed_text[:100]}...'"
                        st.session_state.message_timestamp = time.time()
                        st.rerun()
                    else:
                        st.session_state.audio_error = transcribed_text
                        st.rerun()
                except Exception as e:
                    st.session_state.audio_error = f"Auto-transcription failed: {str(e)}"
                    ui_logger.error(f"Auto-transcription error: {e}")
                    st.rerun()

# Alternative: Microphone recorder (only show if native not selected and TTS not in progress)
if st.session_state.recording_method != 'native' and not st.session_state.get('tts_in_progress', False):
    if st.session_state.recording_method is None:
        st.markdown("**Or use the microphone recorder:**")
    
    audio_rec = mic_recorder(
        start_prompt="🎤 Dictate",
        stop_prompt="🛑 Stop",
        just_once=False,
        use_container_width=True,
        callback=None,
        args=(),
        kwargs={},
        key='recorder'
    )
    
    if audio_rec is not None:
        st.session_state.recording_method = 'mic'
        
        # Only show recording status if not doing TTS
        if not st.session_state.get('tts_in_progress', False):
            if not st.session_state.audio_status:
                st.session_state.audio_status = "Audio recorded with mic recorder!"
                st.session_state.message_timestamp = current_time
            
            # Show auto-dismissing status
            if st.session_state.audio_status and st.session_state.message_timestamp > 0:
                st.toast(st.session_state.audio_status, icon='🎉')
            if st.session_state.audio_error:
                st.error(st.session_state.audio_error)
        
        # Auto-transcribe when mic recording is available
        if not st.session_state.get('transcribed_text') or st.session_state.transcribed_text == "":
            with st.spinner("Auto-transcribing mic recording..."):
                ui_logger.info("Auto-transcribing mic recorded audio")
                try:
                    # streamlit-mic-recorder returns a dictionary with audio data
                    if isinstance(audio_rec, dict):
                        # Extract bytes from the dictionary
                        if 'bytes' in audio_rec:
                            audio_bytes = audio_rec['bytes']
                        elif 'data' in audio_rec:
                            audio_bytes = audio_rec['data']
                        else:
                            # If it's a numpy array or other format, convert it
                            import numpy as np
                            if isinstance(audio_rec.get('array'), np.ndarray):
                                audio_bytes = audio_rec['array'].tobytes()
                            else:
                                raise ValueError("Unable to extract audio bytes from mic recorder data")
                    elif hasattr(audio_rec, 'tobytes'):
                        audio_bytes = audio_rec.tobytes()
                    else:
                        audio_bytes = audio_rec
                        
                    transcribed_text = translator.transcribe_audio(audio_bytes)
                    if not transcribed_text.startswith("Error"):
                        st.session_state.transcribed_text = transcribed_text
                        st.session_state.ready_to_translate = True
                        st.session_state.audio_status = f"Transcribed: '{transcribed_text[:100]}...'"
                        st.session_state.message_timestamp = time.time()
                        st.rerun()
                    else:
                        st.session_state.audio_error = transcribed_text
                        st.rerun()
                except Exception as e:
                    st.session_state.audio_error = f"Auto-transcription failed: {str(e)}"
                    ui_logger.error(f"Auto-transcription error: {e}")
                    st.rerun()

# Reset recording method when no audio is present
if audio_data is None and audio_rec is None:
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
        # Reset recording method to show both options again
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
            
            # Clear transcription state after translation
            st.session_state.transcribed_text = ""
            st.session_state.ready_to_translate = False
            
            ui_logger.info(f"Translation received. Direction: {direction}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if button_disabled:
        st.caption("Enter text or record audio to enable translation")

# --- Output Section (Conditional) ---
if st.session_state.translated_text:
    st.markdown("---")
    
    st.markdown(f"### Translation Result ({st.session_state.translation_direction})")
    
    # The output text box
    st.text_area(
        "Translated Text",
        value=st.session_state.translated_text,
        height=150,
        key="output_text_area",
        label_visibility="collapsed"
    )
    
    # Action buttons container - Two identical buttons side by side
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Select Voice button (using modal approach with Streamlit dialog)
        if tts_handler and st.session_state.target_language:
            voice_options = tts_handler.get_voice_options(st.session_state.target_language)
            if voice_options:
                
                # Voice selection modal is now initialized at the top
                
                # Create a unique session state key for this button
                voice_trigger_key = f"voice_btn_trigger_{id(voice_options)}"
                if voice_trigger_key not in st.session_state:
                    st.session_state[voice_trigger_key] = False
                
                # Use custom HTML button that matches the copy button styling exactly
                voice_button_html = f"""
                <div class="voice-btn-container">
                    <button class="voice-btn" onclick="triggerVoiceSelection()">
                        🎤 Select Voice
                    </button>
                </div>

                <script>
                function triggerVoiceSelection() {{
                    // Try to find and click the hidden Streamlit button
                    setTimeout(() => {{
                        const streamlitButtons = parent.document.querySelectorAll('button');
                        for (let btn of streamlitButtons) {{
                            if (btn.textContent && btn.textContent.includes('Select Voice') && 
                                !btn.classList.contains('voice-btn')) {{
                                btn.click();
                                return;
                            }}
                        }}
                        // Fallback: try to trigger through data attributes
                        const dataButtons = parent.document.querySelectorAll('[data-testid="stButton"] button');
                        for (let btn of dataButtons) {{
                            if (btn.textContent && btn.textContent.includes('Select Voice')) {{
                                btn.click();
                                return;
                            }}
                        }}
                    }}, 10);
                }}
                </script>

                <style>
                .voice-btn-container {{
                    display: flex;
                    justify-content: flex-end;
                    margin-top: 1rem;
                    position: relative;
                    z-index: 10;
                }}
                .voice-btn {{
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
                .voice-btn:hover {{
                    background: rgba(0, 212, 255, 0.4);
                    transform: scale(1.05);
                }}
                </style>
                """
                
                # Native Streamlit button (same styling as copy button for consistency)
                if st.button("🎤 Select Voice", key="native_voice_btn", use_container_width=True):
                    log_tts_debug("Voice selection button clicked - no recording interference")
                    st.session_state.show_voice_modal = True
                    # Explicitly prevent any recording-related state changes
                    # Do not modify recording_method, audio_status, or audio_error here
                
                # Voice selection modal using st.selectbox in an expander
                if st.session_state.show_voice_modal:
                    with st.expander("🎤 Choose Voice", expanded=True):
                        selected_voice = st.selectbox(
                            "Select a voice:",
                            options=voice_options,
                            index=0,
                            key="voice_modal_selector"
                        )
                        
                        col_speak, col_cancel = st.columns([1, 1])
                        
                        with col_speak:
                            if st.button("🔊 Speak Now", key="speak_now_btn", type="primary", use_container_width=True):
                                log_tts_debug(f"Speak Now button clicked for {st.session_state.target_language} with voice {selected_voice}")
                                
                                if tts_handler and st.session_state.translated_text:
                                    with st.spinner("Generating speech..."):
                                        log_tts_debug(f"Starting TTS for text: {st.session_state.translated_text[:50]}...")
                                        try:
                                            # Mark TTS as in progress to prevent recording interference
                                            st.session_state.tts_in_progress = True
                                            
                                            audio_data = tts_handler.text_to_speech(
                                                st.session_state.translated_text, 
                                                st.session_state.target_language,
                                                voice_name=selected_voice
                                            )
                                            
                                            # TTS completed successfully
                                            st.session_state.tts_in_progress = False
                                            
                                            if audio_data:
                                                # Store audio data for display outside the modal
                                                st.session_state.generated_audio_path = audio_data
                                                st.session_state.generated_audio_voice = selected_voice
                                                st.success(f"🔊 Audio generated with voice: {selected_voice}")
                                                log_tts_debug("Audio generated successfully")
                                                st.session_state.show_voice_modal = False
                                                st.session_state.audio_played = True  # Enable restart option
                                                st.session_state.selected_voice = selected_voice  # Remember the voice
                                                st.rerun()
                                            else:
                                                # Reset TTS flag when no audio generated
                                                st.session_state.tts_in_progress = False
                                                st.error("Failed to generate speech. Please try again.")
                                                log_tts_debug("TTS returned no audio data")
                                        except Exception as e:
                                            # Reset TTS flag on error
                                            st.session_state.tts_in_progress = False
                                            st.error(f"Speech generation failed: {str(e)}")
                                            log_tts_debug(f"TTS error: {e}")
                                else:
                                    # Reset TTS flag when service unavailable
                                    st.session_state.tts_in_progress = False
                                    st.error("Text-to-speech service is not available. Please check your ElevenLabs API key.")
                                    log_tts_debug("TTS service unavailable - API key issue")
                        
                        with col_cancel:
                            if st.button("❌ Cancel", key="cancel_voice_btn", use_container_width=True):
                                log_tts_debug("Voice selection cancelled")
                                # Reset TTS flag when canceling
                                st.session_state.tts_in_progress = False
                                st.session_state.show_voice_modal = False
                                st.rerun()
                
            else:
                # No voices available - disabled button
                st.button("🎤 No Voices Available", disabled=True, use_container_width=True)
        else:
            # TTS not available - disabled button  
            st.button("🎤 TTS Unavailable", disabled=True, use_container_width=True)

    with col2:
        # Enhanced copy button using components with proper clipboard permissions
        # Pre-escape the text outside the f-string to avoid backslash issues
        escaped_text = st.session_state.translated_text.replace('`', '\\`').replace('\\', '\\\\').replace('\n', '\\n')
        
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

# Add restart functionality after audio plays
if 'audio_played' not in st.session_state:
    st.session_state.audio_played = False

# Display custom audio player if audio was generated
if st.session_state.get('generated_audio_path') and st.session_state.get('audio_played', False):
    st.markdown("---")
    st.markdown("### 🎵 Audio Player")
    create_audio_player(
        st.session_state.generated_audio_path, 
        text=f"Translation with {st.session_state.get('generated_audio_voice', 'Selected Voice')}",
        autoplay=False  # Don't auto-play on page reload
    )

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