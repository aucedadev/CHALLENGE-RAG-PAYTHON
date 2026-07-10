
from langchain_chroma import Chroma
from app.config import CHROMA_DIR, TOP_K
from app.embeddings import get_embedding_model


def search_documents(question: str):
    embedding_model = get_embedding_model()

    vector_db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model
    )

    results = vector_db.similarity_search_with_score(
        question,
        k=TOP_K
    )

    return results