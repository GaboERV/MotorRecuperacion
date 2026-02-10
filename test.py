from MotorRecuperacion import configure, create_RecoveryEngine_client

# 1. Configuración Global (Solo una vez al inicio) no es necesario si se configura en el archivo .env
configure(database_url="mysql+pymysql://user:pass@localhost/db_name")

# 2. Crear una instancia del cliente
client = create_RecoveryEngine_client()

# 3. Subir un archivo (ejemplo con PDF)
with open("documento.pdf", "rb") as f:
    client.upload(
        user_email="usuario@ejemplo.com",
        filename="documento.pdf",
        data=f.read()
    )

# 4. Realizar una consulta (RAG)
respuesta = client.ask(
    user_email="usuario@ejemplo.com",
    filenames=["documento.pdf"],
    question="¿Cuál es el tema principal del documento?"
)
print(respuesta)

# 5. Listar archivos
archivos = client.list_files("usuario@ejemplo.com")

# 6. Eliminar archivo
client.delete("usuario@ejemplo.com", "documento.pdf")

print(archivos)