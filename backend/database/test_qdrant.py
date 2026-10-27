from qdrant_connection import client
from qdrant_client.models import Distance, VectorParams, PointStruct

COLLECTION_NAME = "test_vectors"

# Delete collection if it already exists (for repeatable testing)
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)

# Create collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=4,
        distance=Distance.COSINE
    )
)

print("Collection created!")

# Insert test vectors
client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, 0.4],
            payload={"text": "Psychology and human behaviour"}
        ),
        PointStruct(
            id=2,
            vector=[0.11, 0.21, 0.29, 0.41],
            payload={"text": "Human behavior in social groups"}
        ),
        PointStruct(
            id=3,
            vector=[0.9, 0.8, 0.7, 0.6],
            payload={"text": "How to cook Italian pasta"}
        )
    ]
)

print("Vectors inserted!")

# Search for similar vectors
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=[0.1, 0.2, 0.3, 0.4],
    limit=2
)

print("\nSimilarity Search Results:")
for point in results.points:
    print(point.id, point.score, point.payload)