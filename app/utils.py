import logging
import uuid
from pathlib import Path

from fastapi import HTTPException

from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR

logger = logging.getLogger(__name__)


def validate_and_save(filename: str, content: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning("Rejected file with extension: %s", ext)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Only .js files are accepted.",
        )

    if not content or not content.strip():
        logger.warning("Empty file uploaded: %s", filename)
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(content) > MAX_FILE_SIZE:
        logger.warning("File too large: %s (%d bytes)", filename, len(content))
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum size of {MAX_FILE_SIZE // 1024} KB",
        )

    safe_name = Path(filename).name
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    save_path = UPLOAD_DIR / unique_name

    try:
        save_path.write_bytes(content)
        logger.info("Saved uploaded file to: %s", save_path)
    except OSError as exc:
        logger.exception("Failed to save uploaded file")
        raise HTTPException(
            status_code=500, detail=f"Failed to save file: {exc}"
        ) from exc

    return content.decode("utf-8", errors="replace")
