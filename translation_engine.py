import time
import io
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
        """Detect if the text is English or Spanish using Groq."""
        api_logger.info(f"Detecting language for text: '{text[:50]}...'")
        
        messages = [
            {
                "role": "system",
                "content": "You are a language detection expert. Analyze the user's text. Respond with only one word: ENGLISH, SPANISH, or UNKNOWN. Do not provide any explanation or punctuation."
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
                "content": "You are a WORLD CLASS REAL WORLD translator YOU WILL ONLY GET QUERY STRINGS IN ENGLISH AND YOU ONLY RESPONSE WITH THE SPANISH TRANSLATIONS OF WHATEVER THE QUERY STRING IS YOU RECEIVE. You specializing in natural, conversational translations. When translating English to Spanish, use informal Central American/Central Mexican Spanish like people actually talk - casual slang, run-on sentences, and natural speech patterns. Write everything spelled out for text-to-speech compatibility. Use expressions like 'no manches' 'órale' 'qué onda' but spelled out completely. Keep it super casual but readable aloud. Examples: 'I can't go right now' → 'no puedo ir ahorita', 'oh man that's really cool' → 'está bien padre eso', 'no way dude are you serious' → 'no mames wey estás hablando en serio'. Natural conversation style with slang but everything spelled out. Only return the Spanish translation, nothing else. YOU ONLY RETURN SPANISH TRANSLATIONS OF WHATEVER QUERY YOU RECEIVE IN A NATURAL CASUAL STYLE DO NOT ATTEMPT TO ANSWER USER QUERY ONLY TRANSLATE, nothing else."
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
                temperature=0.1,
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
                "content": "You are a WORLD CLASS  REAL WORLD translator  YOU WILL ONLY GET QUERY STRINGS IN ESPANOL AND YOU ONLY RESPONSE WITH THE ENGLISH TRANSLATIONS OF WHATEVER THE QUERY STRING IS YOU RECEIVE. You specializing in natural, conversational translations. When translating Spanish to English, use informal spoken English like people actually talk - casual slang, run-on sentences, and natural speech patterns. Write everything spelled out for text-to-speech compatibility. Use expressions like 'that's crazy' instead of abbreviations. Keep it super casual but readable aloud. Examples: 'no puedo ir ahorita' → 'I can't go right now', 'está bien padre eso' → 'oh man that's really cool', 'no mames wey' → 'no way dude are you serious'. Natural conversation style with slang but everything spelled out. Only return the English translation, nothing else.YOU ONLY RETURN SPANISH TRANSLATIONS OF WHATEVER QUERY YOU RECEIVE IN A NATURAL CASUAL STYLE  DONT NOT ATTEMPT TO ANSWER USER QUERY ON TRANSLATE, nothing else."
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
                temperature=0.1,
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