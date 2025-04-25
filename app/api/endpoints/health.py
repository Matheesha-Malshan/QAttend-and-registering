from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient(host="localhost", port=6333)

from qdrant_client.models import Distance, VectorParams

"""
client.create_collection(
    collection_name="face_db",
    vectors_config=VectorParams(size=512,distance=Distance.EUCLID),
)
"""

"""
import numpy as np


vectors = [np.random.rand(512).tolist() for _ in range(5)]


points = [
    PointStruct(id=i, vector=vec, payload={"label": f"person_{i}"})
    for i, vec in enumerate(vectors)
]


client.upsert(
    collection_name="face_db",
    points=points
)

print("Collection created and vectors inserted!")
"""