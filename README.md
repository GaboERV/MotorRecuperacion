# Motor de Recuperación Semántica con MySQL

Este proyecto implementa un sistema de Búsqueda Semántica (Retrieval Engine) que permite cargar documentos (PDF, Docx, Texto, Imágenes, Video), almacenarlos de forma segura y realizar consultas de similitud sobre ellos utilizando una base de datos vectorial temporal.

**Nota**: Este no es un sistema RAG completo (aún no incluye generación de texto con LLMs), sino el componente de recuperación (Retrieval) que podría alimentar a uno.

## Características

- **Base de Datos**: MySQL para metadatos de usuario y registro de archivos.
- **Búsqueda Semántica**: Búsqueda vectorial temporal usando ChromaDB y modelos de embeddings de HuggingFace (`sentence-transformers`). Recupere los fragmentos más relevantes de sus documentos basándose en el significado, no solo en palabras clave.
- **Formatos Soportados**:
  - Texto: `.txt`, `.md`, `.py`, `.json`
  - Documentos: `.pdf`, `.docx`
  - Multimedia: Imágenes (OCR con Tesseract), Video (Transcripción de audio)
- **Seguridad**: Validación de tipos de archivo y rutas.

## Requisitos Previos

- Python 3.8+
- MySQL Server (local o remoto)
- Herramientas del sistema: `ffmpeg` (para video), `tesseract-ocr` (para imágenes)

## Instalación

1.  **Clonar el repositorio** o descargar el código fuente.

2.  **Crear y activar un entorno virtual**:

    ```bash
    python3 -m venv rag_env
    source rag_env/bin/activate  # Linux/Mac
    # rag_env\Scripts\activate   # Windows
    ```

    3.  **Instalar el paquete en modo edición**:

    ```bash
    pip install -e .
    ```

3.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en la raíz del proyecto con la URL de conexión a tu base de datos MySQL:

    ````env
    ```env
    # Opción A: MySQL
    DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd

    # Opción B: SQLite (Archivo local)
    # DATABASE_URL=sqlite:///rag_data.db
    ````

    _Nota: El driver utilizado es `pymysql`. Asegúrate de que tu usuario tenga permisos para crear tablas si es la primera ejecución._

## Uso

El sistema está diseñado para ser utilizado como una librería o servicio.

### Ejemplo Rápido

Puedes ver un ejemplo funcional en el archivo `test.py`. Para ejecutarlo:

```bash
# Asegúrate de estar en el entorno virtual
source rag_env/bin/activate

# Ejecuta el script de prueba
python3 test.py
```

### Integración en tu Código

```python
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

# 4. Realizar una consulta (Búsqueda Semántica)
respuesta = client.ask(
    user_email="usuario@ejemplo.com",
    filenames=["documento.pdf"],
    question="¿Qué fragmentos son relevantes para 'tema principal'?"
)
# Devuelve una lista de cadenas de texto (chunks) relevantes
print(respuesta)

# 5. Listar archivos
archivos = client.list_files("usuario@ejemplo.com")
print(archivos)

# 6. Eliminar archivo
client.delete("usuario@ejemplo.com", "documento.pdf")

```

## Estructura del Proyecto

- `MotorRecuperacion/`
  - `main.py`: Fachada principal (`RecoveryEngine`) y punto de entrada.
  - `config.py`: Gestión de configuración (Singleton).
  - `managers/`: Lógica de negocio (RAG, gestión de archivos).
  - `services/`: Capa de servicio e integración con BD.
  - `repositories/`: Patrón repositorio para acceso a datos.
  - `models/`: Modelos ORM (SQLAlchemy).
  - `loaders/`: Estrategias de carga para diferentes tipos de archivo.
  - `database/`: Configuración de conexión a base de datos.

## Solución de Problemas

- **Error de Autenticación MySQL**: Si ves errores relacionados con `caching_sha2_password`, asegúrate de tener instalada la librería `cryptography` (incluida en `requirements.txt`).
- **Error de Importación**: Si ejecutas scripts desde dentro de la carpeta del paquete, asegúrate de configurar `PYTHONPATH` o ejecutar los tests desde el directorio padre.
- **Modelos**: La primera vez que se ejecuta, el sistema descargará los modelos de HuggingFace (`all-MiniLM-L6-v2`), lo cual puede tardar unos minutos dependiendo de tu conexión.
