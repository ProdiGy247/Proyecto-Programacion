import streamlit as st
import pandas as pd
from db import obtener_datos, insertar_cliente

# Título de la aplicación
st.title("Gestión de Clientes - Salón de Belleza")

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
