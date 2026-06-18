import logging
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.config import QDRANT_PATH

logger = logging.getLogger(__name__)

COLLECTIONS = {
    "notes": "Class notes and lecture material",
    "rubrics": "Grading rubrics",
    "mistakes": "Common student mistakes",
    "assignments": "Assignment instructions",
    "feedback_examples": "Previous feedback examples",
}

_shared_client: QdrantClient | None = None


class QdrantServiceError(Exception):
    pass


def get_qdrant(dimension: int = 384) -> QdrantClient:
    global _shared_client
    if _shared_client is not None:
        return _shared_client
    try:
        _shared_client = QdrantClient(path=QDRANT_PATH)
        logger.info("Qdrant in-memory client created")
    except Exception as exc:
        raise QdrantServiceError(f"Failed to create Qdrant client: {exc}") from exc
    for name in COLLECTIONS:
        try:
            if _shared_client.collection_exists(collection_name=name):
                continue
            _shared_client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=dimension, distance=Distance.COSINE
                ),
            )
            logger.info("Collection created: %s", name)
        except Exception as exc:
            raise QdrantServiceError(
                f"Failed to create collection '{name}': {exc}"
            ) from exc
    return _shared_client


class QdrantService:
    def __init__(self, dimension: int = 384) -> None:
        self._dimension = dimension
        self._client = get_qdrant(dimension=dimension)

    def ensure_collections(self) -> None:
        get_qdrant(dimension=self._dimension)

    def upsert(self, collection: str, points: list[dict]) -> int:
        if collection not in COLLECTIONS:
            raise QdrantServiceError(f"Unknown collection: {collection}")
        if not points:
            return 0
        point_structs = []
        for p in points:
            point_id = p.get("id", uuid.uuid4().hex)
            point_structs.append(
                PointStruct(
                    id=point_id,
                    vector=p["vector"],
                    payload={"text": p["text"], "source": p.get("source", ""), "metadata": p.get("metadata", {})},
                )
            )
        try:
            self._client.upsert(collection_name=collection, points=point_structs)
            logger.info("Upserted %d points to '%s'", len(point_structs), collection)
            return len(point_structs)
        except Exception as exc:
            raise QdrantServiceError(
                f"Failed to upsert to '{collection}': {exc}"
            ) from exc

    def search(self, collection: str, vector: list[float], limit: int = 5) -> list[dict]:
        if collection not in COLLECTIONS:
            raise QdrantServiceError(f"Unknown collection: {collection}")
        try:
            results = self._client.query_points(
                collection_name=collection,
                query=vector,
                limit=limit,
            )
            return [
                {
                    "id": str(p.id),
                    "score": p.score,
                    "text": p.payload.get("text", ""),
                    "source": p.payload.get("source", ""),
                }
                for p in results.points
            ]
        except Exception as exc:
            logger.exception("Search failed on '%s'", collection)
            raise QdrantServiceError(f"Search failed on '{collection}': {exc}") from exc

    def delete(self, collection: str, point_id: str) -> bool:
        if collection not in COLLECTIONS:
            raise QdrantServiceError(f"Unknown collection: {collection}")
        try:
            self._client.delete(
                collection_name=collection,
                points_selector=[point_id],
            )
            logger.info("Deleted point %s from '%s'", point_id, collection)
            return True
        except Exception as exc:
            raise QdrantServiceError(
                f"Failed to delete from '{collection}': {exc}"
            ) from exc

    def stats(self) -> dict:
        result = {}
        for name in COLLECTIONS:
            try:
                info = self._client.get_collection(collection_name=name)
                result[name] = {
                    "points_count": info.points_count,
                    "description": COLLECTIONS[name],
                }
            except Exception:
                result[name] = {"points_count": 0, "description": COLLECTIONS[name]}
        return result

    def close(self) -> None:
        pass
