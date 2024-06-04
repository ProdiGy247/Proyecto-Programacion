import sqlite3

def init_db():
    conn = sqlite3.connect('salon.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            fecha_registro TEXT,
            fecha_primera_visita TEXT,
            imagen BLOB
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

def agregar_cliente(nombre, telefono, fecha_registro, imagen):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO clientes (nombre, telefono, fecha_registro, imagen)
        VALUES (?, ?, ?, ?)
    ''', (nombre, telefono, fecha_registro, imagen))
    conn.commit()
    conn.close()

def actualizar_primera_visita(cliente_id, fecha_primera_visita):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE clientes
        SET fecha_primera_visita = ?
        WHERE id = ?
    ''', (fecha_primera_visita, cliente_id))
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
    # Actualizar fecha de primera visita si es la primera vez que el cliente tiene una visita
    c = conn.cursor()
    c.execute('''
        SELECT fecha_primera_visita FROM clientes WHERE id = ?
    ''', (cliente_id,))
    fecha_primera_visita = c.fetchone()[0]
    if not fecha_primera_visita:
        actualizar_primera_visita(cliente_id, fecha)

def obtener_visitas(cliente_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM visitas WHERE cliente_id = ?
    ''', (cliente_id,))
    visitas = c.fetchall()
    conn.close()
    return visitas

def buscar_visitas_por_fecha(fecha):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM visitas WHERE fecha = ?
    ''', (fecha,))
    visitas = c.fetchall()
    conn.close()
    return visitas
