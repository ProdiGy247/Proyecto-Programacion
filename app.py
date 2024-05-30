import streamlit as st
import pandas as pd
from db import insertar_cliente, obtener_datos

# Título de la aplicación
st.title("Gestión de Clientes - Salón de Belleza")

# Formulario para agregar clientes
st.header("Agregar nuevo cliente")
nombre = st.text_input("Nombre del Cliente")
servicio = st.text_input("Servicio Realizado")
costo = st.number_input("Costo del Servicio", min_value=0.0, format="%.2f")
fecha = st.date_input("Fecha de Visita")
atendido_por = st.text_input("Atendido por")
formula_tinte = st.text_area("Fórmula del Tinte")

if st.button("Agregar Cliente"):
    insertar_cliente(nombre, servicio, costo, fecha.strftime('%Y-%m-%d'), atendido_por, formula_tinte)
    st.success("Cliente agregado exitosamente!")

# Mostrar los datos en una tabla
st.header("Clientes Registrados")
datos = obtener_datos()
st.dataframe(datos)
