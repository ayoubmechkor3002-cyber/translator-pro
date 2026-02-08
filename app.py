"""
TRANSLATOR PRO - Application de Traduction Multilingue
Interface Streamlit avec traduction de texte, images, fichiers et audio
"""
import streamlit as st
from PIL import Image
import io

# Import des modules
from utils.text_translator import text_translator
from utils.image_translator import image_translator
from utils.file_translator import file_translator
from utils.audio_translator import audio_translator

# Configuration de la page
st.set_page_config(
    page_title="Translator Pro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger le CSS personnalisé
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Fichier CSS non trouvé. Utilisation du style par défaut.")

load_css()

# Langues supportées
LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en",
    "🇸🇦 العربية": "ar",
    "🇪🇸 Español": "es",
    "🇩🇪 Deutsch": "de",
    "🇮🇹 Italiano": "it",
}

# En-tête de l'application
def render_header():
    st.markdown("""
        <div class="header-container">
            <h1 class="app-title">🌍 Translator AH</h1>
            <p class="app-subtitle">Traduction Multilingue Intelligente</p>
        </div>
    """, unsafe_allow_html=True)

render_header()

# Sélection des langues dans la sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    source_lang_name = st.selectbox(
        " Langue source",
        options=list(LANGUAGES.keys()),
        index=0
    )
    source_lang = LANGUAGES[source_lang_name]
    
    target_lang_name = st.selectbox(
        " Langue cible",
        options=list(LANGUAGES.keys()),
        index=1
    )
    target_lang = LANGUAGES[target_lang_name]
    
    st.divider()
    
    st.markdown("""
    ### 📖 Guide d'utilisation
    
    **📝 Texte**: Collez ou tapez votre texte
    
    **🖼️ Image**: Uploadez une image avec du texte (OCR)
    
    **📄 Fichier**:  TXT, PDF, DOCX
    
    **🎤 Audio**:  MP3, WAV, OGG
    
    ---
    

    
    ---
    
    <div style="text-align: center; color: #7f8c8d;">
        <p><strong>Translator AH v1.0</strong></p>
        <p>Développé par MECHKOR Ayoub</p>
    </div>
    """, unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Texte", 
    "🖼️ Image", 
    "📄 Fichier", 
    "🎤 Audio"
])

# ========== ONGLET TEXTE ==========
with tab1:
    st.markdown("### 📝 Traduction de Texte")
    st.markdown("Entrez votre texte ci-dessous. La structure (paragraphes, ponctuation) sera préservée.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Texte Original")
        input_text = st.text_area(
            "Texte à traduire",
            height=300,
            placeholder="Entrez votre texte ici...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### 📤 Traduction")
        translation_placeholder = st.empty()
    
    if st.button("🚀 Traduire le texte", use_container_width=True):
        if not input_text.strip():
            st.error("⚠️ Veuillez entrer du texte à traduire")
        elif source_lang == target_lang:
            st.warning("⚠️ Les langues source et cible doivent être différentes")
        else:
            try:
                with st.spinner("🔄 Traduction en cours..."):
                    translated = text_translator.translate(
                        input_text, source_lang, target_lang
                    )
                    translation_placeholder.text_area(
                        "Résultat",
                        value=translated,
                        height=300,
                        label_visibility="collapsed"
                    )
                st.success("✅ Traduction réussie!")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# ========== ONGLET IMAGE ==========
with tab2:
    st.markdown("### 🖼️ Traduction depuis Image (OCR)")
    st.markdown("Uploadez une image contenant du texte. Le texte sera extrait et traduit.")
    
    uploaded_image = st.file_uploader(
        "Choisir une image",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Formats supportés: PNG, JPG, JPEG, BMP, TIFF"
    )
    
    if uploaded_image:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🖼️ Image Uploadée")
            image = Image.open(uploaded_image)
            st.image(image, use_container_width=True)
        
        with col2:
            st.markdown("#### 📤 Texte Traduit")
            result_placeholder = st.empty()
        
        if st.button("🔍 Extraire et Traduire", use_container_width=True):
            if source_lang == target_lang:
                st.warning("⚠️ Les langues source et cible doivent être différentes")
            else:
                try:
                    with st.spinner("🔄 Extraction et traduction en cours..."):
                        translated = image_translator.translate_image(
                            image, source_lang, target_lang
                        )
                        result_placeholder.text_area(
                            "Résultat",
                            value=translated,
                            height=300,
                            label_visibility="collapsed"
                        )
                    st.success("✅ Image traduite avec succès!")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")

