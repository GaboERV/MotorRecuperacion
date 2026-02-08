# Sistema RAG con MySQL

Este proyecto implementa un sistema de Generación Aumentada por Recuperación (RAG) que permite cargar documentos (PDF, Docx, Texto, Imágenes, Video), almacenarlos de forma segura, y realizar consultas sobre ellos utilizando una base de datos vectorial temporal.

## Características

- **Base de Datos**: MySQL para metadatos de usuario y archivos.
- **Almacenamiento**: Gestión de archivos locales con validación.
- **Formatos Soportados**: `.txt`, `.md`, `.py`, `.json`, `.pdf`, `.docx`, Imágenes (OCR), Video (Transcripción).
- **Logging**: Sistema de logs configurado.

## Instalación

1.  **Clonar el repositorio** (si aplica) o descargar el código.

2.  **Crear un entorno virtual** (recomendado):

    ```bash
    python -m venv rag_env
    source rag_env/bin/activate  # Linux/Mac
    # rag_env\Scripts\activate   # Windows
    ```

3.  **Instalar dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    Asegúrate de tener un archivo `.env` en la raíz con la conexión a la base de datos MySQL:
    ```env
    DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/nombre_bd
    ```

## Uso

El archivo principal es `main.py`. Ejecútalo para verificar el flujo completo (carga, listado, consulta y eliminación):

```bash
python main.py
```

El script realizará las siguientes acciones automáticamente como demostración:

1.  Creará un archivo de prueba.
2.  Lo cargará al sistema.
3.  Listará los archivos del usuario.
4.  Realizará una pregunta sobre el contenido del archivo.
5.  Eliminará el archivo y limpiará el entorno.

## Estructura del Proyecto

- `main.py`: Punto de entrada y definición del sistema (Frontal/Facade).
- `config.py`: Configuración centralizada.
- `managers/`: Lógica de negocio (File Manager, Motor RAG).
- `services/`: Servicios de base de datos.
- `models/`: Modelos SQLAlchemy (`User`, `File`).
- `repositories/`: Acceso a datos.
- `loaders/`: Manejadores de diferentes tipos de archivo.
