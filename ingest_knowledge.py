import logging

from app.rag.embeddings import EmbeddingService
from app.rag.ingestion import KnowledgeIngestor
from app.rag.qdrant_service import QdrantService

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting knowledge ingestion")
    qdrant = QdrantService()
    embeddings = EmbeddingService()
    qdrant.ensure_collections()
    ingestor = KnowledgeIngestor(qdrant, embeddings)
    results = ingestor.ingest_all()
    for collection, count in results.items():
        logger.info("  %s: %d chunks ingested", collection, count)
    logger.info("Ingestion complete")


if __name__ == "__main__":
    main()
