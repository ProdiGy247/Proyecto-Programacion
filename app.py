import streamlit as st
from PIL import Image
import io
import db

# Inicializar la base de datos
db.init_db()

# Interfaz de Streamlit
st.title('Sistema de Gestión de Clientes - Salón de Belleza')

# Sección para agregar nuevo cliente
st.header('Agregar Nuevo Cliente')
nombre = st.text_input('Nombre')
telefono = st.text_input('Teléfono')
email = st.text_input('Email')
if st.button('Agregar Cliente'):
    db.agregar_cliente(nombre, telefono, email)
    st.success('Cliente agregado exitosamente')

# Sección para ver clientes existentes
st.header('Clientes Existentes')
clientes = db.obtener_clientes()
for cliente in clientes:
    st.subheader(f"{cliente[1]} (ID: {cliente[0]})")
    st.write(f"Teléfono: {cliente[2]}")
    st.write(f"Email: {cliente[3]}")
    
    # Sección para agregar una visita
    st.write('Agregar Visita:')
    fecha = st.date_input('Fecha')
    servicio = st.text_input('Servicio')
    costo = st.number_input('Costo', min_value=0.0, format="%.2f")
    formula = st.text_area('Fórmula Utilizada')
    notas = st.text_area('Notas')
    imagen = st.file_uploader('Subir Imagen', type=['jpg', 'jpeg', 'png'])
    
    imagen_bytes = None
    if imagen:
        imagen_bytes = imagen.read()
    
    if st.button(f'Agregar Visita para {cliente[1]}'):
        db.agregar_visita(cliente[0], fecha, servicio, costo, formula, notas, imagen_bytes)
        st.success('Visita agregada exitosamente')
    
    # Mostrar visitas del cliente
    st.write('Historial de Visitas:')
    visitas = db.obtener_visitas(cliente[0])
    for visita in visitas:
        st.write(f"Fecha: {visita[2]}, Servicio: {visita[3]}, Costo: ${visita[4]:.2f}")
        st.write(f"Fórmula: {visita[5]}")
        st.write(f"Notas: {visita[6]}")
        if visita[7]:
            st.image(Image.open(io.BytesIO(visita[7])), caption='Imagen', use_column_width=True)


