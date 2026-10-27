from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from backend.database.qdrant_connection import get_qdrant_client


class QdrantService:

    COLLECTION_NAME = "podcast_chunks"

    def __init__(self):

        print("Connecting to Qdrant...")

        self.client = get_qdrant_client()

        self.create_collection()

        print("Qdrant service ready!")

    def create_collection(self):

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME not in collection_names:

            print(
                f"Creating collection: {self.COLLECTION_NAME}"
            )

            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

        else:

            print(
                f"Collection already exists: "
                f"{self.COLLECTION_NAME}"
            )

    def store_chunk(
        self,
        chunk_id,
        embedding,
        payload
    ):

        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload=payload
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point]
        )

    def get_collection_info(self):

        return self.client.get_collection(
            collection_name=self.COLLECTION_NAME
        )


if __name__ == "__main__":

    service = QdrantService()

    info = service.get_collection_info()

    print("\nCollection Info:")
    print(info)