from pathlib import Path

# Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpetas principales
DATA_DIR = BASE_DIR / "data"
DOCUMENTS_DIR = DATA_DIR / "documentos"
CHROMA_DIR = DATA_DIR / "chroma"

# Configuración de documentos
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Modelo de embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Configuración de búsqueda
TOP_K = 3