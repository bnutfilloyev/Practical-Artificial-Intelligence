from eng2clips import NLP


def main():
    nlp = NLP()
    while True:

        val = input("Input English (1 sentence per time)\n >> ")

        if val.lower() == "exit":
            print("Bye!")
            break

        clips_cmd = nlp.process(val, render=False)

        print("\nCLIPS command: ", clips_cmd)


if __name__ == "__main__":
    main()
