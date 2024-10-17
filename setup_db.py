import sqlite3

conn = sqlite3.connect('votacion.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE candidatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        partido TEXT NOT NULL,
        foto TEXT,
        votos INTEGER DEFAULT 0
    )
''')
conn.commit()
conn.close()