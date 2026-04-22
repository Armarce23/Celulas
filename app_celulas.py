import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# =========================
# 🎨 CONFIG VISUAL
# =========================
st.set_page_config(
    page_title="Registro de Jóvenes",
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
<style>

/* Fondo general (seguro) */
.stApp {
    background-color: #420991;
}

/* Título */
h1 {
    text-align: center;
    color: #f2faf4;
}

/* Card */
.card {
    background-color: #f2faf4;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)


# =========================
# 🔥 TÍTULO
# =========================
st.markdown("<h1>Registro de Jóvenes</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#f2faf4;'>Completa tu información 💛</p>", unsafe_allow_html=True)


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
    "Niquía", "Bello Centro", "Pérez", "Madera", "Santa Ana",
    "Trapiche", "Cabañas", "Cabañitas", "Zamora", "Buenos Aires",
    "Rincón Santo", "Salento", "Paris", "La Cumbre", "Gran Avenida",
    "Andalucía", "Primavera", "El Carmelo", "La Gabriela",
    "La Selva", "Ciudad Niquía", "Altos de Niquía", "La Aldea",
    "Santa Rita", "Los Alpes", "Manchester", "El Rosario",
    "La Maruchenga", "Playa Rica", "Valadares"
]

lideres = [
    "Juan Loaiza",
    "Ruth Gómez",
    "Jhonny Rodriguez",
    "Mary Zuleta"
]


# =========================
# 🧾 FORMULARIO
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("formulario"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre completo *")

    with col2:
        celular = st.text_input("Número de celular *")

    dia = st.selectbox(
        "Día de tu célula",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    horario = st.text_input("Horario")

    modalidad = st.radio(
        "Modalidad",
        ["Presencial", "Virtual", "Ambas"]
    )

    # =========================
    # 📍 BARRIO
    # =========================
    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("📡 Modalidad virtual activada")
    else:
        barrio = st.selectbox("Selecciona el barrio en Bello", barrios_bello)

    lider = st.selectbox("Selecciona tu líder de 12", lideres)

    grupo = st.radio("Equipo", ["Hombres", "Damas"])

    # =========================
    # 🔘 BOTÓN
    # =========================
    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 💾 GUARDAR DATOS
# =========================
if enviar:
    if nombre.strip() == "" or celular.strip() == "":
        st.warning("⚠️ Completa los campos obligatorios")
    else:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

        sheet.append_row([
            nombre,
            celular,
            dia,
            horario,
            modalidad,
            barrio,
            lider,
            grupo,
            fecha
        ])

        st.success("✅ Registro guardado correctamente en la nube")
