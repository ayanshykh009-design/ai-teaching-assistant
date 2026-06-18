import asyncio
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import ErrorResponse, UploadResponse
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.utils import validate_and_save

logger = logging.getLogger(__name__)

router = APIRouter()

_gemini_service: GeminiService | None = None


def _get_gemini_service() -> GeminiService:
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


@router.post(
    "/upload",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    content = await file.read()
    filename = file.filename or ""
    code_text = validate_and_save(filename, content)

    logger.info("Processing review for file: %s (%d bytes)", filename, len(code_text))

    try:
        review = await asyncio.to_thread(_get_gemini_service().review_code, code_text)
    except GeminiServiceError as exc:
        logger.exception("Gemini service error during review")
        raise HTTPException(
            status_code=502, detail=f"Review service failed: {exc}"
        ) from exc

    logger.info("Review completed for file: %s", filename)
    return UploadResponse(filename=filename, review=review)
