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
    """Procesa la imagen y extrae el texto mediante OCR."""

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
# RUTAS DE IMÁGENES
# ==========================================

ASSETS = "assets"

imagenes = {
    "🪧 Señales y avisos": os.path.join(ASSETS, "senales.jpg"),
    "🍽️ Menús y restaurantes": os.path.join(ASSETS, "menus.jpg"),
    "🚌 Transporte": os.path.join(ASSETS, "transporte.jpg"),
    "🏛️ Turismo y lugares": os.path.join(ASSETS, "turismo.jpg"),
    "🛍️ Compras y productos": os.path.join(ASSETS, "compras.jpg"),
    "📄 Documentos": os.path.join(ASSETS, "documentos.jpg")
}


# ==========================================
# ESTILOS PERSONALIZADOS
# ==========================================

st.markdown(
    """
    <style>

    /* =====================================
       FONDO GENERAL
       ===================================== */

    .stApp {
        background-color: #F7F5F0;
    }


    /* =====================================
       TÍTULO TRAVELLENS
       ===================================== */

    .titulo-travel {
        font-size: 55px;
        font-weight: 800;
        margin-bottom: 0px;

        /* Fuerza el color negro */
        color: #000000 !important;

        /* Evita que Streamlit cambie el color */
        -webkit-text-fill-color: #000000 !important;
    }


    /* =====================================
       SUBTÍTULO
       ===================================== */

    .subtitulo-travel {
        font-size: 22px;
        color: #555555 !important;
        margin-top: 0px;
    }


    /* =====================================
       TARJETA DE CATEGORÍA
       ===================================== */

    .categoria-info {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E5E5E5;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #222222;
    }


    /* =====================================
       SEPARADORES
       ===================================== */

    hr {
        margin-top: 25px;
        margin-bottom: 25px;
    }


    /* =====================================
       BOTONES
       ===================================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="titulo-travel">🌍 TravelLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo-travel">'
    'Tu asistente inteligente para viajar sin barreras de idioma.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ==========================================
# IMAGEN DE PORTADA
# ==========================================

portada = os.path.join(
    ASSETS,
    "portada.jpg"
)

if os.path.exists(portada):

    st.image(
        portada,
        use_container_width=True
    )

else:

    st.warning(
        "No se encontró la imagen de portada. "
        "Agrega 'assets/portada.jpg' a tu repositorio."
    )


st.write(
    """
    **Captura, comprende y escucha.**

    TravelLens utiliza reconocimiento óptico de caracteres,
    traducción y síntesis de voz para ayudarte a comprender
    información durante tus viajes.
    """
)


# ==========================================
# CATEGORÍAS
# ==========================================

st.divider()

st.subheader("🧭 ¿Qué necesitas durante tu viaje?")

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
# IMAGEN DE CATEGORÍA
# ==========================================

imagen_categoria = imagenes[categoria]

if os.path.exists(imagen_categoria):

    st.image(
        imagen_categoria,
        caption=categoria,
        use_container_width=True
    )

else:

    st.warning(
        f"No se encontró la imagen: {imagen_categoria}"
    )


# ==========================================
# DESCRIPCIÓN DE CATEGORÍA
# ==========================================

descripciones = {

    "🪧 Señales y avisos":
        "Toma una fotografía de señales, advertencias o indicaciones para comprender rápidamente su significado.",

    "🍽️ Menús y restaurantes":
        "Fotografía un menú para reconocer y traducir los nombres de los platos y la información del restaurante.",

    "🚌 Transporte":
        "Captura horarios, rutas, estaciones o información relacionada con el transporte.",

    "🏛️ Turismo y lugares":
        "Fotografía información sobre museos, monumentos, lugares turísticos o sitios de interés.",

    "🛍️ Compras y productos":
        "Captura etiquetas, instrucciones o información de productos durante tu viaje.",

    "📄 Documentos":
        "Carga o fotografía documentos, reservas, formularios o información importante."
}


st.markdown(
    f"""
    <div class="categoria-info">
        <strong>{categoria}</strong><br><br>
        {descripciones[categoria]}
    </div>
    """,
    unsafe_allow_html=True
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

            st.session_state[
                "texto_detectado"
            ] = texto_detectado


# ==========================================
# RECUPERAR TEXTO
# ==========================================

if "texto_detectado" in st.session_state:

    texto_detectado = st.session_state[
        "texto_detectado"
    ]


# ==========================================
# MOSTRAR TEXTO
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
# SIDEBAR
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


    if st.button(
        "🌍 Traducir y escuchar"
    ):

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
