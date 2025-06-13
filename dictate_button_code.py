# Add this import at the top of app.py
from st_audiorec import st_audiorec

# Add this session state initialization after the existing ones
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Replace the existing button section with this code:
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Audio recording component
    wav_audio_data = st_audiorec()
    
    if wav_audio_data is not None:
        with st.spinner("Transcribing speech..."):
            ui_logger.info("Audio recorded. Starting transcription.")
            transcribed_text = translator.transcribe_audio(wav_audio_data)
            
            if not transcribed_text.startswith("Error"):
                # Update the text area with transcribed text
                st.session_state.input_text_area = transcribed_text
                st.session_state.transcribed_text = transcribed_text
                ui_logger.info(f"Transcription successful: '{transcribed_text[:50]}...'")
                st.success("Speech transcribed successfully!")
                st.rerun()  # Refresh to show the transcribed text in the input area
            else:
                st.error(transcribed_text)

with col2:
    if st.button("⚡ Translate", use_container_width=True):
        if st.session_state.get("input_text_area", ""):
            with st.spinner("Translating..."):
                ui_logger.info("Translate button clicked. Calling engine.")
                translated, direction = translator.detect_and_translate(st.session_state.input_text_area)
                st.session_state.translated_text = translated
                st.session_state.translation_direction = direction
                ui_logger.info(f"Translation received. Direction: {direction}")
        else:
            st.toast("Please enter some text to translate.")

with col3:
    if st.button("🎤 Dictate", use_container_width=True):
        st.info("Click the red record button above to start recording your voice!")