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

init_db()
