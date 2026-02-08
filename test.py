import sys
import os

# Add parent directory to path to allow importing 'mi_proyecto_rag' as a package
# This allows running 'python test.py' inside the folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from mi_proyecto_rag.main import rag_client, RAGSystem

    
if not isinstance(rag_client, RAGSystem):
    print(f"FAILURE: rag_client is not RAGSystem, it is {type(rag_client)}")
    sys.exit(1)



with open("clase2.pdf", "rb") as f:
    rag_client.upload("gaboe@example.com", "clase2.pdf", f.read())    


try:
    print(rag_client.list_files("gaboe@example.com"))


    print(rag_client.ask("gaboe@example.com", ["clase2.pdf"], "¿que es un vector?"))

    rag_client.delete("gaboe@example.com", "clase2.pdf")

    print(rag_client.list_files("gaboe@example.com"))
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)

