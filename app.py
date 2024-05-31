import streamlit as st
import pandas as pd
from db import insertar_cliente, obtener_datos

# Título de la aplicación
st.title("Gestión de Clientes - Salón de Belleza")

# Formulario para agregar clientes
st.header("Agregar nuevo cliente")
nombre = st.text_input("Nombre del Cliente", key="nombre_cliente")
servicio = st.text_input("Servicio Realizado", key="servicio_cliente")
costo = st.number_input("Costo del Servicio", min_value=0.0, format="%.2f", key="costo_servicio")
fecha = st.date_input("Fecha de Visita", key="fecha_visita")
atendido_por = st.text_input("Atendido por", key="atendido_por")
formula_tinte = st.text_area("Fórmula del Tinte", key="formula_tinte")

if st.button("Agregar Cliente", key="btn_agregar_cliente"):
    if not nombre or not servicio or not atendido_por or not formula_tinte:
        st.error("Por favor, completa todos los campos obligatorios.")
    else:
        insertar_cliente(nombre, servicio, costo, fecha.strftime('%Y-%m-%d'), atendido_por, formula_tinte)
        st.success("Cliente agregado exitosamente!")

# Mostrar los datos en una tabla
st.header("Clientes Registrados")
datos = obtener_datos()
st.dataframe(datos)

# Filtrado y búsqueda
st.header("Buscar Clientes")
buscar_nombre = st.text_input("Buscar por nombre", key="buscar_nombre")
filtrar_servicio = st.selectbox("Filtrar por servicio", ["Todos"] + datos["servicio"].unique().tolist(), key="filtrar_servicio")

# Filtrar datos
datos_filtrados = datos
if buscar_nombre:
    datos_filtrados = datos_filtrados[datos_filtrados["nombre"].str.contains(buscar_nombre, case=False)]
if filtrar_servicio != "Todos":
    datos_filtrados = datos_filtrados[datos_filtrados["servicio"] == filtrar_servicio]

st.dataframe(datos_filtrados)

# Manejo de errores en la base de datos
def insertar_cliente(nombre, servicio, costo, fecha, atendido_por, formula_tinte):
    try:
        conn = sqlite3.connect('salon.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, servicio, costo, fecha, atendido_por, formula_tinte)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, servicio, costo, fecha, atendido_por, formula_tinte))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error al insertar en la base de datos: {e}")
    finally:
        conn.close()