# ========== ONGLET FICHIER ==========
with tab3:
    st.markdown("### 📄 Traduction de Fichiers")
    st.markdown("Uploadez un document. Le contenu sera extrait et traduit.")
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=['txt', 'pdf', 'docx'],
        help="Formats supportés: TXT, PDF, DOCX"
    )
    
    if uploaded_file:
        file_details = {
            "Nom": uploaded_file.name,
            "Type": uploaded_file.type,
            "Taille": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        with st.expander("📋 Détails du fichier"):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        if st.button("📖 Traduire le fichier", use_container_width=True):
            if source_lang == target_lang:
                st.warning("⚠️ Les langues source et cible doivent être différentes")
            else:
                try:
                    with st.spinner("🔄 Extraction et traduction en cours..."):
                        file_bytes = uploaded_file.read()
                        file_ext = uploaded_file.name.split('.')[-1]
                        
                        original, translated = file_translator.translate_file(
                            file_bytes, file_ext, source_lang, target_lang
                        )
                    
                    st.success("✅ Fichier traduit avec succès!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📥 Texte Original")
                        st.text_area(
                            "Original",
                            value=original[:5000],  # Limiter l'affichage
                            height=300,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        st.markdown("#### 📤 Traduction")
                        st.text_area(
                            "Traduit",
                            value=translated[:5000],
                            height=300,
                            label_visibility="collapsed"
                        )
                    
                    # Bouton de téléchargement
                    st.download_button(
                        label="💾 Télécharger la traduction",
                        data=translated,
                        file_name=f"translated_{uploaded_file.name.split('.')[0]}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")

# ========== ONGLET AUDIO ==========
with tab4:
    st.markdown("### 🎤 Traduction depuis Audio")
    st.markdown("Uploadez un fichier audio. La parole sera transcrite puis traduite.")
    
    uploaded_audio = st.file_uploader(
        "Choisir un fichier audio",
        type=['mp3', 'wav', 'ogg', 'flac', 'm4a'],
        help="Formats supportés: MP3, WAV, OGG, FLAC, M4A"
    )
    
    if uploaded_audio:
        st.audio(uploaded_audio, format=f"audio/{uploaded_audio.name.split('.')[-1]}")
        
        audio_details = {
            "Nom": uploaded_audio.name,
            "Type": uploaded_audio.type,
            "Taille": f"{uploaded_audio.size / 1024:.2f} KB"
        }
        
        with st.expander("📋 Détails du fichier audio"):
            for key, value in audio_details.items():
                st.write(f"**{key}:** {value}")
        
        if st.button("🎧 Transcrire et Traduire", use_container_width=True):
            if source_lang == target_lang:
                st.warning("⚠️ Les langues source et cible doivent être différentes")
            else:
                try:
                    with st.spinner("🔄 Transcription et traduction en cours... (peut prendre quelques instants)"):
                        audio_bytes = uploaded_audio.read()
                        audio_format = uploaded_audio.name.split('.')[-1]
                        
                        # Transcription
                        transcribed = audio_translator.transcribe_audio(
                            audio_bytes, audio_format, source_lang
                        )
                        
                        # Traduction
                        translated = text_translator.translate(
                            transcribed, source_lang, target_lang
                        )
                    
                    st.success("✅ Audio transcrit et traduit avec succès!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🎤 Transcription")
                        st.text_area(
                            "Transcrit",
                            value=transcribed,
                            height=200,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        st.markdown("#### 📤 Traduction")
                        st.text_area(
                            "Traduit",
                            value=translated,
                            height=200,
                            label_visibility="collapsed"
                        )
                    
                    # Bouton de téléchargement
                    st.download_button(
                        label="💾 Télécharger la traduction",
                        data=translated,
                        file_name=f"translated_{uploaded_audio.name.split('.')[0]}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>🌍 Translator AH</strong> - Traduction multilingue intelligente</p>
</div>
""", unsafe_allow_html=True)
