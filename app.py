import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import datetime, date, time

# Configuración de Supabase
url = "https://lrwufbjvkfnyfjyjuzue.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxyd3VmYmp2a2ZueWZqeWp1enVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyNzUyNDQsImV4cCI6MjAzMjg1MTI0NH0.OI88wwe7zTNLMdmaQBW7TRjoK3cU0Mx3koFs0Sam52Q"
supabase: Client = create_client(url, key)

# Funciones de la Base de Datos
def agregar_cliente(nombre, telefono=None):
    data = {"nombre": nombre, "telefono": telefono}
    response = supabase.table("clientes").insert(data).execute()
    return response.data

def registrar_visita(cliente_id, atendido_por, servicio_id, precio, fecha_hora, formula=None, notas=None, imagen_path=None):
    imagen_data = None
    if imagen_path and os.path.isfile(imagen_path):
        with open(imagen_path, "rb") as image_file:
            imagen_data = base64.b64encode(image_file.read()).decode()
    
    data = {
        "cliente_id": cliente_id,
        "atendido_por": atendido_por,
        "servicio_id": servicio_id,
        "precio": precio,
        "fecha_hora": fecha_hora.isoformat(),
        "formula": formula,
        "notas": notas,
        "imagen": imagen_data
    }
    response = supabase.table("visitas").insert(data).execute()
    return response.data

def buscar_cliente(nombre=None, telefono=None):
    if nombre:
        response = supabase.table("clientes").select("*").ilike("nombre", f"%{nombre}%").execute()
    elif telefono:
        response = supabase.table("clientes").select("*").eq("telefono", telefono).execute()
    else:
        raise ValueError("Debes proporcionar un nombre o un teléfono para buscar.")
    return response.data

def editar_cliente(cliente_id, nombre=None, telefono=None):
    data = {}
    if nombre:
        data["nombre"] = nombre
    if telefono:
        if len(telefono) > 10:
            raise ValueError("El número de teléfono no puede tener más de 10 dígitos.")
        data["telefono"] = telefono

    response = supabase.table("clientes").update(data).eq("id", cliente_id).execute()
    return response.data

def obtener_servicios():
    response = supabase.table("servicios").select("*").execute()
    return response.data

def obtener_empleados():
    response = supabase.table("empleados").select("*").execute()
    return response.data

# Interfaz de Streamlit
st.title("Sistema de Gestión de Clientes")

