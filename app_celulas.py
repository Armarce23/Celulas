import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Registro de Jóvenes", page_icon="🔥")

# --- CONEXIÓN GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\Arley Martinez\Desktop\Programar\Registro de Jovenes\credenciales.json",
    scope
)
client = gspread.authorize(creds)

sheet = client.open("Registro Jóvenes").sheet1

# --- UI ---
st.title("🔥 Registro de Jóvenes")
st.markdown("Completa tu información 💛")

# --- FORM ---
with st.form("formulario"):

    nombre = st.text_input("Nombre completo *")
    celular = st.text_input("Número de celular *")

    dia = st.selectbox("Día de tu célula",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    horario = st.text_input("Horario")

    modalidad = st.radio("Modalidad",
        ["Presencial", "Virtual", "Ambas"]
    )

    barrio = st.text_input('Barrio (o escribe "VIRTUAL")')

    lideres = [
    "Juan Loaiza",
    "Ruth Gómez",
    "Jhonny Rodriguez",
    "Mary Zuleta"
]

    lider = st.selectbox("Selecciona tu líder de 12", lideres)

    grupo = st.radio("Equipo",
        ["Hombres", "Damas"]
    )

    enviar = st.form_submit_button("Guardar")

# --- GUARDAR EN GOOGLE SHEETS ---
if enviar:
    if nombre.strip() == "" or celular.strip() == "":
        st.warning("⚠️ Completa los campos obligatorios")
    else:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

        sheet.append_row([
            nombre, celular, dia, horario,
            modalidad, barrio, lider, grupo, fecha
        ])

        st.success("✅ Registro guardado en la nube")