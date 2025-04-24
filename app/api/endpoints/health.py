from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

from qdrant_client.models import Distance, VectorParams

"""
client.create_collection(
    collection_name="face_db",
    vectors_config=VectorParams(size=512,distance=Distance.EUCLID),
)

"""

