from langchain_community.vectorstores import Chroma

from app.config import CHROMA_DIR
from app.embeddings import get_embedding_model
from app.load_documents import load_documents, split_documents


def create_vector_db():
    documents = load_documents()

    if not documents:
        print("No hay documentos para procesar.")
        return

    chunks = split_documents(documents)

    print(f"Chunks creados: {len(chunks)}")

    embedding_model = get_embedding_model()

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DIR)
    )

    print("Base vectorial creada correctamente.")


if __name__ == "__main__":
    create_vector_db()