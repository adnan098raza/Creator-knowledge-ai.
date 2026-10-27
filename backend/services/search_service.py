from backend.database.qdrant_connection import get_qdrant_client
from backend.services.embedding_service import EmbeddingService


COLLECTION_NAME = "podcast_chunks"


class SearchService:

    def __init__(self):

        print("Initializing search service...")

        self.embedding_service = EmbeddingService()

        self.qdrant_client = get_qdrant_client()

        print("Search service ready!")


    def search(self, query: str, limit: int = 3):

        # Convert question into embedding
        query_vector = (
            self.embedding_service
            .generate_embedding(query)
        )

        # Search Qdrant
        results = self.qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit
        ).points

        return results


if __name__ == "__main__":

    search_service = SearchService()

    query = "What was discussed about China and geopolitics?"

    results = search_service.search(query)

    print("\nSearch Results:\n")

    for result in results:

        print("Score:", result.score)

        print("\nEnglish:")
        print(result.payload["english_text"])

        print("\nHinglish:")
        print(result.payload["hinglish_text"])

        print("\nTimestamp:")
        print(
            result.payload["start_time"],
            "-",
            result.payload["end_time"]
        )

        print("-" * 70)