from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Leer los PDFs
loader = PyPDFDirectoryLoader("../documentos")
documents = loader.load()

print(f"Se encontraron {len(documents)} páginas.")

# 2. Crear el separador de texto
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# 3. Dividir el documento en chunks
chunks = text_splitter.split_documents(documents)

print(f"\nSe generaron {len(chunks)} chunks.\n")

# 4. Mostrar los primeros 3 chunks
for i, chunk in enumerate(chunks[:3]):
    print(f"========== Chunk {i+1} ==========")
    print(chunk.page_content)
    print()