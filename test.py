from MotorRecuperacion import configure, create_RecoveryEngine_client

# 1. Configuración Global (Solo una vez al inicio) no es necesario si se configura en el archivo .env
configure(
    # MySQL
    database_url = "mysql+pymysql://admin:58875887@localhost/rag_db",
    # SQLite
    # database_url = "sqlite:///rag_data.db"
)

# 2. Crear una instancia del cliente
client = create_RecoveryEngine_client()

# 3. Subir un archivo (ejemplo con PDF)
with open("clase2.pdf", "rb") as f:
    client.upload(
        user_email="usuario@ejemplo.com",
        filename="clase2.pdf",
        data=f.read()
    )

# 4. Realizar una consulta (RAG)
respuesta = client.ask(
    user_email="usuario@ejemplo.com",
    filenames=["clase2.pdf"],
    question="¿Cuál es el tema principal del documento?"
)
print(respuesta)

# 5. Listar archivos
archivos = client.list_files("usuario@ejemplo.com")

# 6. Eliminar archivo
client.delete("usuario@ejemplo.com", "documento.pdf")

print(archivos)