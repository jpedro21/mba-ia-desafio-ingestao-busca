from search import search_prompt


def main():
    while True:
        question = input("Digite sua pergunta ou 'sair' para encerrar: ")
        if question.lower() == "sair":
            break
        response = search_prompt(question)
        print(response)

if __name__ == "__main__":
    main()