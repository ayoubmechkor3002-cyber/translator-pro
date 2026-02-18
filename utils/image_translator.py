"""
Module OCR et traduction d'images
"""
from PIL import Image
import pytesseract
import logging
import os
import sys
from utils.text_translator import text_translator

# =============================
# CONFIGURATION TESSERACT (AUTO)
# =============================
# التحقق من نظام التشغيل وضبط مسار Tesseract
if os.name == "nt":  # Windows
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif sys.platform == "linux":  # Linux (Streamlit Cloud)
    # Tesseract مثبت عبر packages.txt
    tesseract_path = "/usr/bin/tesseract"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

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
        if not text:
            return ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def extract_text(self, image: Image.Image, source_lang: str) -> str:
        """OCR Image avec gestion d'erreurs améliorée"""
        try:
            # التأكد من أن الصورة في الوضع الصحيح
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            # الحصول على لغة Tesseract
            tess_lang = self.tesseract_lang_map.get(source_lang, "eng")

            # استخراج النص
            text = pytesseract.image_to_string(
                image,
                lang=tess_lang,
                config="--psm 6 --oem 3"
            )

            # تنظيف النص
            text = self.clean_text(text)

            logger.info(f"✅ OCR réussi : {len(text)} caractères extraits")
            return text

        except pytesseract.TesseractNotFoundError:
            error_msg = "Tesseract non installé. Veuillez vérifier le fichier packages.txt"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"❌ Erreur OCR: {str(e)}")
            raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")

    def translate_image(self, image: Image.Image, source_lang: str, target_lang: str) -> str:
        """OCR + Traduction avec gestion d'erreurs"""
        try:
            # استخراج النص من الصورة
            extracted_text = self.extract_text(image, source_lang)

            if not extracted_text or len(extracted_text.strip()) < 2:
                return "⚠️ Aucun texte détecté dans l'image. Assurez-vous que l'image contient du texte lisible."

            # ترجمة النص
            translated = self.translator.translate(
                extracted_text,
                source_lang,
                target_lang
            )
            
            return translated

        except Exception as e:
            logger.error(f"❌ Erreur traduction image: {str(e)}")
            raise


# =============================
# INSTANCE GLOBALE
# =============================
image_translator = ImageTranslator()
