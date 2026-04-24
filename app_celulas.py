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

/* Fondo */
.stApp {
    background: linear-gradient(135deg, #5E35B1, #7E57C2);
}

/* Título */
h1 {
    text-align: center;
    color: #FFD600;
    font-weight: 900;
    font-size: 2.5rem;
}

/* Subtítulo */
.subtitle {
    text-align: center;
    color: #FFFFFF;
    margin-bottom: 20px;
}

/* Card */
.card {
    background: white;
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

/* Botón */
.stButton > button {
    background: linear-gradient(90deg, #FF6D00, #FFD600) !important;
    color: #000 !important;
    border-radius: 12px !important;
    font-weight: 900 !important;
    padding: 12px !important;
    border: none !important;
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* Modalidad bonita */
div[role="radiogroup"] {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 15px;
}

div[role="radiogroup"] label {
    background: #F5F5F5 !important;
    padding: 10px 16px !important;
    border-radius: 20px !important;
}

/* Seleccionado */
div[role="radiogroup"] label[data-selected="true"] {
    background: #FFD600 !important;
    color: #000 !important;
    font-weight: 800;
}

/* Warning */
.stWarning {
    background: linear-gradient(90deg, #FF6D00, #FFAB00) !important;
    color: #000 !important;
    font-weight: 800;
    border-radius: 12px;
    padding: 12px;
    border-left: 6px solid #000;
}

/* Success */
.stSuccess {
    background: #FFD600 !important;
    color: #000 !important;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🔥 HEADER
# =========================
st.markdown("<h1>🔥 Registro de Jóvenes</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>MOVE 🔥 ¡Nada nos detiene!</p>", unsafe_allow_html=True)

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
barrios_bello = [
    "Niquía", "Central", "Pérez", "Quitasol", "Madera", "Santa Ana",
    "Trapiche", "Cabañas", "Cabañitas", "Serramonte", "Zamora"
]

lideres = [
    "P. Juan Loaiza",
    "P. Ruth Gómez",
    "P. Jhonny Rodriguez",
    "P. Mary Zuleta",
    "P. Esteban Rodriguez",
    "P. Daniela Villa"
]

# =========================
# =========================
# 👥 CONTROL INVITADO (FUERA DEL FORM)
# =========================
tiene_invitado = st.checkbox("👥 ¿Traes invitado?")

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
        ["Presencial", "Virtual", "No asisto"]
    )

    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("📡 Modalidad virtual activada")
    else:
        barrio = st.selectbox("Barrio en Bello", barrios_bello)

    lider = st.selectbox("Líder de 12", lideres)

    grupo = st.radio(
        "Célula",
        ["Caballeros", "Damas", "Mixta"],
        horizontal=True
    )

    # 👇 INVITADO DENTRO DEL FORM PERO CONTROLADO DESDE AFUERA
    if tiene_invitado:
        st.markdown("---")
        st.markdown("### 👥 Invitado")

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

    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

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

        st.success("🎉 ¡Joven registrado con éxito!")
        st.balloons()
