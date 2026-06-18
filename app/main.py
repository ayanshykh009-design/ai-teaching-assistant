import json
import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import CORS_ORIGINS, SSL_ENABLED, UPLOAD_DIR, UPLOAD_RETENTION_SECONDS
from app.middleware import register_middleware
from app.models.schemas import ErrorResponse, HealthResponse
from app.rag.qdrant_service import QdrantService
from app.routes.knowledge import router as knowledge_router
from app.routes.review import router as review_router
from app.routes.upload import router as upload_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


def cleanup_old_uploads() -> None:
    """Remove uploaded files older than UPLOAD_RETENTION_SECONDS."""
    if not UPLOAD_DIR.is_dir():
        return
    now = time.time()
    cutoff = now - UPLOAD_RETENTION_SECONDS
    removed = 0
    for f in UPLOAD_DIR.iterdir():
        if f.is_file():
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
                    removed += 1
            except OSError:
                pass
    if removed:
        logger.info("Cleaned up %d old upload files (retention=%ds)", removed, UPLOAD_RETENTION_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    upload_dir = UPLOAD_DIR
    upload_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Upload directory ensured at: %s", upload_dir.resolve())
    try:
        qdrant = QdrantService()
        qdrant.ensure_collections()
        logger.info("Qdrant collections ensured at: %s", os.environ.get("QDRANT_PATH", "qdrant_data"))
    except Exception as exc:
        logger.warning("Qdrant initialization failed (non-fatal): %s", exc)
    cleanup_old_uploads()
    yield


app = FastAPI(
    title="AI Teaching Assistant",
    description="AI Teaching Assistant with multi-agent code review, RAG memory, and Qdrant knowledge base.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow only configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Auth, rate-limit, security headers
register_middleware(app)

app.include_router(upload_router, tags=["Upload"])
app.include_router(review_router, tags=["Review"])
app.include_router(knowledge_router, tags=["Knowledge"])


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check(request: Request) -> HealthResponse:
    qdrant_ok = False
    try:
        from app.rag.qdrant_service import get_qdrant
        get_qdrant()
        qdrant_ok = True
    except Exception:
        pass
    return HealthResponse(
        status="running",
        service="AI Teaching Assistant",
        version="1.0.0",
        qdrant_connected=qdrant_ok,
        auth_enabled=os.getenv("API_KEY", "") != "",
        client_host=request.client.host if request.client else None,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
