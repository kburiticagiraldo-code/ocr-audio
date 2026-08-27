import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from googletrans import Translator


# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="TravelLens",
    page_icon="🌍",
    layout="wide"
)


# ==========================================
# FUNCIONES
# ==========================================

def remove_files(n):
    """Elimina archivos MP3 antiguos."""
    
    if not os.path.exists("temp"):
        os.makedirs("temp")

    mp3_files = glob.glob("temp/*.mp3")

    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400

        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)


def text_to_speech(input_language, output_language, text, tld):
    """Traduce un texto y genera un archivo de audio."""

    translator = Translator()

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    translated_text = translation.text

    tts = gTTS(
        translated_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    file_name = f"audio_{int(time.time())}"

    if not os.path.exists("temp"):
        os.makedirs("temp")

    audio_path = f"temp/{file_name}.mp3"

    tts.save(audio_path)

    return audio_path, translated_text


def procesar_imagen(imagen, aplicar_filtro=False):
    """Procesa la imagen y extrae el texto utilizando OCR."""

    if aplicar_filtro:
        imagen = cv2.bitwise_not(imagen)

    img_rgb = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2RGB
    )

    texto_detectado = pytesseract.image_to_string(
        img_rgb
    )

    return texto_detectado


# ==========================================
# LIMPIAR ARCHIVOS ANTIGUOS
# ==========================================

remove_files(7)


# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================

st.title("🌍 TravelLens")
st.subheader("Tu asistente inteligente de traducción para viajes")

st.write(
    """
    Captura o carga una imagen, reconoce el texto automáticamente,
    tradúcelo a otro idioma y escúchalo mediante audio.
    """
)


# ==========================================
# CATEGORÍAS
# ==========================================

st.divider()

st.subheader("🧭 ¿Qué deseas explorar?")

categoria = st.selectbox(
    "Selecciona una categoría",
    (
        "🪧 Señales y avisos",
        "🍽️ Menús y restaurantes",
        "🚌 Transporte",
        "🏛️ Turismo y lugares",
        "🛍️ Compras y productos",
        "📄 Documentos"
    )
)


# ==========================================
# INFORMACIÓN SEGÚN CATEGORÍA
# ==========================================

if categoria == "🪧 Señales y avisos":

    st.info(
        "📸 Toma una fotografía de señales, advertencias o indicaciones "
        "para comprender rápidamente su significado."
    )


elif categoria == "🍽️ Menús y restaurantes":

    st.info(
        "🍽️ Fotografía un menú para reconocer y traducir los nombres "
        "de los platos y la información del restaurante."
    )


elif categoria == "🚌 Transporte":

    st.info(
        "🚌 Captura horarios, rutas, estaciones o información "
        "relacionada con el transporte."
    )


elif categoria == "🏛️ Turismo y lugares":

    st.info(
        "🏛️ Fotografía información sobre museos, monumentos, "
        "lugares turísticos o sitios de interés."
    )


elif categoria == "🛍️ Compras y productos":

    st.info(
        "🛍️ Captura etiquetas, instrucciones o información "
        "de productos durante tu viaje."
    )


elif categoria == "📄 Documentos":

    st.info(
        "📄 Carga o fotografía documentos, reservas, formularios "
        "o información importante."
    )


# ==========================================
# CAPTURA DE IMAGEN
# ==========================================

st.divider()

st.subheader("📸 Captura la información")

tipo_captura = st.radio(
    "¿Cómo deseas obtener la imagen?",
    (
        "Usar cámara",
        "Cargar imagen"
    ),
    horizontal=True
)


imagen = None


# ==========================================
# CÁMARA
# ==========================================

if tipo_captura == "Usar cámara":

    imagen_camara = st.camera_input(
        "Toma una fotografía"
    )

    if imagen_camara is not None:

        bytes_data = imagen_camara.getvalue()

        imagen = cv2.imdecode(
            np.frombuffer(
                bytes_data,
                np.uint8
            ),
            cv2.IMREAD_COLOR
        )


# ==========================================
# CARGAR IMAGEN
# ==========================================

