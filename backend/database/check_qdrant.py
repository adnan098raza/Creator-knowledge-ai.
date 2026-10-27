from qdrant_connection import client

COLLECTION_NAME = "transcript_chunks"

info = client.get_collection(COLLECTION_NAME)

print("Collection name:", COLLECTION_NAME)
print("Points count:", info.points_count)
print("Status:", info.status)
print("\nFull collection info:")
print(info)