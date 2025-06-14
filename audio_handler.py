import io
import pandas as pd
import os
from elevenlabs.client import ElevenLabs
from config import ELEVEN_LABS_API_KEY, LOGGERS

# Get audio logger
audio_logger = LOGGERS['audio']

class TextToSpeechHandler:
    def __init__(self):
        audio_logger.info("Initializing TextToSpeechHandler with ElevenLabs SDK")
        self.api_key = ELEVEN_LABS_API_KEY
        
        # Load voices from CSV
        self.voices = self._load_voices_from_csv()
        
        if not self.api_key:
            audio_logger.error("ElevenLabs API key not found in environment variables")
            raise ValueError("ElevenLabs API key is required")
        
        # Initialize ElevenLabs client
        try:
            self.client = ElevenLabs(api_key=self.api_key)
            audio_logger.info("ElevenLabs SDK client initialized successfully")
        except Exception as e:
            audio_logger.error(f"Failed to initialize ElevenLabs client: {e}")
            raise
        
        audio_logger.info("TextToSpeechHandler initialized successfully")

    def _load_voices_from_csv(self):
        """Load voice configurations from CSV file with proper multiline handling"""
        try:
            csv_path = "reference/22spanish_voices_complete - spanish_voices_complete.csv"
            if os.path.exists(csv_path):
                # Read CSV with proper multiline handling
                df = pd.read_csv(csv_path, quotechar='"', skipinitialspace=True)
                
                # Clean up the dataframe by removing rows where essential fields are NaN
                df = df.dropna(subset=['voice_id', 'name', 'gender', 'language'])
                
                # Filter for English and Spanish voices only - load ALL available
                english_voices = df[df['language'] == 'en']  # Get ALL English voices
                spanish_voices = df[df['language'] == 'es']  # Get ALL Spanish voices
                
                voices = {
                    'english': {},
                    'spanish': {}
                }
                
                audio_logger.info(f"Processing {len(english_voices)} English and {len(spanish_voices)} Spanish voices from CSV")
                
                # Add English voices
                for _, row in english_voices.iterrows():
                    try:
                        # Clean up multiline names and descriptions
                        clean_name = str(row['name']).replace('\n', ' ').replace('  ', ' ').strip()
                        clean_name = clean_name.split(' - ')[0].strip()  # Remove extra descriptors after dash
                        # Handle names like "Santiago Latinamerican Spanish" - keep only the first name
                        if len(clean_name.split()) > 2 and 'spanish' in clean_name.lower():
                            clean_name = clean_name.split()[0]
                        
                        gender_emoji = "👨" if str(row['gender']).lower() == 'male' else "👩"
                        accent = str(row['accent']).replace('nan', '').replace('NaN', '').strip()
                        accent_label = f" ({accent.title()})" if accent and accent != '' and accent.lower() != 'standard' else ""
                        
                        display_name = f"{gender_emoji} {clean_name}{accent_label}"
                        
                        # Clean description
                        description = str(row['description']).replace('\n', ' ').replace('  ', ' ').strip()
                        if description == 'nan' or description == 'NaN':
                            description = f"Professional {str(row['gender']).lower()} voice"
                        
                        voices['english'][display_name] = {
                            'voice_id': str(row['voice_id']).strip(),
                            'name': clean_name,
                            'gender': str(row['gender']).strip(),
                            'accent': accent,
                            'description': description[:100] + "..." if len(description) > 100 else description
                        }
                        
                        audio_logger.debug(f"Added English voice: {display_name} (ID: {row['voice_id']})")
                        
                    except Exception as e:
                        audio_logger.warning(f"Skipping English voice due to parsing error: {e}")
                        continue
                
                # Add Spanish voices  
                for _, row in spanish_voices.iterrows():
                    try:
                        # Clean up multiline names and descriptions
                        clean_name = str(row['name']).replace('\n', ' ').replace('  ', ' ').strip()
                        clean_name = clean_name.split(' - ')[0].strip()  # Remove extra descriptors after dash
                        # Handle names like "Santiago Latinamerican Spanish" - keep only the first name
                        if len(clean_name.split()) > 2 and 'spanish' in clean_name.lower():
                            clean_name = clean_name.split()[0]
                        
                        gender_emoji = "👨" if str(row['gender']).lower() == 'male' else "👩"
                        accent = str(row['accent']).replace('nan', '').replace('NaN', '').strip()
                        accent_label = f" ({accent.title()})" if accent and accent != '' and accent.lower() != 'standard' else ""
                        
                        display_name = f"{gender_emoji} {clean_name}{accent_label}"
                        
                        # Clean description
                        description = str(row['description']).replace('\n', ' ').replace('  ', ' ').strip()
                        if description == 'nan' or description == 'NaN':
                            description = f"Professional {str(row['gender']).lower()} voice"
                        
                        voices['spanish'][display_name] = {
                            'voice_id': str(row['voice_id']).strip(),
                            'name': clean_name,
                            'gender': str(row['gender']).strip(),
                            'accent': accent,
                            'description': description[:100] + "..." if len(description) > 100 else description
                        }
                        
                        audio_logger.debug(f"Added Spanish voice: {display_name} (ID: {row['voice_id']})")
                        
                    except Exception as e:
                        audio_logger.warning(f"Skipping Spanish voice due to parsing error: {e}")
                        continue
                
                audio_logger.info(f"Successfully loaded {len(voices['english'])} English and {len(voices['spanish'])} Spanish voices from CSV")
                return voices
                
            else:
                audio_logger.warning("Voice CSV file not found, using default voices")
        except Exception as e:
            audio_logger.error(f"Error loading voices from CSV: {e}")
            audio_logger.error(f"CSV parsing failed, falling back to default voices")
        
        # Fallback to default voices if CSV loading fails
        return {
            'english': {
                '👩 Sarah (American)': {
                    'voice_id': 'EXAVITQu4vr4xnSDxMaL',
                    'name': 'Sarah',
                    'gender': 'female',
                    'accent': 'american',
                    'description': 'Young adult woman with a confident and warm, mature quality...'
                },
                '👨 Will (American)': {
                    'voice_id': 'bIHbv24MWmeRgasZH58o',
                    'name': 'Will',
                    'gender': 'male',
                    'accent': 'american',
                    'description': 'Conversational and laid back...'
                }
            },
            'spanish': {
                '👩 Lumina (Colombian)': {
                    'voice_id': 'x5IDPSl4ZUbhosMmVFTk',
                    'name': 'Lumina',
                    'gender': 'female',
                    'accent': 'colombian',
                    'description': 'A neutral and versatile female voice, characterized by its clarity...'
                },
                '👨 Santiago (Mexican)': {
                    'voice_id': '15bJsujCI3tcDWeoZsQP',
                    'name': 'Santiago',
                    'gender': 'male',
                    'accent': 'mexican',
                    'description': 'Young Spanish Male. Voice is Clear, casual with a Mexican accent...'
                }
            }
        }
        
    def get_voice_options(self, language):
        """Get available voice options for a language"""
        language_key = language.lower()
        if language_key in self.voices:
            return list(self.voices[language_key].keys())
        return []
        
    def get_voice_info(self, language, voice_display_name):
        """Get voice information for a specific voice"""
        language_key = language.lower()
        if language_key in self.voices and voice_display_name in self.voices[language_key]:
            return self.voices[language_key][voice_display_name]
        return None

    def generate_audio_with_voice_id(self, text, voice_id, voice_name):
        """
        Generate audio directly with voice_id - simplified approach
        
        Args:
            text (str): Text to convert to speech
            voice_id (str): ElevenLabs voice ID
            voice_name (str): Display name for logging
            
        Returns:
            str: Path to temp MP3 file or None if failed
        """
        audio_logger.info(f"Converting text to speech with voice: {voice_name} (ID: {voice_id})")
        
        try:
            # Use the official ElevenLabs SDK with fast model for real-time use
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_flash_v2_5",  # Ultra-fast model ~75ms, supports all languages
                output_format="mp3_44100_128",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            )
            
            # Convert the audio generator to bytes
            audio_bytes = b''.join(audio)
            audio_logger.info(f"TTS request successful. Audio size: {len(audio_bytes)} bytes")
            
            # Save to temp file for reliable st.audio() playback
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
                audio_logger.info(f"Audio saved to temp file: {temp_file_path}")
                return temp_file_path
            
        except Exception as e:
            audio_logger.error(f"TTS request failed with ElevenLabs SDK: {e}")
            return None

    def text_to_speech(self, text, language, voice_name=None):
        """
        Convert text to speech using ElevenLabs SDK
        
        Args:
            text (str): Text to convert to speech
            language (str): Target language ('english' or 'spanish')
            voice_name (str): Optional specific voice name from dropdown
            
        Returns:
            bytes: MP3 audio data or None if failed
        """
        audio_logger.info(f"Converting text to speech in {language}: '{text[:50]}...'")
        
        # Get voice configuration
        language_key = language.lower()
        if language_key not in self.voices:
            audio_logger.error(f"Unsupported language: {language}")
            return None
        
        # Use specific voice if provided, otherwise use first available voice
        if voice_name and voice_name in self.voices[language_key]:
            voice_config = self.voices[language_key][voice_name]
        else:
            # Get first voice as default
            first_voice_key = list(self.voices[language_key].keys())[0]
            voice_config = self.voices[language_key][first_voice_key]
            
        voice_id = voice_config['voice_id']
        
        try:
            audio_logger.info(f"Making TTS request with ElevenLabs SDK for voice: {voice_config['name']} (ID: {voice_id})")
            
            # Use the official ElevenLabs SDK with fast model for real-time use
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_flash_v2_5",  # Ultra-fast model ~75ms, supports all languages
                output_format="mp3_44100_128",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            )
            
            # Convert the audio generator to bytes
            audio_bytes = b''.join(audio)
            audio_logger.info(f"TTS request successful. Audio size: {len(audio_bytes)} bytes")
            
            # Save to temp file for reliable st.audio() playback (like BiLingual AI)
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
                audio_logger.info(f"Audio saved to temp file: {temp_file_path}")
                return temp_file_path
            
        except Exception as e:
            audio_logger.error(f"TTS request failed with ElevenLabs SDK: {e}")
            return None

    def get_available_voices(self):
        """
        Get list of available voices from ElevenLabs API using SDK
        
        Returns:
            dict: Available voices or None if failed
        """
        audio_logger.info("Fetching available voices from ElevenLabs API using SDK")
        
        try:
            voices_response = self.client.voices.get_all()
            voices_data = {
                "voices": voices_response.voices,
                "total_count": len(voices_response.voices)
            }
            audio_logger.info(f"Successfully fetched {len(voices_response.voices)} voices using SDK")
            return voices_data
        except Exception as e:
            audio_logger.error(f"Failed to fetch voices using SDK: {e}")
            return None