import streamlit as st
import sqlite3
from PIL import Image
import io

# Conexión a la base de datos
def get_connection():
    conn = sqlite3.connect('salon.db')
    return conn

# Función para agregar un nuevo cliente
def agregar_cliente(nombre, telefono, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO clientes (nombre, telefono, email)
        VALUES (?, ?, ?)
    ''', (nombre, telefono, email))
    conn.commit()
    conn.close()

# Función para obtener todos los clientes
def obtener_clientes():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    conn.close()
    return clientes

# Función para agregar una nueva visita
def agregar_visita(cliente_id, fecha, servicio, costo, formula, notas, imagen):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO visitas (cliente_id, fecha, servicio, costo, formula, notas, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cliente_id, fecha, servicio, costo, formula, notas, imagen))
    conn.commit()
    conn.close()

# Función para obtener visitas por cliente
def obtener_visitas(cliente_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM visitas WHERE cliente_id = ?
    ''', (cliente_id,))
    visitas = c.fetchall()
    conn.close()
    return visitas

# Interfaz de Streamlit
st.title('Sistema de Gestión de Clientes - Salón de Belleza')

# Sección para agregar nuevo cliente
st.header('Agregar Nuevo Cliente')
nombre = st.text_input('Nombre')
telefono = st.text_input('Teléfono')
email = st.text_input('Email')
if st.button('Agregar Cliente'):
    agregar_cliente(nombre, telefono, email)
    st.success('Cliente agregado exitosamente')

# Sección para ver clientes existentes
st.header('Clientes Existentes')
clientes = obtener_clientes()
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
        agregar_visita(cliente[0], fecha, servicio, costo, formula, notas, imagen_bytes)
        st.success('Visita agregada exitosamente')
    
    # Mostrar visitas del cliente
    st.write('Historial de Visitas:')
    visitas = obtener_visitas(cliente[0])
    for visita in visitas:
        st.write(f"Fecha: {visita[2]}, Servicio: {visita[3]}, Costo: ${visita[4]:.2f}")
        st.write(f"Fórmula: {visita[5]}")
        st.write(f"Notas: {visita[6]}")
        if visita[7]:
            st.image(Image.open(io.BytesIO(visita[7])), caption='Imagen', use_column_width=True)

