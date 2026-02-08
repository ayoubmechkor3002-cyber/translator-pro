"""
Module de traitement et traduction de fichiers (TXT, PDF, DOCX)
"""
from typing import Tuple
import io
from PyPDF2 import PdfReader
from docx import Document
from utils.text_translator import text_translator
import logging

logger = logging.getLogger(__name__)


class FileTranslator:
    """Traducteur de fichiers multiples formats"""
    
    def __init__(self):
        self.translator = text_translator
    
    def extract_text_from_txt(self, file_bytes: bytes) -> str:
        """Extrait le texte d'un fichier TXT"""
        try:
            text = file_bytes.decode('utf-8')
            return text
        except UnicodeDecodeError:
            # Essayer avec d'autres encodages
            try:
                text = file_bytes.decode('latin-1')
                return text
            except:
                raise Exception("Impossible de décoder le fichier TXT")
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extrait le texte d'un fichier PDF"""
        try:
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extrait le texte d'un fichier DOCX"""
        try:
            docx_file = io.BytesIO(file_bytes)
            doc = Document(docx_file)
            
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du DOCX: {str(e)}")
    
    def extract_text(self, file_bytes: bytes, file_type: str) -> str:
        """
        Extrait le texte selon le type de fichier
        
        Args:
            file_bytes: Contenu du fichier en bytes
            file_type: Extension du fichier (txt, pdf, docx)
        
        Returns:
            Texte extrait
        """
        file_type = file_type.lower().strip('.')
        
        extractors = {
            'txt': self.extract_text_from_txt,
            'pdf': self.extract_text_from_pdf,
            'docx': self.extract_text_from_docx,
        }
        
        if file_type not in extractors:
            raise ValueError(f"Type de fichier non supporté: {file_type}")
        
        return extractors[file_type](file_bytes)
    
    def translate_file(self, file_bytes: bytes, file_type: str, 
                      source_lang: str, target_lang: str) -> Tuple[str, str]:
        """
        Extrait et traduit le contenu d'un fichier
        
        Args:
            file_bytes: Contenu du fichier
            file_type: Type du fichier
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            Tuple (texte_original, texte_traduit)
        """
        try:
            # Extraction
            original_text = self.extract_text(file_bytes, file_type)
            
            if not original_text.strip():
                return "", "⚠️ Aucun texte trouvé dans le fichier"
            
            # Traduction
            translated_text = self.translator.translate(
                original_text, source_lang, target_lang
            )
            
            logger.info(f"✅ Fichier {file_type.upper()} traduit avec succès")
            return original_text, translated_text
            
        except Exception as e:
            logger.error(f"❌ Erreur traduction fichier: {str(e)}")
            raise


# Instance globale
file_translator = FileTranslator()
