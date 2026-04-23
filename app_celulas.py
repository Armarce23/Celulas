import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# =========================
# 🎨 CONFIGURACIÓN VISUAL
# =========================
# Paleta: Verde (#00C853), Morado (#6200EA), Blanco (#FFFFFF), Negro (#121212)
st.markdown("""
<style>
    /* Fondo de toda la aplicación */
    .stApp {
        background-color: #E8F5E9; 
    }

    /* Título principal */
    h1 {
        text-align: center;
        color: #6200EA;
        font-weight: 800;
    }

    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #121212;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }

    /* Estilo del banner negro interno */
    .banner-move {
        background-color: #121212; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 25px;
        border-left: 5px solid #6200EA; /* Detalle morado lateral */
    }

    .banner-text {
        color: #00C853; 
        text-align: center; 
        margin: 0; 
        font-family: 'Arial Black', sans-serif; 
        letter-spacing: 3px;
        font-size: 1.4rem;
    }

    /* Ajuste de color para los textos de los campos */
    label {
        color: #121212 !important;
        font-weight: bold !important;
    }

    /* Botón principal */
    .stButton > button {
        background-color: #6200EA !important; 
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s !important;
    }

    .stButton > button:hover {
        background-color: #3700B3 !important;
        transform: scale(1.02);
    }
    
    /* Etiquetas de inputs */
    label {
        color: #121212 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Registro de Jóvenes",
    page_icon="🔥",
    layout="centered"
)

# =========================
# 🔥 HEADER
# =========================
st.markdown("<h1>Registro de Jóvenes</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>¡Completa tu información, juntos veremos la promesa en <b>NUESTRA IGLESIA</b>! 🔥</p>", unsafe_allow_html=True)

# =========================
# 📊 GOOGLE SHEETS
# =========================
# (Mantén tu lógica de credenciales aquí)
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1YKaieMah74PhHw8-eSv7-KCnahdBOdc4pTH0AjwPdVA/edit?usp=sharing").sheet1

# =========================
# 📍 DATOS Y FORMULARIO
# =========================
barrios_bello = ["Niquía", "Central", "Pérez", "Quitasol", "Madera", "Santa Ana", "Trapiche", "Cabañas", "Cabañitas", "Serramonte", "Zamora", "Buenos Aires", "Espiritu Santo", "Salento", "Paris", "La Cumbre", "Gran Avenida", "Andalucía", "Primavera", "El Carmelo", "La Gabriela", "La Selva", "Ciudad Niquía", "Altos de Niquía", "La Aldea", "Santa Rita", "Los Alpes", "Manchester", "El Rosario", "La Maruchenga", "Playa Rica", "Valadares"]
lideres = ["Juan Loaiza", "Ruth Gómez", "Jhonny Rodriguez", "Mary Zuleta"]

st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("formulario"):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.text_input("Nombre completo *")
    with col2:
        celular = st.text_input("Número de celular *")
    with col3:
        edad = st.text_input("Edad *")

    dia = st.selectbox("Día de tu célula", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
    horario = st.text_input("Hora <b>Ejemplo: 7:30</b>")
    modalidad = st.radio("Modalidad", ["Presencial", "Virtual", "Ambas"])

    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("📡 Modalidad virtual activada")
    else:
        barrio = st.selectbox("Selecciona el barrio en Bello", barrios_bello)

    lider = st.selectbox("Selecciona tu líder de 12", lideres)
    grupo = st.radio("Célula", ["Caballeros", "Damas", "Mixta"], horizontal=True)

    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 💾 LÓGICA DE GUARDADO
# =========================
if enviar:
    if nombre.strip() == "" or celular.strip() == "":
        st.warning("⚠️ Completa los campos obligatorios")
    else:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.append_row([nombre, celular, edad, dia, horario, modalidad, barrio, lider, grupo, fecha])
        st.success("✅ ¡Joven registrado con éxito!")
