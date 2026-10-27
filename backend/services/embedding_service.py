from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )
        print("Embedding model loaded!")

    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)

        return embedding.tolist()


if __name__ == "__main__":
    service = EmbeddingService()

    text = "The conversation discusses geopolitics between India and China."

    embedding = service.generate_embedding(text)

    print("\nText:")
    print(text)

    print("\nEmbedding dimensions:")
    print(len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])