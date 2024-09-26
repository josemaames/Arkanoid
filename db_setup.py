import mysql.connector
from mysql.connector import Error

def create_db():
    try:
        conn = mysql.connector.connect(
            host="junction.proxy.rlwy.net",
            database="railway",
            user="root",
            password="coxuOuzEzFhMTNmKfWVNNmFdOngqdfkb",
            port="27018 "
        )
        if conn.is_connected():
            print("Conexión exitosa")
            
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(50) UNIQUE,
                    contrasena VARCHAR(50),
                    email VARCHAR(50),
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS puntuaciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT,
                    puntuacion INT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
                );
            ''')

            conn.commit()  
            print("Tablas creadas exitosamente")
            
            cursor.close()  
    except Error as e:
        print("Error al conectar:", e)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    create_db()
