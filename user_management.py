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

def register_user(nombre_usuario, contrasena, email):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, email) VALUES (%s, %s, %s)", (nombre_usuario, contrasena, email))
        conn.commit()
        cursor.close()
        conn.close()

def authenticate_user(nombre_usuario, contrasena):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s", (nombre_usuario, contrasena))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user  # Retorna el usuario si las credenciales son correctas
    return None
