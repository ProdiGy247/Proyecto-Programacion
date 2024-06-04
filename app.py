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
imagen_cliente = st.file_uploader('Subir Imagen del Cliente', type=['jpg', 'jpeg', 'png'])

imagen_cliente_bytes = None
if imagen_cliente:
    imagen_cliente_bytes = imagen_cliente.read()

if st.button('Agregar Cliente'):
    db.agregar_cliente(nombre, telefono, fecha_registro.isoformat(), imagen_cliente_bytes)
    st.success('Cliente agregado exitosamente')

# Sección para ver clientes existentes
st.header('Clientes Existentes')
clientes = db.obtener_clientes()
for cliente in clientes:
    st.subheader(f"{cliente[1]} (ID: {cliente[0]})")
    st.write(f"Teléfono: {cliente[2]}")
    st.write(f"Fecha de Registro: {cliente[3]}")
    st.write(f"Fecha de Primera Visita: {cliente[4]}")
    if cliente[5]:
        st.image(Image.open(io.BytesIO(cliente[5])), caption='Imagen del Cliente', use_column_width=True)
    
    # Sección para agregar una visita
    st.write('Agregar Visita:')
    fecha = st.date_input('Fecha')
    servicio = st.text_input('Servicio')
    costo = st.number_input('Costo', min_value=0.0, format="%.2f")
    formula = st.text_area('Fórmula Utilizada')
    notas = st.text_area('Notas')
    imagen_visita = st.file_uploader('Subir Imagen del Servicio', type=['jpg', 'jpeg', 'png'])
    
    imagen_visita_bytes = None
    if imagen_visita:
        imagen_visita_bytes = imagen_visita.read()
    
    if st.button(f'Agregar Visita para {cliente[1]}'):
        db.agregar_visita(cliente[0], fecha.isoformat(), servicio, costo, formula, notas, imagen_visita_bytes)
        st.success('Visita agregada exitosamente')
    
    # Mostrar visitas del cliente
    st.write('Historial de Visitas:')
    visitas = db.obtener_visitas(cliente[0])
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
