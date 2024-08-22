import mysql.connector

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '22102001',
    'database': 'prueba'
}

def insert_person(name, age, image_path):
    # Leer la imagen en formato binario
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Consulta SQL para insertar datos
    query = "INSERT INTO personas (nombre, edad, image_data) VALUES (%s, %s, %s)"
    
    # Ejecutar la consulta
    cursor.execute(query, (name, age, image_data))
    
    # Confirmar los cambios
    conn.commit()
    
    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

# Ejemplo de uso
insert_person('Maite ', 1, 'C:\\Users\\rojas\\OneDrive\\Imágenes\\Álbum de cámara\\Maite.jpg')

