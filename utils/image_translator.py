"""
Module OCR et traduction d'images
"""
from PIL import Image
import pytesseract
import logging
import os
from utils.text_translator import text_translator

# =============================
# CONFIGURATION TESSERACT (AUTO)
# =============================
if os.name == "nt":  # Windows seulement
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ImageTranslator:
    """Extraction de texte depuis images et traduction"""

    def __init__(self):
        self.translator = text_translator

        # Mapping langues → Tesseract
        self.tesseract_lang_map = {
            "fr": "fra",
            "en": "eng",
            "ar": "ara",
            "es": "spa",
            "de": "deu",
            "it": "ita",
        }

    def clean_text(self, text: str) -> str:
        """Nettoyage sans casser les paragraphes"""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def extract_text(self, image: Image.Image, source_lang: str) -> str:
        """OCR Image"""
        try:
            if image.mode != "RGB":
                image = image.convert("RGB")

            tess_lang = self.tesseract_lang_map.get(source_lang, "eng")

            text = pytesseract.image_to_string(
                image,
                lang=tess_lang,
                config="--psm 6"
            )

            text = self.clean_text(text)

            logger.info(f"✅ OCR réussi : {len(text)} caractères")
            return text

        except Exception as e:
            logger.error(f"❌ Erreur OCR: {str(e)}")
            raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")

    def translate_image(self, image: Image.Image, source_lang: str, target_lang: str) -> str:
        """OCR + Traduction"""
        extracted_text = self.extract_text(image, source_lang)

        if not extracted_text:
            return "⚠️ Aucun texte détecté dans l'image"

        return self.translator.translate(
            extracted_text,
            source_lang,
            target_lang
        )


# =============================
# INSTANCE GLOBALE
# =============================
image_translator = ImageTranslator()
