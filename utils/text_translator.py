"""
Module de traduction de texte avec conservation de la structure
"""
import re
from typing import List
from models.model_cache import model_cache
import logging

logger = logging.getLogger(__name__)


class TextTranslator:
    """Traducteur de texte avec conservation de la structure"""
    
    def __init__(self):
        self.cache = model_cache
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Découpe le texte en phrases en conservant la structure"""
        # Séparation par sauts de ligne
        paragraphs = text.split('\n')
        sentences = []
        
        for para in paragraphs:
            if para.strip():
                # Découpage par phrases (., !, ?)
                sent_list = re.split(r'([.!?]+\s*)', para)
                current_sentence = ""
                
                for i, part in enumerate(sent_list):
                    current_sentence += part
                    if re.match(r'[.!?]+\s*', part):
                        sentences.append(current_sentence.strip())
                        current_sentence = ""
                
                if current_sentence.strip():
                    sentences.append(current_sentence.strip())
            else:
                sentences.append("")  # Conserver les lignes vides
        
        return sentences
    
    def translate(self, text: str, source_lang: str, target_lang: str, 
                  max_length: int = 512) -> str:
        """
        Traduit le texte en conservant la structure originale
        
        Args:
            text: Texte à traduire
            source_lang: Langue source (fr, en, ar, etc.)
            target_lang: Langue cible
            max_length: Longueur maximale des segments
        
        Returns:
            Texte traduit avec structure préservée
        """
        if not text or not text.strip():
            return ""
        
        try:
            # Charger le modèle
            model, tokenizer = self.cache.load_model(source_lang, target_lang)
            
            # Découper en phrases
            sentences = self.split_into_sentences(text)
            translated_sentences = []
            
            for sentence in sentences:
                if not sentence or not sentence.strip():
                    translated_sentences.append(sentence)
                    continue
                
                # Tokenization et traduction
                inputs = tokenizer(sentence, return_tensors="pt", 
                                 padding=True, truncation=True, 
                                 max_length=max_length).to(self.cache.device)
                
                translated = model.generate(**inputs, max_length=max_length)
                translated_text = tokenizer.decode(translated[0], 
                                                  skip_special_tokens=True)
                
                translated_sentences.append(translated_text)
            
            # Reconstituer le texte avec la structure originale
            result = '\n'.join(translated_sentences)
            
            logger.info(f"✅ Traduction {source_lang}→{target_lang} réussie")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur de traduction: {str(e)}")
            raise Exception(f"Erreur lors de la traduction: {str(e)}")


# Instance globale
text_translator = TextTranslator()
