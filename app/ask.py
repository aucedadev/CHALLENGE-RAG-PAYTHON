from app.llm import get_llm
from app.search import search_documents
from app.prompts import RAG_PROMPT
from collections import defaultdict
from pathlib import Path

def format_sources(results) -> str:
    grouped_sources = defaultdict(set)

    for document, score in results:
        filename = Path(document.metadata.get("source", "Desconocido")).name
        page = document.metadata.get("page", 0) + 1

        grouped_sources[filename].add(page)

    output = []

    for filename in sorted(grouped_sources):
        output.append(f"📄 {filename}")

        for page in sorted(grouped_sources[filename]):
            output.append(f"   • Página {page}")

        output.append("")

    return "\n".join(output)

def ask_question(question: str) -> str:
    results = search_documents(question)

    context = "\n\n".join(
        document.page_content for document, score in results
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    llm = get_llm()
    response = llm.invoke(prompt)

    sources = format_sources(results)

    return f"{response}\n\nFuentes:\n{sources}"