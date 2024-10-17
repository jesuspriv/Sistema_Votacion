from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('votacion.db')
    conn.row_factory = sqlite3.Row 
    return conn

def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM candidatos')
   
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="candidatos"')

    cursor.execute('''CREATE TABLE IF NOT EXISTS candidatos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        partido TEXT NOT NULL,
                        foto TEXT,
                        votos INTEGER DEFAULT 0
                    )''')

    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario == 'admin' and contrasena == 'admin123':
            return redirect(url_for('agregar_candidato'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")
    return render_template('login.html')


@app.route('/agregar_candidato', methods=['GET', 'POST'])
def agregar_candidato():
    if request.method == 'POST':
        nombre = request.form['nombre']
        partido = request.form['partido']
        foto = request.files['foto']

        if foto:
            foto_path = os.path.join('static/images', foto.filename)
            foto.save(foto_path)
        else:
            foto_path = None

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO candidatos (nombre, partido, foto) VALUES (?, ?, ?)',
                       (nombre, partido, foto_path))
        conn.commit()
        conn.close()

        if 'agregar_mas' in request.form:
            return redirect(url_for('agregar_candidato'))

        elif 'ir_a_votar' in request.form:
            return redirect(url_for('votar'))

    return render_template('agregar_candidato.html')


@app.route('/votar', methods=['GET', 'POST'])
def votar():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_candidato = request.form['candidato']
        cursor.execute('UPDATE candidatos SET votos = votos + 1 WHERE id = ?', (id_candidato,))
        conn.commit()
        return redirect(url_for('votar'))

    cursor.execute('SELECT * FROM candidatos')
    candidatos = cursor.fetchall()
    conn.close()

    return render_template('votar.html', candidatos=candidatos)


@app.route('/ganador')
def ganador():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT nombre, partido, votos, foto FROM candidatos ORDER BY votos DESC LIMIT 1')
    ganador = cursor.fetchone()

    conn.close()

    return render_template('ganador.html', ganador=ganador)

if __name__ == '__main__':
    crear_tablas()
    app.run(debug=True)