else:

    imagen_archivo = st.file_uploader(
        "Carga una imagen",
        type=["png", "jpg", "jpeg"]
    )

    if imagen_archivo is not None:

        bytes_data = imagen_archivo.getvalue()

        imagen = cv2.imdecode(
            np.frombuffer(
                bytes_data,
                np.uint8
            ),
            cv2.IMREAD_COLOR
        )


# ==========================================
# PROCESAMIENTO DE IMAGEN
# ==========================================

texto_detectado = ""


if imagen is not None:

    st.divider()

    st.subheader("🖼️ Imagen seleccionada")

    imagen_rgb = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2RGB
    )

    st.image(
        imagen_rgb,
        use_container_width=True
    )


    aplicar_filtro = st.checkbox(
        "Aplicar filtro de contraste"
    )


    if aplicar_filtro:

        imagen_procesada = cv2.bitwise_not(
            imagen
        )

    else:

        imagen_procesada = imagen


    # ==========================================
    # OCR
    # ==========================================

    if st.button("🔍 Reconocer texto"):

        with st.spinner(
            "Analizando la imagen..."
        ):

            texto_detectado = procesar_imagen(
                imagen,
                aplicar_filtro
            )

            st.session_state["texto_detectado"] = texto_detectado


# Recuperar texto detectado
if "texto_detectado" in st.session_state:

    texto_detectado = st.session_state[
        "texto_detectado"
    ]


# ==========================================
# MOSTRAR TEXTO DETECTADO
# ==========================================

if texto_detectado:

    st.divider()

    st.subheader("🔍 Texto detectado")

    st.text_area(
        "Texto reconocido mediante OCR",
        texto_detectado,
        height=200
    )


# ==========================================
# SIDEBAR - TRADUCCIÓN
# ==========================================

with st.sidebar:

    st.header("🌐 Traducción")


    idiomas = {
        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Francés": "fr",
        "Alemán": "de",
        "Italiano": "it",
        "Portugués": "pt"
    }


    idioma_entrada_nombre = st.selectbox(
        "Idioma del texto detectado",
        list(idiomas.keys())
    )


    idioma_salida_nombre = st.selectbox(
        "Traducir a",
        list(idiomas.keys()),
        index=1
    )


    input_language = idiomas[
        idioma_entrada_nombre
    ]

    output_language = idiomas[
        idioma_salida_nombre
    ]


    # ==========================================
    # ACENTO
    # ==========================================

    st.subheader("🔊 Configuración de voz")


    acento = st.selectbox(
        "Selecciona el acento",
        (
            "Predeterminado",
            "India",
            "Reino Unido",
            "Estados Unidos",
            "Canadá",
            "Australia",
            "Irlanda",
            "Sudáfrica"
        )
    )


    acentos = {

        "Predeterminado": "com",
        "India": "co.in",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za"

    }


    tld = acentos[acento]


    mostrar_texto = st.checkbox(
        "Mostrar traducción",
        value=True
    )


# ==========================================
# TRADUCIR Y GENERAR AUDIO
# ==========================================

if texto_detectado:

    st.divider()

    st.subheader("🌐 Traducción y audio")


    if st.button("🌍 Traducir y escuchar"):

        with st.spinner(
            "Traduciendo y generando audio..."
        ):

            try:

                audio_path, texto_traducido = (
                    text_to_speech(
                        input_language,
                        output_language,
                        texto_detectado,
                        tld
                    )
                )


                st.success(
                    "¡Traducción completada!"
                )


                if mostrar_texto:

                    st.subheader(
                        "🌐 Texto traducido"
                    )

                    st.write(
                        texto_traducido
                    )


                st.subheader(
                    "🔊 Escuchar traducción"
                )


                with open(
                    audio_path,
                    "rb"
                ) as audio_file:

                    audio_bytes = (
                        audio_file.read()
                    )


                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )


            except Exception as e:

                st.error(
                    "Ocurrió un error durante "
                    "la traducción o generación "
                    "del audio."
                )

                st.write(e)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🌍 TravelLens | Reconocimiento de texto, "
    "traducción y audio para viajeros"
)

 
    
    
