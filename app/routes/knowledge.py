import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ErrorResponse,
    KnowledgeAddRequest,
    KnowledgeAddResponse,
    KnowledgeDeleteResponse,
    KnowledgeIngestResponse,
    KnowledgeSearchResponse,
    KnowledgeStatsResponse,
)
from app.rag.embeddings import EmbeddingService
from app.rag.ingestion import KnowledgeIngestor
from app.rag.qdrant_service import QdrantService, QdrantServiceError
from app.rag.retriever import Retriever

logger = logging.getLogger(__name__)

router = APIRouter()

_qdrant: QdrantService | None = None
_embeddings: EmbeddingService | None = None
_retriever: Retriever | None = None
_ingestor: KnowledgeIngestor | None = None


def _ensure_rag() -> None:
    global _qdrant, _embeddings, _retriever, _ingestor
    if _qdrant is not None:
        return
    _qdrant = QdrantService()
    _embeddings = EmbeddingService()
    _retriever = Retriever(_qdrant, _embeddings)
    _ingestor = KnowledgeIngestor(_qdrant, _embeddings)


@router.post(
    "/knowledge/ingest",
    response_model=KnowledgeIngestResponse,
    responses={500: {"model": ErrorResponse}},
)
async def ingest_knowledge() -> KnowledgeIngestResponse:
    try:
        _ensure_rag()
        results = _ingestor.ingest_all()
        total = sum(results.values())
        return KnowledgeIngestResponse(collections=results, total_points=total)
    except Exception as exc:
        logger.exception("Knowledge ingestion failed")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}")


@router.get(
    "/knowledge/stats",
    response_model=KnowledgeStatsResponse,
    responses={500: {"model": ErrorResponse}},
)
async def knowledge_stats() -> KnowledgeStatsResponse:
    try:
        _ensure_rag()
        stats = _qdrant.stats()
        return KnowledgeStatsResponse(collections=stats)
    except Exception as exc:
        logger.exception("Failed to get knowledge stats")
        raise HTTPException(status_code=500, detail=f"Stats failed: {exc}")


@router.get(
    "/knowledge/search",
    response_model=KnowledgeSearchResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def search_knowledge(q: str, collection: str = "notes", limit: int = 5) -> KnowledgeSearchResponse:
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    try:
        _ensure_rag()
        results = _retriever.search_collection(collection, q, limit=limit)
        items = [
            {
                "id": r["id"],
                "score": r["score"],
                "text": r["text"],
                "source": r["source"],
            }
            for r in results
        ]
        return KnowledgeSearchResponse(query=q, collection=collection, results=items)
    except QdrantServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Knowledge search failed")
        raise HTTPException(status_code=500, detail=f"Search failed: {exc}")


@router.post(
    "/knowledge/add",
    response_model=KnowledgeAddResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def add_knowledge(body: KnowledgeAddRequest) -> KnowledgeAddResponse:
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        _ensure_rag()
        vector = _embeddings.embed(body.text)
        count = _qdrant.upsert(
            body.collection,
            [{"text": body.text, "source": body.source, "vector": vector}],
        )
        return KnowledgeAddResponse(collection=body.collection, points_added=count)
    except QdrantServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Failed to add knowledge")
        raise HTTPException(status_code=500, detail=f"Add failed: {exc}")


@router.delete(
    "/knowledge/{collection}/{point_id}",
    response_model=KnowledgeDeleteResponse,
    responses={500: {"model": ErrorResponse}},
)
async def delete_knowledge(collection: str, point_id: str) -> KnowledgeDeleteResponse:
    try:
        _ensure_rag()
        deleted = _qdrant.delete(collection, point_id)
        return KnowledgeDeleteResponse(collection=collection, deleted=deleted)
    except QdrantServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Failed to delete knowledge")
        raise HTTPException(status_code=500, detail=f"Delete failed: {exc}")
