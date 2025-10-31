import os
import streamlit as st
import base64
from openai import OpenAI

# Estilo visual con temática oceánica
st.markdown("""
    <style>
        body {
            background-color: #e0f7fa;  /* Azul claro del océano */
            color: #00796b;  /* Texto en verde mar */
        }
        .stTitle {
            color: #004d40;  /* Título en verde océano oscuro */
        }
        .stSubheader {
            color: #0077b6;  /* Azul océano para los subtítulos */
        }
        .stButton>button {
            background-color: #004d40;  /* Botones de color verde mar */
            color: white;  /* Texto blanco en el botón */
        }
        .stImage>div>img {
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSidebar {
            background-color: #00897b;  /* Barra lateral verde suave */
        }
        .stTextInput>div>div>input {
            background-color: #80d0c7;  /* Fondo de los campos de texto en verde suave */
        }
        .stTextArea>div>div>textarea {
            background-color: #80d0c7;  /* Fondo del área de texto */
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación con emojis
st.title("🌊 **Análisis de Imagen: Inteligencia Artificial en Acción** 🤖")

# Mostrar la versión de Python
st.write("👨‍💻 **Versión de Python**:", platform.python_version())

# Cargar y mostrar imagen relacionada con la tecnología oceánica
try:
    image = Image.open('Chat_pdf.png')  # Asegúrate de que esta imagen esté disponible
    st.image(image, width=350)
except Exception as e:
    st.warning(f"⚠️ No se pudo cargar la imagen: {e}")

# Barra lateral con descripción
with st.sidebar:
    st.subheader("🌊 **Este agente te ayudará a analizar la imagen cargada**")
    st.write("""
    Sube una imagen y pregunta sobre su contenido. El agente procesará la imagen usando IA y generará respuestas.
    """)

# Clave API de OpenAI
ke = st.text_input('🔑 **Ingresa tu Clave de OpenAI**', type="password")
os.environ['OPENAI_API_KEY'] = ke

# Recuperar la clave de API de OpenAI
api_key = os.environ['OPENAI_API_KEY']

# Inicializar cliente de OpenAI
client = OpenAI(api_key=api_key)

# Cargar archivo de imagen
uploaded_file = st.file_uploader("📥 **Sube una imagen**", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Mostrar imagen cargada
    with st.expander("Imagen cargada", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Toggle para mostrar detalles adicionales
show_details = st.checkbox("🔍 **Pregunta algo específico sobre la imagen**", value=False)

if show_details:
    # Entrada de texto para detalles adicionales, solo si se activa el toggle
    additional_details = st.text_area(
        "📝 **Añade contexto sobre la imagen aquí**:",
        disabled=not show_details
    )

# Botón para activar el análisis
analyze_button = st.button("🔍 **Analizar Imagen**", type="secondary")

# Verificar si se cargó una imagen, si la clave de API está disponible, y si se presionó el botón
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("🔄 **Analizando...**"):
        # Codificar la imagen
        base64_image = encode_image(uploaded_file)
    
        prompt_text = "Describe lo que ves en la imagen en español"
    
        if show_details and additional_details:
            prompt_text += (
                f"\n\n**Contexto adicional proporcionado por el usuario:**\n{additional_details}"
            )
    
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]
    
        
        try:
            
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4", messages=messages,   
                max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
    
        except Exception as e:
            st.error(f"❌ **Ocurrió un error**: {e}")
else:
    
    if not uploaded_file and analyze_button:
        st.warning("⚠️ **Por favor sube una imagen.**")
    if not api_key:
        st.warning("⚠️ **Por favor ingresa tu clave de API.**")

