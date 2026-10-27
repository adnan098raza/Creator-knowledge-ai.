import json
from pathlib import Path

from backend.services.embedding_service import EmbeddingService
from backend.services.qdrant_service import QdrantService


class IngestionService:

    def __init__(self):

        print("Initializing Ingestion Service...")

        self.embedding_service = EmbeddingService()

        self.qdrant_service = QdrantService()

        print("Ingestion Service ready!")


    def load_translated_chunks(self):

        file_path = Path("translated_chunks.json")

        if not file_path.exists():
            raise FileNotFoundError(
                "translated_chunks.json not found!"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        return chunks


    def ingest_chunks(self):

        chunks = self.load_translated_chunks()

        print(f"\nChunks to ingest: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            print(
                f"\nProcessing chunk "
                f"{i + 1}/{len(chunks)}"
            )

            # Embed English text
            text_to_embed = chunk["english_text"]

            vector = (
                self.embedding_service
                .generate_embedding(text_to_embed)
            )

            payload = {

                "chunk_index": chunk["chunk_index"],

                "original_text": chunk["original_text"],

                "english_text": chunk["english_text"],

                "hinglish_text": chunk["hinglish_text"],

                "start_time": chunk["start_time"],

                "end_time": chunk["end_time"]

            }

            self.qdrant_service.store_chunk(
                chunk_id=chunk["chunk_index"],
                embedding=vector,
                payload=payload
            )

            print(
                f"Successfully stored chunk "
                f"{chunk['chunk_index']}"
            )

        print(
            "\nAll chunks successfully stored in Qdrant!"
        )


if __name__ == "__main__":

    ingestion_service = IngestionService()

    ingestion_service.ingest_chunks()