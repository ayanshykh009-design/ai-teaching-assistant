import json
import logging
from pathlib import Path

from app.rag.embeddings import EmbeddingService
from app.rag.qdrant_service import QdrantService

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "app" / "knowledge"

COLLECTION_DIR_MAP = {
    "notes": "notes",
    "rubrics": "rubrics",
    "mistakes": "mistakes",
    "assignments": "assignments",
    "feedback_examples": "feedback_examples",
}

MAX_CHUNK_SIZE = 500


def chunk_text(text: str, max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    if not text.strip():
        return []
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        stripped = para.strip()
        if not stripped:
            continue
        if len(current) + len(stripped) + 2 < max_size:
            current = (current + "\n\n" + stripped).strip()
        else:
            if current:
                chunks.append(current)
            current = stripped
    if current:
        chunks.append(current)
    return chunks


def read_file(path: Path) -> str:
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return json.dumps(data, indent=2)
            return str(data)
        except (json.JSONDecodeError, OSError):
            pass
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Cannot read {path}: {exc}") from exc


class KnowledgeIngestor:
    def __init__(
        self, qdrant: QdrantService, embeddings: EmbeddingService
    ) -> None:
        self._qdrant = qdrant
        self._embeddings = embeddings

    def ingest_all(self) -> dict:
        results: dict[str, int] = {}
        for collection, subdir in COLLECTION_DIR_MAP.items():
            count = self._ingest_collection(collection, subdir)
            results[collection] = count
        logger.info("Ingestion complete: %s", results)
        return results

    def _ingest_collection(self, collection: str, subdir: str) -> int:
        dir_path = KNOWLEDGE_DIR / subdir
        if not dir_path.is_dir():
            logger.warning("Knowledge directory not found: %s", dir_path)
            return 0

        points = []
        for file_path in sorted(dir_path.iterdir()):
            if file_path.is_file() and file_path.suffix in {".md", ".txt", ".json", ".js"}:
                try:
                    text = read_file(file_path)
                    chunks = chunk_text(text)
                    for chunk in chunks:
                        points.append(
                            {
                                "text": chunk,
                                "source": str(file_path.relative_to(KNOWLEDGE_DIR)),
                            }
                        )
                except Exception as exc:
                    logger.warning("Failed to read %s: %s", file_path, exc)

        if not points:
            logger.info("No points to ingest for '%s'", collection)
            return 0

        texts = [p["text"] for p in points]
        vectors = self._embeddings.embed_batch(texts)

        for i, p in enumerate(points):
            p["vector"] = vectors[i]

        return self._qdrant.upsert(collection, points)
