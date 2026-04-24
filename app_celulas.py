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
        barrio = st.selectbox("Selecciona el barrio en Bello", barrios_bello)

    lider = st.selectbox("Selecciona tu líder de 12", lideres)

    grupo = st.radio(
        "Célula",
        ["Caballeros", "Damas", "Mixta"],
        horizontal=True
    )

    # =========================
    # 👥 INVITADO (CORREGIDO)
    # =========================
    st.markdown("---")
    st.markdown("### 👥 Invitado")

    tiene_invitado = st.checkbox("¿Traes invitado?")

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

    enviar = st.form_submit_button("💾 Guardar registro", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
