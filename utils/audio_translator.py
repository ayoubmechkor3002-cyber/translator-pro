"""
Module de transcription audio et traduction
"""
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import os
from utils.text_translator import text_translator
import logging

logger = logging.getLogger(__name__)


class AudioTranslator:
    """Transcription audio vers texte et traduction"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = text_translator
        
        # Mapping des codes de langue pour Google Speech
        self.speech_lang_map = {
            "fr": "fr-FR",
            "en": "en-US",
            "ar": "ar-SA",
            "es": "es-ES",
            "de": "de-DE",
            "it": "it-IT",
        }
    
    def convert_to_wav(self, audio_bytes: bytes, audio_format: str) -> bytes:
        """
        Convertit un fichier audio en WAV pour la reconnaissance vocale
        
        Args:
            audio_bytes: Données audio
            audio_format: Format d'origine (mp3, ogg, wav, etc.)
        
        Returns:
            Données WAV
        """
        try:
            # Charger l'audio
            audio = AudioSegment.from_file(
                io.BytesIO(audio_bytes), 
                format=audio_format
            )
            
            # Convertir en WAV mono 16kHz (optimal pour Speech Recognition)
            audio = audio.set_channels(1).set_frame_rate(16000)
            
            # Exporter en WAV
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)
            
            return wav_io.read()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la conversion audio: {str(e)}")
    
    def transcribe_audio(self, audio_bytes: bytes, audio_format: str, 
                        source_lang: str) -> str:
        """
        Transcrit un fichier audio en texte
        
        Args:
            audio_bytes: Données audio
            audio_format: Format du fichier (mp3, wav, ogg)
            source_lang: Code langue (fr, en, ar, etc.)
        
        Returns:
            Texte transcrit
        """
        try:
            # Convertir en WAV si nécessaire
            if audio_format.lower() != 'wav':
                logger.info(f"🔄 Conversion {audio_format} → WAV")
                audio_bytes = self.convert_to_wav(audio_bytes, audio_format)
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
            
            try:
                # Charger l'audio avec SpeechRecognition
                with sr.AudioFile(tmp_path) as source:
                    audio = self.recognizer.record(source)
                
                # Obtenir le code langue
                speech_lang = self.speech_lang_map.get(source_lang, "en-US")
                
                # Reconnaissance vocale
                logger.info(f"🎤 Transcription en cours ({speech_lang})...")
                text = self.recognizer.recognize_google(audio, language=speech_lang)
                
                logger.info(f"✅ Transcription réussie: {len(text)} caractères")
                return text
                
            finally:
                # Supprimer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            
        except sr.UnknownValueError:
            raise Exception("⚠️ Impossible de comprendre l'audio")
        except sr.RequestError as e:
            raise Exception(f"❌ Erreur du service de reconnaissance vocale: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Erreur transcription: {str(e)}")
            raise
    
    def translate_audio(self, audio_bytes: bytes, audio_format: str, 
                       source_lang: str, target_lang: str) -> str:
        """
        Transcrit et traduit un fichier audio
        
        Args:
            audio_bytes: Données audio
            audio_format: Format du fichier
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            Texte traduit
        """
        try:
            # Transcription
            transcribed_text = self.transcribe_audio(
                audio_bytes, audio_format, source_lang
            )
            
            if not transcribed_text.strip():
                return "⚠️ Aucun texte transcrit"
            
            # Traduction
            translated_text = self.translator.translate(
                transcribed_text, source_lang, target_lang
            )
            
            return translated_text
            
        except Exception as e:
            logger.error(f"❌ Erreur traduction audio: {str(e)}")
            raise


# Instance globale
audio_translator = AudioTranslator()
