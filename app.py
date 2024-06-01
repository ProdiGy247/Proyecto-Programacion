import streamlit as st
import pandas as pd
import sqlite3
from db import obtener_datos

# Título de la aplicación
st.title("Gestión de Clientes - Salón de Belleza")

# Función para insertar datos en la tabla


def insertar_cliente(nombre, servicio, costo, fecha, atendido_por, formula_tinte, celular):
    try:
        conn = sqlite3.connect('salon.db')  # Conectar a la base de datos
        cursor = conn.cursor()  # Crear un cursor para ejecutar comandos SQL
        cursor.execute('''
            INSERT INTO clientes (nombre, servicio, costo, fecha, atendido_por, formula_tinte, celular)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, servicio, costo, fecha, atendido_por, formula_tinte, celular))  # Ejecutar la inserción
        conn.commit()  # Confirmar los cambios en la base de datos
    except sqlite3.Error as e:  # Capturar cualquier error de SQLite
        # Mostrar el error en la interfaz de usuario
        st.error(f"Error al insertar en la base de datos: {e}")
        # Imprimir el error en la consola
        print(f"Error al insertar en la base de datos: {e}")
    finally:
        conn.close()  # Asegurar que la conexión a la base de datos se cierre


# Formulario para agregar clientes
st.header("Agregar nuevo cliente")
nombre = st.text_input("Nombre del Cliente", key="nombre_cliente")
servicio = st.text_input("Servicio Realizado", key="servicio_cliente")
costo = st.number_input("Costo del Servicio", min_value=0.0,
                        format="%.2f", key="costo_servicio")
fecha = st.date_input("Fecha de Visita", key="fecha_visita")
atendido_por = st.text_input("Atendido por", key="atendido_por")
formula_tinte = st.text_area("Fórmula del Tinte", key="formula_tinte")
celular = st.text_input("Número de Celular", key="celular_cliente")

if st.button("Agregar Cliente", key="btn_agregar_cliente"):
    if not nombre or not servicio or not atendido_por or not formula_tinte or not celular:
        st.error("Por favor, completa todos los campos obligatorios.")
    else:
        insertar_cliente(nombre, servicio, costo, fecha.strftime(
            '%Y-%m-%d'), atendido_por, formula_tinte, celular)
        st.success("Cliente agregado exitosamente!")

# Filtrado y búsqueda
st.header("Buscar Clientes")
buscar_nombre = st.text_input("Buscar por nombre", key="buscar_nombre")

# Obtener sugerencias para autocompletado
sugerencias_celular = obtener_datos()["celular"].unique().tolist()
celular_elegido = st.selectbox("Seleccionar número de celular", [
                               ""] + sugerencias_celular)

if buscar_nombre or celular_elegido:
    st.header("Clientes Registrados")
    datos_filtrados = obtener_datos()

    if buscar_nombre:
        datos_filtrados = datos_filtrados[datos_filtrados["nombre"].str.contains(
            buscar_nombre, case=False)]
    if celular_elegido:
        datos_filtrados = datos_filtrados[datos_filtrados["celular"].str.contains(
            celular_elegido, case=False)]

    st.dataframe(datos_filtrados)
