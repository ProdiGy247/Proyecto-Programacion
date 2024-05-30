import sqlite3
import pandas as pd

# Crear la base de datos y la tabla si no existen
def crear_tabla():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            servicio TEXT,
            costo REAL,
            fecha TEXT,
            atendido_por TEXT,
            formula_tinte TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para insertar datos en la tabla
def insertar_cliente(nombre, servicio, costo, fecha, atendido_por, formula_tinte):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nombre, servicio, costo, fecha, atendido_por, formula_tinte)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, servicio, costo, fecha, atendido_por, formula_tinte))
    conn.commit()
    conn.close()

# Función para obtener todos los datos de la tabla
def obtener_datos():
    conn = sqlite3.connect('salon.db')
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    return df

# Ejecutar la función para crear la tabla al importar el módulo
crear_tabla()
