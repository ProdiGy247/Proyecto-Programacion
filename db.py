import os
from supabase import create_client, Client
import pandas as pd


# Configuración de Supabase
SUPABASE_URL = os.environ.get('https://lrwufbjvkfnyfjyjuzue.supabase.co')
SUPABASE_KEY = os.environ.get('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxyd3VmYmp2a2ZueWZqeWp1enVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyNzUyNDQsImV4cCI6MjAzMjg1MTI0NH0.OI88wwe7zTNLMdmaQBW7TRjoK3cU0Mx3koFs0Sam52Q')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def crear_tabla():
    query = '''
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        servicio TEXT NOT NULL,
        costo REAL NOT NULL,
        fecha DATE NOT NULL,
        atendido_por TEXT NOT NULL,
        formula_tinte TEXT NOT NULL,
        celular TEXT NOT NULL
    )
    '''
    response = supabase.rpc('execute_sql', {'sql': query}).execute()


# Función para obtener todos los datos de la tabla


def obtener_datos():
    response = supabase.table('clientes').select('*').execute()
    return pd.DataFrame(response.data)

# Función para insertar datos en la tabla


def insertar_cliente(nombre, servicio, costo, fecha, atendido_por, formula_tinte, celular):
    try:
        data = {
            "nombre": nombre,
            "servicio": servicio,
            "costo": costo,
            "fecha": fecha,
            "atendido_por": atendido_por,
            "formula_tinte": formula_tinte,
            "celular": celular
        }
        response = supabase.table('clientes').insert(data).execute()
        if response.status_code != 201:
            raise Exception(f"Error al insertar en la base de datos: {response.data}")
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
