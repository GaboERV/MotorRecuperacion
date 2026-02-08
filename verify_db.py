from database.config import engine, get_db, Base
from services.file_service import FileService
import os

# 1. Create tables
Base.metadata.create_all(bind=engine)

def verify():
    db = next(get_db())
    service = FileService(db)

    email = "test@example.com"
    filename = "test_upload.txt"
    content = b"Contenido de prueba para base de datos."

    print(f"--- Subiendo archivo para {email} ---")
    file_record = service.upload_file(email, filename, content)
    
    print(f"Archivo guardado en BD con ID: {file_record.id}")
    print(f"Ruta física: {file_record.path}")
    print(f"Usuario asociado: {file_record.user.email}")

    # Verify file exists on disk
    if os.path.exists(file_record.path):
        print("VERIFICACIÓN EXITOSA: El archivo existe en disco.")
    else:
        print("ERROR: El archivo no se creó en disco.")

    # Clean up
    if os.path.exists(file_record.path):
        os.remove(file_record.path)
        # remove dirs if empty
        os.rmdir(os.path.dirname(file_record.path))

if __name__ == "__main__":
    verify()
