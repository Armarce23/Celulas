import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Registro de Jóvenes", page_icon="🔥")

# --- CONEXIÓN GOOGLE SHEETS ---
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


# --- UI ---
st.title("🔥 Registro de Jóvenes")
st.markdown("Completa tu información 💛")

# =========================
# 📍 LISTAS
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
# 🧾 FORMULARIO (CORREGIDO)
# =========================
with st.form("formulario"):

    nombre = st.text_input("Nombre completo *")
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

    # --- Barrio condicional ---
    if modalidad == "Virtual":
        barrio = "VIRTUAL"
        st.info("Barrio: VIRTUAL")
    else:
        barrio = st.selectbox(
            "Selecciona el barrio en Bello",
            barrios_bello
        )

    # --- líder y grupo ---
    lider = st.selectbox("Selecciona tu líder de 12", lideres)

    grupo = st.radio(
        "Equipo",
        ["Hombres", "Damas"]
    )

    # 🔥 BOTÓN OBLIGATORIO DEL FORM
    enviar = st.form_submit_button("Guardar registro")


# =========================
# 💾 GUARDAR EN SHEETS
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

        st.success("✅ Registro guardado en la nube")
