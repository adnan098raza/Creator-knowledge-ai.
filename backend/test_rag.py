from backend.services.answer_service import AnswerService


def main():

    answer_service = AnswerService()

    questions = [
        "What did they discuss about China and India?",
        "What did they say about artificial intelligence?",
        "What was discussed about Pakistan?",
        "What did they say about Taiwan?",
        "What was discussed about the United States and Russia?"
    ]

    for i, question in enumerate(questions, start=1):

        print("\n" + "=" * 80)
        print(f"QUESTION {i}: {question}")
        print("=" * 80)

        answer, sources = answer_service.answer_question(question)

        print("\nANSWER:")
        print(answer)

        print("\nSOURCES:")

        for source in sources:
            print(
                f"- Chunk {source.payload['chunk_index']} | "
                f"{source.payload['start_time']:.2f}s "
                f"to {source.payload['end_time']:.2f}s | "
                f"Score: {source.score:.4f}"
            )

        print()

if __name__ == "__main__":
    main()