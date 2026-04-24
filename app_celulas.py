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
# 🎨 ESTILOS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #5E35B1, #7E57C2);
}

h1 {
    text-align: center;
    color: #FFD600;
    font-weight: 900;
}

.subtitle {
    text-align: center;
    color: #FFFFFF;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border-top: 6px solid #FFD600;
}

.stButton > button {
    background: linear-gradient(90deg, #FF6D00, #FFD600) !important;
    color: black !important;
    border-radius: 12px !important;
    font-weight: 900 !important;
}

.stWarning {
    background: linear-gradient(90deg, #FF6D00, #FFAB00) !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🔥 HEADER
# =========================
st.markdown("<h1>🔥 Registro de Jóvenes</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>MOVE 🚀</p>", unsafe_allow_html=True)

# =========================
# 📊 GOOGLE SHEETS
# =========================
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1YKaieMah74PhHw8-eSv7-KCnahdBOdc4pTH0AjwPdVA/edit"
).sheet1

# =========================
# 📍 DATOS
# =========================
barrios_bello = ["Niquía", "Central", "Pérez", "Quitasol", "Madera"]

lideres = [
    "P. Juan Loaiza",
    "P. Ruth Gómez",
    "P. Jhonny Rodriguez",
    "P. Mary Zuleta",
    "P. Esteban Rodriguez",
    "P. Daniela Villa"
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

    horario = st.text_input("Hora")

    modalidad = st.radio(
        "Modalidad",
        ["Presencial", "Virtual", "No asisto"]
    )

    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("📡 Modalidad virtual")
    else:
        barrio = st.selectbox("Barrio", barrios_bello)

    lider = st.selectbox("Líder", lideres)

    grupo = st.radio(
        "Célula",
        ["Caballeros", "Damas", "Mixta"],
        horizontal=True
    )

    # 👥 INVITADO
    st.markdown("### 👥 Invitado")

    tiene_invitado = st.toggle("¿Traes invitado?")

    if tiene_invitado:
        col4, col5, col6 = st.columns(3)

        with col4:
            nombre_inv = st.text_input("Nombre invitado")

        with col5:
            celular_inv = st.text_input("Celular invitado")

        with col6:
            edad_inv = st.text_input("Edad invitado")
    else:
        nombre_inv = ""
        celular_inv = ""
        edad_inv = ""

    # 🔥 BOTÓN (ESTABA FALTANDO)
    enviar = st.form_submit_button("💾 Guardar registro")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 💾 GUARDAR
# =========================
if enviar:

    if nombre.strip() == "" or celular.strip() == "":
        st.warning("⚠️ Completa los campos obligatorios")

    else:
        fecha = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M")

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
            nombre_inv,
            celular_inv,
            edad_inv,
            fecha
        ])

        st.success("🎉 Registro exitoso")
        st.balloons()
