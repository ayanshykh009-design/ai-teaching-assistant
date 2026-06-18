import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

_shared_model = None


def _get_model():
    global _shared_model
    if _shared_model is not None:
        return _shared_model
    from sentence_transformers import SentenceTransformer
    logger.info("Loading embedding model: %s", EMBEDDING_MODEL)
    _shared_model = SentenceTransformer(EMBEDDING_MODEL)
    logger.info("Embedding model loaded (dim=%d)", EMBEDDING_DIMENSION)
    return _shared_model


class EmbeddingService:
    def embed(self, text: str) -> list[float]:
        model = _get_model()
        vec = model.encode(text, normalize_embeddings=True)
        return vec.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        model = _get_model()
        vecs = model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vecs]

    @property
    def dimension(self) -> int:
        return EMBEDDING_DIMENSION
