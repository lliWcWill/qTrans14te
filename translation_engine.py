import time
import io
import re
from groq import Groq
from config import GROQ_API_KEY, LOGGERS

# Get specialized loggers
api_logger = LOGGERS['api']
translation_logger = LOGGERS['transcription']  # Re-using for consistency

class TextTranslator:
    def __init__(self):
        translation_logger.info("Initializing TextTranslator with Groq API")
        try:
            self.client = Groq(api_key=GROQ_API_KEY)
            translation_logger.info("Groq client initialized successfully for text translation.")
        except Exception as e:
            translation_logger.error(f"Failed to initialize Groq client: {e}")
            raise

    def _detect_language(self, text):
        """Detect if the text is English or Spanish using simple heuristics + Groq fallback."""
        api_logger.info(f"Detecting language for text: '{text[:50]}...'")
        
        # First try simple heuristic detection
        spanish_indicators = ['ñ', 'é', 'á', 'í', 'ó', 'ú', 'ü', '¿', '¡']
        spanish_words = ['el', 'la', 'los', 'las', 'de', 'del', 'en', 'con', 'por', 'para', 'que', 'qué', 'es', 'son', 'está', 'están', 'no', 'sí', 'y', 'o', 'pero', 'como', 'muy', 'más', 'menos', 'todo', 'toda', 'todos', 'todas']
        english_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should', 'this', 'that', 'these', 'those']
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Check for Spanish indicators
        spanish_score = 0
        english_score = 0
        
        # Character-based indicators
        for char in spanish_indicators:
            if char in text_lower:
                spanish_score += 2
        
        # Word-based indicators
        for word in words:
            if word in spanish_words:
                spanish_score += 1
            if word in english_words:
                english_score += 1
        
        # If heuristics are decisive, return result
        if spanish_score > english_score and spanish_score > 2:
            api_logger.info(f"Heuristic detection: SPANISH (score: {spanish_score} vs {english_score})")
            return "SPANISH"
        elif english_score > spanish_score and english_score > 2:
            api_logger.info(f"Heuristic detection: ENGLISH (score: {spanish_score} vs {english_score})")
            return "ENGLISH"
        
        # Fall back to LLM detection for ambiguous cases
        api_logger.info(f"Heuristic inconclusive (scores: Spanish={spanish_score}, English={english_score}), using LLM")
        
        messages = [
            {
                "role": "system",
                "content": "Detect language. Respond with only: ENGLISH or SPANISH"
            },
            {
                "role": "user",
                "content": text
            }
        ]
        
        # Log the full API call for debugging
        api_logger.info(f"LANGUAGE DETECTION API CALL:")
        api_logger.info(f"Model: llama-3.3-70b-versatile")
        api_logger.info(f"Messages: {messages}")
        
        try:
            start_time = time.time()
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.0,
                max_tokens=5
            )
            duration = time.time() - start_time
            detected_lang = chat_completion.choices[0].message.content.strip().upper()
            api_logger.info(f"Language detection API call completed in {duration:.2f}s")
            api_logger.info(f"RAW RESPONSE: '{chat_completion.choices[0].message.content}'")
            api_logger.info(f"CLEANED RESPONSE: '{detected_lang}'")
            
            if detected_lang in ["ENGLISH", "SPANISH"]:
                return detected_lang
            else:
                api_logger.warning(f"Unexpected language detection response: '{detected_lang}', returning UNKNOWN")
                return "UNKNOWN"
        except Exception as e:
            api_logger.error(f"Language detection failed: {e}")
            return "UNKNOWN"

    def _translate_to_spanish(self, english_text):
        """Translate English text to Spanish using Llama 3.3 70B"""
        translation_logger.info(f"Starting text translation to Spanish: '{english_text[:50]}...'")
        
        messages = [
            {
                "role": "system",
                "content": "You are a translation engine. Translate the English text to casual Mexican Spanish. Do not answer questions, do not explain, do not add information. Output only the direct translation, nothing else."
            },
            {
                "role": "user", 
                "content": english_text
            }
        ]
        
        # Log the full API call for debugging
        api_logger.info(f"SPANISH TRANSLATION API CALL:")
        api_logger.info(f"Model: llama-3.3-70b-versatile")
        api_logger.info(f"Messages: {messages}")
        
        try:
            start_time = time.time()
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.0,
                max_tokens=2000
            )
            duration = time.time() - start_time
            result = chat_completion.choices[0].message.content.strip()
            api_logger.info(f"Spanish translation API call completed in {duration:.2f}s")
            api_logger.info(f"RESPONSE: '{result[:100]}...'")
            return result
        except Exception as e:
            translation_logger.error(f"Spanish translation failed: {e}")
            return f"Error during text translation: {str(e)}"

    def _translate_to_english(self, spanish_text):
        """Translate Spanish text to English using Llama 3.3 70B"""
        translation_logger.info(f"Starting text translation to English: '{spanish_text[:50]}...'")
        
        messages = [
            {
                "role": "system",
                "content": "You are a translation engine. Translate the Spanish text to casual English. Do not answer questions, do not explain, do not add information. Output only the direct translation, nothing else."
            },
            {
                "role": "user",
                "content": spanish_text
            }
        ]
        
        # Log the full API call for debugging
        api_logger.info(f"ENGLISH TRANSLATION API CALL:")
        api_logger.info(f"Model: llama-3.3-70b-versatile")
        api_logger.info(f"Messages: {messages}")
        
        try:
            start_time = time.time()
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.0,
                max_tokens=2000
            )
            duration = time.time() - start_time
            result = chat_completion.choices[0].message.content.strip()
            api_logger.info(f"English translation API call completed in {duration:.2f}s")
            api_logger.info(f"RESPONSE: '{result[:100]}...'")
            return result
        except Exception as e:
            translation_logger.error(f"English translation failed: {e}")
            return f"Error during text translation: {str(e)}"

    def transcribe_audio(self, audio_bytes):
        """Transcribe audio to text using Groq Whisper large-v3-turbo"""
        translation_logger.info("Starting audio transcription with Whisper large-v3-turbo")
        try:
            start_time = time.time()
            
            # Create a BytesIO object from the audio bytes
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.wav"  # Required by Groq API
            
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                response_format="text",
                language=None  # Auto-detect language
            )
            
            duration = time.time() - start_time
            api_logger.info(f"Audio transcription completed in {duration:.2f}s")
            translation_logger.info(f"Transcribed text: '{str(transcription)[:100]}...'")
            
            return str(transcription).strip()
            
        except Exception as e:
            translation_logger.error(f"Audio transcription failed: {e}")
            return f"Error during audio transcription: {str(e)}"

    def detect_and_translate(self, text):
        """Automatically detects the language and translates it to the other."""
        translation_logger.info(f"Starting translation for text: '{text[:50]}...'")
        api_logger.info(f"DETECT_AND_TRANSLATE INPUT: '{text}'")
        
        detected_language = self._detect_language(text)
        translation_logger.info(f"Detected language: {detected_language}")
        api_logger.info(f"DETECTED LANGUAGE: {detected_language}")

        if detected_language == "ENGLISH":
            api_logger.info("ROUTING TO: _translate_to_spanish")
            translation = self._translate_to_spanish(text)
            direction = "English → Spanish"
        elif detected_language == "SPANISH":
            api_logger.info("ROUTING TO: _translate_to_english")
            translation = self._translate_to_english(text)
            direction = "Spanish → English"
        else:
            api_logger.info("LANGUAGE DETECTION FAILED - returning error")
            return "Sorry, I can only translate between English and Spanish. Please check your text.", "Unknown"
        
        translation_logger.info(f"Translation completed: {direction}")
        api_logger.info(f"FINAL TRANSLATION RESULT: '{translation}'")
        return translation, direction