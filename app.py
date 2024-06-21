import streamlit as st
from supabase import create_client, Client
import base64
import os

# Configuración de Supabase
url = "https://lrwufbjvkfnyfjyjuzue.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxyd3VmYmp2a2ZueWZqeWp1enVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyNzUyNDQsImV4cCI6MjAzMjg1MTI0NH0.OI88wwe7zTNLMdmaQBW7TRjoK3cU0Mx3koFs0Sam52Q"
supabase: Client = create_client(url, key)

# Funciones de la Base de Datos
def agregar_cliente(nombre, telefono=None, fecha=None, servicios=None, formula=None, precio=None, notas=None):
    data = {
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha,
        "servicios": servicios,
        "formula": formula,
        "precio": precio,
        "notas": notas
    }
    response = supabase.table("clientes").insert(data).execute()
    return response.data

def agregar_imagen(cliente_id, imagen_path):
    if os.path.isfile(imagen_path):
        with open(imagen_path, "rb") as image_file:
            imagen_data = base64.b64encode(image_file.read()).decode()
        
        data = {
            "cliente_id": cliente_id,
            "imagen": imagen_data
        }
        response = supabase.table("imagenes").insert(data).execute()
        return response.data
    else:
        raise FileNotFoundError(f"No se encontró el archivo {imagen_path}")

def obtener_empleados():
    response = supabase.table("empleados").select("nombre").execute()
    empleados = [empleado['nombre'] for empleado in response.data]
    return empleados

def obtener_nombres_clientes():
    response = supabase.table("clientes").select("nombre").execute()
    nombres = [cliente['nombre'] for cliente in response.data]
    return nombres

def filtrar_nombres(nombres, consulta):
    return [nombre for nombre in nombres if consulta.lower() in nombre.lower()]

# Interfaz de Streamlit
st.title("Sistema de Gestión de Clientes")

menu = ["Agregar Cliente", "Buscar Cliente", "Editar Cliente"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Agregar Cliente":
    st.subheader("Agregar Cliente y Registrar Visita")
    
    nombre = st.text_input("Nombre del cliente")
    telefono = st.text_input("Teléfono del cliente (opcional, máximo 10 dígitos)")
    fecha = st.date_input("Fecha")
    
    empleados = obtener_empleados()
    if empleados:
        atendido_por = st.selectbox("Atendido por", options=empleados)
    else:
        st.warning("No hay empleados disponibles. Por favor, agregue empleados en la base de datos.")
        atendido_por = None
    
    servicios = st.text_area("Servicios realizados (separados por comas)")
    precio = st.number_input("Precio", min_value=0, step=1)
    formula = st.text_area("Fórmula (opcional)")
    notas = st.text_area("Notas (opcional)")
    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])

    if st.button("Agregar Cliente"):
        if nombre:
            nuevo_cliente = agregar_cliente(nombre, telefono if telefono else None, fecha, servicios, formula, precio, notas)
            st.success(f"Cliente {nombre} agregado exitosamente")

            cliente_id = nuevo_cliente[0]['id']
            
            if imagen:
                imagen_path = f"temp_{imagen.name}"
                with open(imagen_path, "wb") as f:
                    f.write(imagen.getbuffer())
                
                agregar_imagen(cliente_id, imagen_path)
                os.remove(imagen_path)
                
            st.success(f"Visita registrada exitosamente para {cliente_id}")
        else:
            st.error("El nombre es obligatorio")

elif choice == "Buscar Cliente":
    st.subheader("Buscar Cliente")
    nombres = obtener_nombres_clientes()
    nombre_input = st.text_input("Ingresar nombre del cliente")

    if nombre_input:
        coincidencias = filtrar_nombres(nombres, nombre_input)
        if coincidencias:
            cliente_seleccionado = st.selectbox("Clientes encontrados", coincidencias)
            if cliente_seleccionado:
                st.write(f"Cliente seleccionado: {cliente_seleccionado}")
        else:
            st.write("No se encontraron coincidencias")

elif choice == "Editar Cliente":
    st.subheader("Editar Cliente")
    nombres = obtener_nombres_clientes()
    cliente_seleccionado = st.selectbox("Seleccionar Cliente", options=nombres)

    if cliente_seleccionado:
        response = supabase.table("clientes").select("*").eq("nombre", cliente_seleccionado).execute()
        cliente_actual = response.data[0]

        with st.form(key="editar_cliente_form"):
            nombre = st.text_input("Nombre", value=cliente_actual["nombre"])
            telefono = st.text_input("Teléfono (opcional, máximo 10 dígitos)", value=cliente_actual.get("telefono", ""))
            fecha = st.date_input("Fecha", value=cliente_actual.get("fecha"))
            servicios = st.text_area("Servicios realizados (separados por comas)", value=cliente_actual.get("servicios", ""))
            formula = st.text_area("Fórmula (opcional)", value=cliente_actual.get("formula", ""))
            precio = st.number_input("Precio", min_value=0, step=1, value=cliente_actual.get("precio", 0))
            notas = st.text_area("Notas (opcional)", value=cliente_actual.get("notas", ""))
            submit_button = st.form_submit_button(label="Actualizar Cliente")

        if submit_button:
            data = {
                "nombre": nombre,
                "telefono": telefono,
                "fecha": fecha,
                "servicios": servicios,
                "formula": formula,
                "precio": precio,
                "notas": notas
            }
            supabase.table("clientes").update(data).eq("id", cliente_actual["id"]).execute()
            st.success(f"Cliente {nombre} actualizado exitosamente")

st.sidebar.markdown("""
    ## Información
    Este es un sistema de gestión de clientes construido con Streamlit y Supabase.
""")





