import logging

from app.rag.embeddings import EmbeddingService
from app.rag.qdrant_service import QdrantService

logger = logging.getLogger(__name__)

COLLECTION_MAP = {
    "notes": "class_notes",
    "rubrics": "rubrics",
    "mistakes": "common_mistakes",
    "assignments": "assignment_instructions",
    "feedback_examples": "previous_feedback",
}


class Retriever:
    def __init__(
        self, qdrant: QdrantService, embeddings: EmbeddingService
    ) -> None:
        self._qdrant = qdrant
        self._embeddings = embeddings

    def search_collection(
        self, collection: str, query: str, limit: int = 3
    ) -> list[dict]:
        vector = self._embeddings.embed(query)
        return self._qdrant.search(collection, vector, limit=limit)

    def retrieve_context(self, code: str, limit: int = 3) -> dict:
        context: dict[str, str] = {}

        for collection, key in COLLECTION_MAP.items():
            try:
                results = self.search_collection(collection, code, limit=limit)
                texts = [r["text"] for r in results if r.get("text")]
                context[key] = "\n\n".join(texts) if texts else ""
                if texts:
                    logger.info(
                        "Retrieved %d results from '%s' for context key '%s'",
                        len(texts),
                        collection,
                        key,
                    )
            except Exception as exc:
                logger.warning("Failed to retrieve from '%s': %s", collection, exc)
                context[key] = ""

        return context
