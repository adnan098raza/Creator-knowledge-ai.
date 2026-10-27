import atexit
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

QDRANT_PATH = os.getenv("QDRANT_PATH")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


@lru_cache(maxsize=1)
def get_qdrant_client():
    """Use local on-disk Qdrant when QDRANT_PATH is set, otherwise Qdrant Cloud."""
    if QDRANT_PATH:
        path = Path(QDRANT_PATH)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        local_client = QdrantClient(path=str(path))
        # Close before interpreter shutdown to avoid noisy __del__ errors
        atexit.register(local_client.close)
        return local_client

    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )


client = get_qdrant_client()

if __name__ == "__main__":
    try:
        collections = client.get_collections()
        print("Successfully connected to Qdrant!")
        print("Mode:", "local" if QDRANT_PATH else "cloud")
        print("Collections:", collections)
    except Exception as e:
        print("Qdrant connection failed:", e)
