import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import date

# Configuración de Supabase
url = "https://lrwufbjvkfnyfjyjuzue.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxyd3VmYmp2a2ZueWZqeWp1enVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyNzUyNDQsImV4cCI6MjAzMjg1MTI0NH0.OI88wwe7zTNLMdmaQBW7TRjoK3cU0Mx3koFs0Sam52Q"

# Funciones de la Base de Datos
def agregar_cliente(nombre, telefono=None, fecha_registro=None, servicios=None, precio=None, formula=None, notas=None, imagen=None, atendido_por=None):
    data = {
        "nombre": nombre,
        "telefono": telefono,
        "fecha_registro": fecha_registro,
        "servicios": servicios,
        "precio": precio,
        "formula": formula,
        "notas": notas,
        "imagen": imagen,
        "atendido_por": atendido_por
    }
    response = supabase.table("clientes").insert(data).execute()
    return response.data[0] if response.data else None

def agregar_visita(cliente_id, fecha, servicios, precio, formula, empleado_id, imagen_path=None):
    data = {
        "cliente_id": cliente_id,
        "fecha": fecha,
        "servicios": servicios,
        "precio": precio,
        "formula": formula,
        "empleado_id": empleado_id
    }
    if imagen_path and os.path.isfile(imagen_path):
        with open(imagen_path, "rb") as image_file:
            imagen_data = base64.b64encode(image_file.read()).decode()
        data["imagen"] = imagen_data
    response = supabase.table("visitas").insert(data).execute()
    return response.data

def guardar_imagen(cliente_id, imagen_path):
    if imagen_path and os.path.isfile(imagen_path):
        with open(imagen_path, "rb") as image_file:
            imagen_data = image_file.read()
        data = {
            "cliente_id": cliente_id,
            "imagen_data": imagen_data
        }
        response = supabase.table("imagenes").insert(data).execute()
        return response.data
    return None

def obtener_empleados():
    response = supabase.table("empleados").select("id, nombre").execute()
    empleados = {empleado['nombre']: empleado['id'] for empleado in response.data}
    return empleados

def obtener_clientes():
    response = supabase.table("clientes").select("id, nombre").execute()
    return response.data

def obtener_historial(cliente_id):
    response = supabase.table("visitas").select("*").eq("cliente_id", cliente_id).execute()
    return response.data

# Interfaz de Streamlit
st.title("Sistema de Gestión de Clientes y Empleados")

menu = ["Agregar Cliente y Visita", "Buscar Cliente", "Ver Historial", "Editar Cliente"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Agregar Cliente y Visita":
    st.subheader("Agregar Cliente y Registrar Visita")
    
    nombre = st.text_input("Nombre del cliente")
    telefono = st.text_input("Teléfono del cliente (opcional, máximo 10 dígitos)")
    fecha = st.date_input("Fecha de visita", value=date.today())
    
    empleados = obtener_empleados()
    if empleados:
        atendido_por = st.selectbox("Atendido por", options=list(empleados.keys()))
        empleado_id = empleados[atendido_por]
    else:
        st.warning("No hay empleados disponibles. Por favor, agregue empleados en la base de datos.")
        atendido_por = None
        empleado_id = None
    
    servicios = st.text_area("Servicios realizados (separados por comas)")
    precio = st.number_input("Precio", min_value=0, step=1)
    formula = st.text_area("Fórmula (opcional)")
    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])

    if st.button("Registrar"):
        if nombre:
            # Verificar si el cliente ya existe
            clientes = obtener_clientes()
            cliente_existente = next((c for c in clientes if c['nombre'] == nombre), None)
            
            if cliente_existente:
                cliente_id = cliente_existente['id']
                st.warning(f"El cliente {nombre} ya existe. Registrando visita.")
                
                agregar_visita(cliente_id, fecha, servicios, precio, formula, empleado_id, imagen.name if imagen else None)
                if imagen:
                    guardar_imagen(cliente_id, imagen.name)
                st.success(f"Visita registrada exitosamente para {nombre}")
            else:
                nueva_imagen = None
                if imagen and os.path.isfile(imagen.name):
                    nueva_imagen = imagen.name
                cliente = agregar_cliente(nombre, telefono, fecha, servicios, precio, formula, None, nueva_imagen, atendido_por)
                if imagen:
                    guardar_imagen(cliente['id'], imagen.name)
                st.success(f"Cliente y visita registrada exitosamente para {nombre}")

elif choice == "Buscar Cliente":
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Ingrese el nombre o teléfono del cliente")
    
    if search_term:
        clientes = obtener_clientes()
        resultado_busqueda = [cliente for cliente in clientes if search_term.lower() in cliente['nombre'].lower() or search_term in cliente['telefono']]
        
        if resultado_busqueda:
            for cliente in resultado_busqueda:
                st.write(f"Nombre: {cliente['nombre']}, Teléfono: {cliente['telefono']}")
        else:
            st.warning("No se encontraron resultados.")
            
elif choice == "Ver Historial":
    st.subheader("Ver Historial")
    cliente_id = st.text_input("Ingrese el ID del cliente")
    
    if cliente_id:
        historial = obtener_historial(cliente_id)
        
        if historial:
            for visita in historial:
                st.write(f"Fecha: {visita['fecha']}, Servicios: {visita['servicios']}, Precio: {visita['precio']}, Atendido por: {visita['empleado_id']}")
        else:
            st.warning("No se encontraron visitas para este cliente.")

elif choice == "Editar Cliente":
    st.subheader("Editar Cliente")
    cliente_id = st.text_input("Ingrese el ID del cliente a editar")
    
    if cliente_id:
        clientes = obtener_clientes()
        cliente = next((c for c in clientes if c['id'] == int(cliente_id)), None)
        
        if cliente:
            nombre = st.text_input("Nombre del cliente", value=cliente['nombre'])
            telefono = st.text_input("Teléfono del cliente (opcional, máximo 10 dígitos)", value=cliente['telefono'])
            servicios = st.text_area("Servicios realizados (separados por comas)", value=cliente['servicios'])
            precio = st.number_input("Precio", min_value=0, step=1, value=cliente['precio'])
            formula = st.text_area("Fórmula (opcional)", value=cliente['formula'])
            notas = st.text_area("Notas (opcional)", value=cliente['notas'])
            imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])
            atendido_por = st.selectbox("Atendido por", options=list(empleados.keys()), index=list(empleados.keys()).index(cliente['atendido_por']))
            
            if st.button("Guardar cambios"):
                # Aquí iría el código para actualizar el cliente en la base de datos
                pass