menu = ["Agregar Cliente y Registrar Visita", "Buscar Cliente", "Editar Cliente"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Agregar Cliente y Registrar Visita":
    st.subheader("Agregar Cliente y Registrar Visita")
    nombre = st.text_input("Nombre del cliente")
    telefono = st.text_input("Teléfono del cliente (opcional, máximo 10 dígitos)")
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    fecha_hora = datetime.combine(fecha, hora)

    buscar_button = st.button("Buscar Cliente")
    
    if buscar_button:
        clientes = buscar_cliente(nombre=nombre) if nombre else buscar_cliente(telefono=telefono)
        if clientes:
            st.warning("Cliente ya registrado:")
            st.write(clientes)

            if st.button("Registrar Visita"):
                clientes_options = {cliente['nombre']: cliente['id'] for cliente in clientes}
                cliente_id = st.selectbox("Seleccionar Cliente", options=list(clientes_options.keys()))
                cliente_id = clientes_options[cliente_id]
                
                empleados = obtener_empleados()
                servicios = obtener_servicios()

                empleado_options = {empleado['nombre']: empleado['id'] for empleado in empleados}
                servicio_options = {servicio['nombre']: servicio['id'] for servicio in servicios}

                atendido_por = st.selectbox("Atendido por", options=list(empleado_options.keys()))
                servicio_id = st.selectbox("Servicio", options=list(servicio_options.keys()))
                precio = st.number_input("Precio", min_value=0, format="%d")
                formula = st.text_area("Fórmula (opcional)")
                notas = st.text_area("Notas (opcional)")
                imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])
                
                if st.button("Registrar Visita"):
                    imagen_path = None
                    if imagen:
                        imagen_path = f"temp_{imagen.name}"
                        with open(imagen_path, "wb") as f:
                            f.write(imagen.getbuffer())
                    
                    visita = registrar_visita(cliente_id, empleado_options[atendido_por], servicio_options[servicio_id], precio, fecha_hora, formula if formula else None, notas if notas else None, imagen_path)
                    if imagen_path:
                        os.remove(imagen_path)
                    st.success(f"Visita registrada exitosamente para {cliente_id}")
        else:
            if st.button("Agregar Cliente"):
                if nombre:
                    nuevo_cliente = agregar_cliente(nombre, telefono if telefono else None)
                    st.success(f"Cliente {nombre} agregado exitosamente")
                    
                    cliente_id = nuevo_cliente[0]['id']
                    
                    empleados = obtener_empleados()
                    servicios = obtener_servicios()

                    empleado_options = {empleado['nombre']: empleado['id'] for empleado in empleados}
                    servicio_options = {servicio['nombre']: servicio['id'] for servicio in servicios}

                    atendido_por = st.selectbox("Atendido por", options=list(empleado_options.keys()))
                    servicio_id = st.selectbox("Servicio", options=list(servicio_options.keys()))
                    precio = st.number_input("Precio", min_value=0, format="%d")
                    formula = st.text_area("Fórmula (opcional)")
                    notas = st.text_area("Notas (opcional)")
                    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])
                    
                    if st.button("Registrar Visita"):
                        imagen_path = None
                        if imagen:
                            imagen_path = f"temp_{imagen.name}"
                            with open(imagen_path, "wb") as f:
                                f.write(imagen.getbuffer())
                        
                        visita = registrar_visita(cliente_id, empleado_options[atendido_por], servicio_options[servicio_id], precio, fecha_hora, formula if formula else None, notas if notas else None, imagen_path)
                        if imagen_path:
                            os.remove(imagen_path)
                        st.success(f"Visita registrada exitosamente para {cliente_id}")
                else:
                    st.error("El nombre es obligatorio")

    empleados = obtener_empleados()
    servicios = obtener_servicios()

    empleado_options = {empleado['nombre']: empleado['id'] for empleado in empleados}
    servicio_options = {servicio['nombre']: servicio['id'] for servicio in servicios}

    atendido_por = st.selectbox("Atendido por", options=list(empleado_options.keys()))
    servicio_id = st.selectbox("Servicio", options=list(servicio_options.keys()))
    precio = st.number_input("Precio", min_value=0, format="%d")
    formula = st.text_area("Fórmula (opcional)")
    notas = st.text_area("Notas (opcional)")
    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "png", "jpeg"])

    if st.button("Agregar Cliente y Registrar Visita"):
        if nombre:
            clientes = buscar_cliente(nombre=nombre) if nombre else buscar_cliente(telefono=telefono)
            if clientes:
                st.warning("Cliente ya registrado:")
                st.write(clientes)

                if st.button("Registrar Visita para Cliente Existente"):
                    clientes_options = {cliente['nombre']: cliente['id'] for cliente in clientes}
                    cliente_id = st.selectbox("Seleccionar Cliente", options=list(clientes_options.keys()))
                    cliente_id = clientes_options[cliente_id]
                    
                    imagen_path = None
                    if imagen:
                        imagen_path = f"temp_{imagen.name}"
                        with open(imagen_path, "wb") as f:
                            f.write(imagen.getbuffer())
                    
                    visita = registrar_visita(cliente_id, empleado_options[atendido_por], servicio_options[servicio_id], precio, fecha_hora, formula if formula else None, notas if notas else None, imagen_path)
                    if imagen_path:
                        os.remove(imagen_path)
                    st.success(f"Visita registrada exitosamente para {cliente_id}")
            else:
                nuevo_cliente = agregar_cliente(nombre, telefono if telefono else None)
                st.success(f"Cliente {nombre} agregado exitosamente")
                
                cliente_id = nuevo_cliente[0]['id']
                
                imagen_path = None
                if imagen:
                    imagen_path = f"temp_{imagen.name}"
                    with open(imagen_path, "wb") as f:
                        f.write(imagen.getbuffer())
                
                visita = registrar_visita(cliente_id, empleado_options[atendido_por], servicio_options[servicio_id], precio, fecha_hora, formula if formula else None, notas if notas else None, imagen_path)
                if imagen_path:
                    os.remove(imagen_path)
                st.success(f"Visita registrada exitosamente para {cliente_id}")
        else:
            st.error("El nombre es obligatorio")

elif choice == "Buscar Cliente":
    st.subheader("Buscar Cliente")
    criterio = st.selectbox("Buscar por", ["Nombre", "Teléfono"])
    buscar_por = st.text_input(f"Ingresar {criterio}")
    
    if st.button("Buscar"):
        if criterio == "Nombre":
            clientes = buscar_cliente(nombre=buscar_por)
        elif criterio == "Teléfono":
            clientes = buscar_cliente(telefono=buscar_por)
        
        if clientes:
            st.write(clientes)
        else:
            st.warning("No se encontraron clientes")

elif choice == "Editar Cliente":
    st.subheader("Editar Cliente")
    clientes = buscar_cliente()
    cliente_options = {cliente['nombre']: cliente['id'] for cliente in clientes}

    cliente_id = st.selectbox("Seleccionar Cliente", options=list(cliente_options.keys()))
    cliente_actual = next(cliente for cliente in clientes if cliente['id'] == cliente_options[cliente_id])

    with st.form(key="editar_cliente_form"):
        nombre = st.text_input("Nombre", value=cliente_actual["nombre"])
        telefono = st.text_input("Teléfono (opcional, máximo 10 dígitos)", value=cliente_actual.get("telefono", ""))
        submit_button = st.form_submit_button(label="Actualizar Cliente")

    if submit_button:
        cliente = editar_cliente(cliente_options[cliente_id], nombre, telefono if telefono else None)
        st.success(f"Cliente {nombre} actualizado exitosamente")

st.sidebar.markdown("""
    ## Información
    Este es un sistema de gestión de clientes construido con Streamlit y Supabase.
""")



