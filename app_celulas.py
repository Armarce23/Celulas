import streamlit as st
import gspread
import pytz
from google.oauth2.service_account import Credentials
from datetime import datetime

# =========================
# 🎨 CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="Registro de Jóvenes",
    page_icon="🔥",
    layout="centered"
)

# =========================
# 🎨 ESTILOS (NUEVO DISEÑO)
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #5E35B1, #7E57C2);
}

/* Título */
h1 {
    text-align: center;
    color: #FFD600;
    font-weight: 900;
    font-size: 2.5rem;
    letter-spacing: 2px;
}

/* Subtítulo */
.subtitle {
    text-align: center;
    color: #FFFFFF;
    font-size: 1.2rem;
    margin-bottom: 20px;
}

/* Tarjeta */
.card {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    border-top: 6px solid #FFD600;
}

/* Labels */
label {
    color: #212121 !important;
    font-weight: 700 !important;
}

/* Inputs */
input, textarea, select {
    border-radius: 10px !important;
}

/* Botón */
.stButton > button {
    background: linear-gradient(90deg, #FF6D00, #FFD600) !important;
    color: #000000 !important;
    border-radius: 12px !important;
    font-weight: 900 !important;
    padding: 12px !important;
    border: none !important;
    font-size: 1.1rem !important;
    transition: 0.3s !important;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
}

/* Radios */
div[role="radiogroup"] > label {
    background: #F5F5F5;
    padding: 8px 12px;
    border-radius: 10px;
    margin-right: 5px;
}

/* Mensajes */
.stSuccess {
    background-color: #FFD600 !important;
    color: #000 !important;
    font-weight: bold;
}

.stWarning {
    background-color: #FF6D00 !important;
    color: #fff !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🔥 HEADER
# =========================
st.markdown("<h1>🔥 Registro de Jóvenes</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>MOVE 🔥 ¡Estamos creciendo juntos!</p>",
    unsafe_allow_html=True
)

st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <span style="
        background:#FFD600;
        color:#000;
        padding:8px 15px;
        border-radius:20px;
        font-weight:800;
    ">
        🚀 BIENVENIDO A MOVE
    </span>
</div>
""", unsafe_allow_html=True)

# =========================
# 📊 GOOGLE SHEETS
# =========================
creds_dict = st.secrets["gcp_service_account"]

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1YKaieMah74PhHw8-eSv7-KCnahdBOdc4pTH0AjwPdVA/edit?usp=sharing"
).sheet1

# =========================
# 📍 DATOS
# =========================
barrios_bello = [
    "Niquía", "Central", "Pérez", "Quitasol", "Madera", "Santa Ana",
    "Trapiche", "Cabañas", "Cabañitas", "Serramonte", "Zamora",
    "Buenos Aires", "Espiritu Santo", "Salento", "Paris", "La Cumbre",
    "Gran Avenida", "Andalucía", "Primavera", "El Carmelo",
    "La Gabriela", "La Selva", "Ciudad Niquía", "Altos de Niquía",
    "La Aldea", "Santa Rita", "Los Alpes", "Manchester",
    "El Rosario", "La Maruchenga", "Playa Rica", "Valadares"
]

lideres = [
    "Juan Loaiza",
    "Ruth Gómez",
    "Jhonny Rodriguez",
    "Mary Zuleta"
]

# =========================
# 📝 FORMULARIO
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("formulario"):

    col1, col2, col3 = st.columns(3)

    with col1:
        nombre = st.text_input("Nombre completo *")

    with col2:
        celular = st.text_input("Número de celular *")

    with col3:
        edad = st.text_input("Edad *")

    dia = st.selectbox(
        "Día de tu célula",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    horario = st.text_input("Hora (Ej: 7:30 PM)")

    modalidad = st.radio(
        "Modalidad",
        ["Presencial", "Virtual", "Ambas"]
    )

    # 🔥 Barrio automático
    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("📡 Modalidad virtual activada")
    else:
        barrio = st.selectbox("Selecciona el barrio en Bello", barrios_bello)

    lider = st.selectbox("Selecciona tu líder de 12", lideres)

    grupo = st.radio(
        "Célula",
        ["Caballeros", "Damas", "Mixta"],
        horizontal=True
    )

    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 💾 GUARDAR
# =========================
if enviar:

    if nombre.strip() == "" or celular.strip() == "":
        st.markdown("""
<style>

/* ⚠️ WARNING MEJORADO */
.stWarning {
    background: linear-gradient(90deg, #FF6D00, #FFAB00) !important;
    color: #000 !important;
    font-weight: 800;
    border-radius: 12px;
    padding: 12px;
    border-left: 6px solid #000;
}

</style>
""", unsafe_allow_html=True)

    else:
        zona_horaria = pytz.timezone('America/Bogota')
        fecha = datetime.now(zona_horaria).strftime("%Y-%m-%d %H:%M")

        sheet.append_row([
            nombre,
            celular,
            edad,
            dia,
            horario,
            modalidad,
            barrio,
            lider,
            grupo,
            fecha
        ])

        st.success("🎉 ¡Joven registrado con éxito!")
        st.balloons()
