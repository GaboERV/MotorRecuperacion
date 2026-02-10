from setuptools import setup, find_packages

setup(
    name="MotorRecuperacion",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain-community",
        "langchain-core",
        "langchain-text-splitters",
        "langchain-huggingface",
        "sentence-transformers",
        "chromadb",
        "sqlalchemy",
        "pymysql",
        "docx2txt",
        "pypdf",
        "pillow",
        "pytesseract",
        "openai-whisper",
        "moviepy",
        "python-dotenv",
        "cryptography",
    ],
)
