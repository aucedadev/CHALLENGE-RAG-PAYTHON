import unicodedata
from collections import defaultdict
from pathlib import Path

from app.llm import get_llm
from app.prompts import RAG_PROMPT
from app.search import search_documents


def format_sources(results) -> str:
    grouped_sources = defaultdict(set)

    for document, score in results:
        filename = Path(
            document.metadata.get("source", "Desconocido")
        ).name
        page = document.metadata.get("page", 0) + 1

        grouped_sources[filename].add(page)

    output = []

    for filename in sorted(grouped_sources):
        output.append(f"📄 {filename}")

        for page in sorted(grouped_sources[filename]):
            output.append(f"   • Página {page}")

        output.append("")

    return "\n".join(output)


def normalize_text(text: str) -> str:
    text = text.strip().lower()

    return "".join(
        character
        for character in unicodedata.normalize("NFD", text)
        if unicodedata.category(character) != "Mn"
    )


def get_greeting_response(question: str) -> str | None:
    normalized_question = normalize_text(question)

    greetings = {
        "hola",
        "buenos dias",
        "buenas tardes",
        "buenas noches",
        "hey",
        "holi",
        "que tal",
        "como estas",
    }

    if normalized_question in greetings:
        return (
            "¡Hola! 👋 Soy tu asistente de BimBam Buy. "
            "Puedes preguntarme sobre la información contenida "
            "en los documentos cargados por el administrador."
        )

    return None


def ask_question(question: str) -> str:
    greeting_response = get_greeting_response(question)

    if greeting_response:
        return greeting_response

    results = search_documents(question)

    context = "\n\n".join(
        document.page_content for document, score in results
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question,
    )

    llm = get_llm()
    response = llm.invoke(prompt)

    sources = format_sources(results)

    return f"{response}\n\nFuentes:\n{sources}"