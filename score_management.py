import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="junction.proxy.rlwy.net",
            database="railway",
            user="root",
            password="coxuOuzEzFhMTNmKfWVNNmFdOngqdfkb",
            port="27018"    
        )
        return conn
    except Error as e:
        print("Error al conectar:", e)
        return None

def save_score(username, score):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO puntuaciones (id_usuario, puntuacion) VALUES ((SELECT id FROM usuarios WHERE nombre_usuario=%s), %s)", (username, score))
        conn.commit()
        cursor.close()
        conn.close()

def get_high_scores(limit=10):
    conn = connect_db()
    scores = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_usuario, puntuacion FROM puntuaciones JOIN usuarios ON puntuaciones.id_usuario = usuarios.id ORDER BY puntuacion DESC LIMIT %s", (limit,))
        scores = cursor.fetchall()
        cursor.close()
        conn.close()
    return scores
