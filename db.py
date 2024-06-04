import sqlite3

def init_db():
    conn = sqlite3.connect('salon.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            email TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha TEXT,
            servicio TEXT,
            costo REAL,
            formula TEXT,
            notas TEXT,
            imagen BLOB,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect('salon.db')
    return conn

def agregar_cliente(nombre, telefono, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO clientes (nombre, telefono, email)
        VALUES (?, ?, ?)
    ''', (nombre, telefono, email))
    conn.commit()
    conn.close()

def obtener_clientes():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    conn.close()
    return clientes

def agregar_visita(cliente_id, fecha, servicio, costo, formula, notas, imagen):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO visitas (cliente_id, fecha, servicio, costo, formula, notas, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cliente_id, fecha, servicio, costo, formula, notas, imagen))
    conn.commit()
    conn.close()

def obtener_visitas(cliente_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM visitas WHERE cliente_id = ?
    ''', (cliente_id,))
    visitas = c.fetchall()
    conn.close()
    return visitas
