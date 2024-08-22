import cv2
import face_recognition
import mysql.connector
import numpy as np

# Configura la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="22102001",
        database="prueba"
    )

# Obtén las imágenes de la base de datos
def load_faces_from_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, nombre,  image_data FROM personas")
    
    faces = []
    for (id, name, image_data) in cursor.fetchall():
        image = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            faces.append((id, name, face_encodings[0]))
    
    cursor.close()
    connection.close()
    return faces

# Función principal de reconocimiento
def recognize_face(frame, known_faces):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([f[2] for f in known_faces], face_encoding)
        if True in matches:
            match_index = matches.index(True)
            person_id, person_name = known_faces[match_index][0:2]
            return person_id, person_name
    
    return None, None

# Captura y procesamiento en tiempo real
def main():
    known_faces = load_faces_from_db()
    
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        person_id, person_name = recognize_face(frame, known_faces)
        
        if person_id:
            cv2.putText(frame, f"ID: {person_id}, Name: {person_name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
