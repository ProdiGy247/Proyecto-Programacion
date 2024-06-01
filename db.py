from supabase import create_client, Client
import pandas as pd


# Configuración de Supabase
SUPABASE_URL = 'https://lrwufbjvkfnyfjyjuzue.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxyd3VmYmp2a2ZueWZqeWp1enVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyNzUyNDQsImV4cCI6MjAzMjg1MTI0NH0.OI88wwe7zTNLMdmaQBW7TRjoK3cU0Mx3koFs0Sam52Q'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para obtener todos los datos de la tabla


def obtener_datos():
    response = supabase.table('clientes').select('*').execute()
    return pd.DataFrame(response.data)

# Función para insertar datos en la tabla


def insertar_cliente(nombre, servicio, costo, fecha, atendido_por, formula_tinte, celular):
    supabase.table('clientes').insert({
        'nombre': nombre,
        'servicio': servicio,
        'costo': costo,
        'fecha': fecha,
        'atendido_por': atendido_por,
        'formula_tinte': formula_tinte,
        'celular': celular
    }).execute()
