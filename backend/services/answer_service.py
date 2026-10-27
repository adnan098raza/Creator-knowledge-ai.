import os

from dotenv import load_dotenv
from groq import Groq

from backend.services.search_service import SearchService


load_dotenv()


class AnswerService:

    def __init__(self):

        print("Initializing Answer Service...")

        self.search_service = SearchService()

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        print("Answer Service ready!")


    def answer_question(self, question: str):

        # Step 1: Search relevant podcast chunks
        search_results = self.search_service.search(
            question,
            limit=3
        )

        # Step 2: Build context from retrieved chunks
        context = "\n\n".join(
            [
                f"[Chunk {result.payload['chunk_index']} | "
                f"Timestamp {result.payload['start_time']}"
                f"-{result.payload['end_time']} seconds]\n"
                f"{result.payload['english_text']}"
                for result in search_results
            ]
        )

        # Step 3: Create grounded RAG prompt
        prompt = f"""
You are an AI assistant for a podcast knowledge system.

Answer the user's question using ONLY the podcast transcript context provided below.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "I couldn't find that information in the available transcript."
4. Give a clear and concise answer based on what was discussed.
5. If relevant, mention differing viewpoints expressed in the discussion.

PODCAST TRANSCRIPT CONTEXT:
{context}

USER QUESTION:
{question}
"""

        # Step 4: Generate answer with Groq
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer questions strictly using the "
                        "provided podcast transcript context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_completion_tokens=800
        )

        answer = response.choices[0].message.content

        return answer, search_results


if __name__ == "__main__":

    answer_service = AnswerService()

    question = (
        "What did they discuss about geopolitics "
        "and China's relationship with India?"
    )

    answer, sources = answer_service.answer_question(question)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")

    for source in sources:

        print(
            f"- Chunk {source.payload['chunk_index']} | "
            f"{source.payload['start_time']}"
            f"-{source.payload['end_time']} seconds"
        )