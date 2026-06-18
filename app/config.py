import os
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
if not UPLOAD_DIR.is_absolute():
    UPLOAD_DIR = (_PROJECT_ROOT / UPLOAD_DIR).resolve()
try:
    UPLOAD_DIR.relative_to(_PROJECT_ROOT)
except ValueError:
    raise RuntimeError(f"UPLOAD_DIR '{UPLOAD_DIR}' is outside project root")

ALLOWED_EXTENSIONS = {".js"}
MAX_FILE_SIZE = 1_048_576

# Qdrant persistent storage
QDRANT_PATH = os.getenv("QDRANT_PATH", "qdrant_data")
if not os.path.isabs(QDRANT_PATH):
    QDRANT_PATH = str(_PROJECT_ROOT / QDRANT_PATH)

# Authentication
API_KEY = os.getenv("API_KEY", "")
API_KEY_ENABLED = API_KEY != ""

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Rate limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Upload retention (seconds, default 24h)
UPLOAD_RETENTION_SECONDS = int(os.getenv("UPLOAD_RETENTION_SECONDS", "86400"))

# HTTPS / SSL
SSL_ENABLED = os.getenv("SSL_ENABLED", "false").lower() == "true"
SSL_CERTFILE = os.getenv("SSL_CERTFILE", "")
SSL_KEYFILE = os.getenv("SSL_KEYFILE", "")
