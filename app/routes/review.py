import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import ErrorResponse, ReviewResponseV2
from app.orchestrator.assignment_orchestrator import AssignmentOrchestrator
from app.rag.embeddings import EmbeddingService
from app.rag.qdrant_service import QdrantService
from app.rag.retriever import Retriever
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.utils import validate_and_save

logger = logging.getLogger(__name__)

router = APIRouter()

_gemini_service: GeminiService | None = None
_orchestrator: AssignmentOrchestrator | None = None
_qdrant: QdrantService | None = None
_embeddings: EmbeddingService | None = None


def _get_orchestrator() -> AssignmentOrchestrator:
    global _gemini_service, _orchestrator, _qdrant, _embeddings
    if _gemini_service is None:
        _gemini_service = GeminiService()
    if _orchestrator is None:
        try:
            _qdrant = QdrantService()
            _embeddings = EmbeddingService()
            retriever = Retriever(_qdrant, _embeddings)
        except Exception as exc:
            logger.warning("RAG unavailable (non-fatal): %s", exc)
            retriever = None
        _orchestrator = AssignmentOrchestrator(_gemini_service, retriever=retriever)
    return _orchestrator


@router.post(
    "/review",
    response_model=ReviewResponseV2,
    responses={
        400: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def review_file(file: UploadFile = File(...)) -> ReviewResponseV2:
    content = await file.read()
    filename = file.filename or ""
    code_text = validate_and_save(filename, content)

    logger.info("Starting multi-agent review for: %s (%d bytes)", filename, len(code_text))

    try:
        review = await _get_orchestrator().review(code_text, filename=filename)
    except GeminiServiceError as exc:
        logger.exception("Multi-agent review failed")
        raise HTTPException(
            status_code=502, detail=f"Review service failed: {exc}"
        ) from exc
    except Exception as exc:
        logger.exception("Unhandled error in review pipeline")
        raise HTTPException(
            status_code=500, detail=f"Review pipeline error: {exc}"
        ) from exc

    logger.info("Multi-agent review completed for: %s", filename)

    try:
        return ReviewResponseV2(
            filename=filename,
            code_review=review["code_review"],
            tutor_explanation=review["tutor_explanation"],
            rubric=review["rubric"],
            feedback=review["feedback"],
        )
    except Exception as exc:
        logger.exception("Response model validation failed")
        raise HTTPException(
            status_code=500, detail=f"Response construction error: {exc}"
        ) from exc
