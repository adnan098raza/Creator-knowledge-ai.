import sys
import uuid

sys.path.append(".")

from sqlalchemy import create_engine, text
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from backend.services.embedding_service import EmbeddingService
from dotenv import load_dotenv
import os


load_dotenv()

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Qdrant connection
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "transcript_chunks"


def ingest_chunks():

    # Load embedding model
    embedding_service = EmbeddingService()

    # Get chunks from PostgreSQL
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT id, transcript_id, chunk_index, chunk_text,
                       start_time_seconds, end_time_seconds
                FROM transcript_chunks
            """)
        )

        chunks = result.fetchall()

    print(f"Found {len(chunks)} chunks.")

    points = []

    for chunk in chunks:

        chunk_id = str(chunk.id)

        # Generate embedding
        embedding = embedding_service.generate_embedding(
            chunk.chunk_text
        )

        # Qdrant point
        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "transcript_id": str(chunk.transcript_id),
                "chunk_index": chunk.chunk_index,
                "chunk_text": chunk.chunk_text,
                "start_time_seconds": chunk.start_time_seconds,
                "end_time_seconds": chunk.end_time_seconds
            }
        )

        points.append(point)

    # Upload to Qdrant
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

        print(f"Successfully uploaded {len(points)} chunks to Qdrant!")

    else:
        print("No chunks found.")


if __name__ == "__main__":
    ingest_chunks()