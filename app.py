import streamlit as st
from PIL import Image
import io
import db
from datetime import date

# Inicializar la base de datos
db.init_db()

# Interfaz de Streamlit
st.title('Sistema de Gestión de Clientes - Salón de Belleza')

# Sección para agregar nuevo cliente
st.header('Agregar Nuevo Cliente')
nombre = st.text_input('Nombre')
telefono = st.text_input('Teléfono')
fecha_registro = st.date_input('Fecha de Registro', value=date.today())
servicio = st.text_input('Servicio')
costo = st.number_input('Costo', min_value=0.0, format="%.2f")
formula = st.text_area('Fórmula Utilizada')
notas = st.text_area('Notas')
imagen_cliente = st.file_uploader('Subir Imagen del Cliente', type=['jpg', 'jpeg', 'png'])

imagen_cliente_bytes = None
if imagen_cliente:
    imagen_cliente_bytes = imagen_cliente.read()

if st.button('Agregar Cliente'):
    db.agregar_cliente(nombre, telefono, fecha_registro.isoformat(), imagen_cliente_bytes)
    st.success('Cliente agregado exitosamente')

# Sección para registrar visitas de clientes existentes
st.header('Registrar Visitas de Clientes')
clientes = db.obtener_clientes()
clientes_dict = {f"{cliente[1]} (ID: {cliente[0]})": cliente[0] for cliente in clientes}
cliente_seleccionado = st.selectbox('Seleccionar Cliente', options=list(clientes_dict.keys()))

if cliente_seleccionado:
    cliente_id = clientes_dict[cliente_seleccionado]
    
    st.subheader(f'Registrar Visita para {cliente_seleccionado}')
    fecha_visita = st.date_input('Fecha de Visita', value=date.today())
    servicio = st.text_input('Servicio')
    costo = st.number_input('Costo', min_value=0.0, format="%.2f")
    formula = st.text_area('Fórmula Utilizada')
    notas = st.text_area('Notas')
    imagen_visita = st.file_uploader('Subir Imagen del Servicio', type=['jpg', 'jpeg', 'png'])

    imagen_visita_bytes = None
    if imagen_visita:
        imagen_visita_bytes = imagen_visita.read()

    if st.button(f'Agregar Visita para {cliente_seleccionado}'):
        db.agregar_visita(cliente_id, fecha_visita.isoformat(), servicio, costo, formula, notas, imagen_visita_bytes)
        st.success('Visita agregada exitosamente')
    
    # Mostrar historial de visitas del cliente
    st.subheader('Historial de Visitas')
    visitas = db.obtener_visitas(cliente_id)
    for visita in visitas:
        st.write(f"Fecha: {visita[2]}, Servicio: {visita[3]}, Costo: ${visita[4]:.2f}")
        st.write(f"Fórmula: {visita[5]}")
        st.write(f"Notas: {visita[6]}")
        if visita[7]:
            st.image(Image.open(io.BytesIO(visita[7])), caption='Imagen del Servicio', use_column_width=True)

# Sección para buscar visitas por fecha
st.header('Buscar Visitas por Fecha')
fecha_busqueda = st.date_input('Seleccionar Fecha')
if st.button('Buscar Visitas'):
    visitas = db.buscar_visitas_por_fecha(fecha_busqueda.isoformat())
    if visitas:
        st.write(f"Visitas para la fecha {fecha_busqueda}:")
        for visita in visitas:
            st.write(f"Cliente ID: {visita[1]}, Fecha: {visita[2]}, Servicio: {visita[3]}, Costo: ${visita[4]:.2f}")
            st.write(f"Fórmula: {visita[5]}")
            st.write(f"Notas: {visita[6]}")
            if visita[7]:
                st.image(Image.open(io.BytesIO(visita[7])), caption='Imagen del Servicio', use_column_width=True)
    else:
        st.write(f"No se encontraron visitas para la fecha {fecha_busqueda}.")

