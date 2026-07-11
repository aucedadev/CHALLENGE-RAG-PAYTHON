from app.ask import ask_question


def main():
    print("=" * 60)
    print("🤖 RAG BimBam Buy")
    print("Escribe 'salir' para terminar.")
    print("=" * 60)

    while True:
        question = input("\nPregunta: ")

        if question.lower() == "salir":
            print("\n¡Hasta luego!")
            break

        response = ask_question(question)

        print("\nRespuesta:")
        print(response)


if __name__ == "__main__":
    main()