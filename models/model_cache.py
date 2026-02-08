"""
Gestion du cache des modèles MarianMT pour optimiser les performances
"""
from transformers import MarianMTModel, MarianTokenizer
import torch
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelCache:
    """Cache intelligent pour les modèles de traduction"""
    
    def __init__(self):
        self.models: Dict[str, MarianMTModel] = {}
        self.tokenizers: Dict[str, MarianTokenizer] = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"💻 Device utilisé: {self.device}")
        
        # Mapping des paires de langues vers les modèles MarianMT
        self.model_mapping = {
            "fr-en": "Helsinki-NLP/opus-mt-fr-en",
            "en-fr": "Helsinki-NLP/opus-mt-en-fr",
            "ar-en": "Helsinki-NLP/opus-mt-ar-en",
            "en-ar": "Helsinki-NLP/opus-mt-en-ar",
            "fr-ar": "Helsinki-NLP/opus-mt-fr-ar",
            "ar-fr": "Helsinki-NLP/opus-mt-ar-fr",
            "es-en": "Helsinki-NLP/opus-mt-es-en",
            "en-es": "Helsinki-NLP/opus-mt-en-es",
            "de-en": "Helsinki-NLP/opus-mt-de-en",
            "en-de": "Helsinki-NLP/opus-mt-en-de",
            "it-en": "Helsinki-NLP/opus-mt-it-en",
            "en-it": "Helsinki-NLP/opus-mt-en-it",
        }
    
    def get_model_name(self, source_lang: str, target_lang: str) -> str:
        """Obtient le nom du modèle pour une paire de langues"""
        pair = f"{source_lang}-{target_lang}"
        if pair in self.model_mapping:
            return self.model_mapping[pair]
        raise ValueError(f"❌ Paire de langues non supportée: {pair}")
    
    def load_model(self, source_lang: str, target_lang: str) -> Tuple[MarianMTModel, MarianTokenizer]:
        """Charge un modèle depuis le cache ou depuis Hugging Face"""
        pair = f"{source_lang}-{target_lang}"
        
        # Si le modèle est déjà en cache
        if pair in self.models:
            logger.info(f"✅ Modèle {pair} chargé depuis le cache")
            return self.models[pair], self.tokenizers[pair]
        
        # Sinon, charger le modèle
        try:
            model_name = self.get_model_name(source_lang, target_lang)
            logger.info(f"⬇️ Téléchargement du modèle: {model_name}")
            
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name).to(self.device)
            
            # Mettre en cache
            self.models[pair] = model
            self.tokenizers[pair] = tokenizer
            
            logger.info(f"✅ Modèle {pair} chargé avec succès")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
            raise
    
    def clear_cache(self):
        """Vide le cache des modèles"""
        self.models.clear()
        self.tokenizers.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("🗑️ Cache vidé")


# Instance globale du cache
model_cache = ModelCache()
