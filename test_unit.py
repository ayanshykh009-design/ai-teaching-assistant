import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def test_chunk_text_basic():
    from app.rag.ingestion import chunk_text

    result = chunk_text("Hello world")
    assert result == ["Hello world"], f"Expected ['Hello world'], got {result}"


def test_chunk_text_multiple_paragraphs():
    from app.rag.ingestion import chunk_text

    text = "A" * 300 + "\n\n" + "B" * 300
    result = chunk_text(text, max_size=500)
    assert len(result) >= 2, f"Expected at least 2 chunks, got {len(result)}"
    assert all(len(c) <= 500 for c in result)


def test_chunk_text_empty():
    from app.rag.ingestion import chunk_text

    result = chunk_text("")
    assert result == [], f"Expected [], got {result}"


def test_chunk_text_whitespace():
    from app.rag.ingestion import chunk_text

    result = chunk_text("   \n\n   ")
    assert result == [], f"Expected [], got {result}"


def test_read_file_md():
    from app.rag.ingestion import read_file

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# Hello")
        p = Path(f.name)
    try:
        result = read_file(p)
        assert result == "# Hello", f"Expected '# Hello', got {result}"
    finally:
        p.unlink(missing_ok=True)


def test_read_file_json():
    from app.rag.ingestion import read_file

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"key": "value"}, f)
        p = Path(f.name)
    try:
        result = read_file(p)
        parsed = json.loads(result)
        assert parsed["key"] == "value"
    finally:
        p.unlink(missing_ok=True)


def test_read_file_json_list():
    from app.rag.ingestion import read_file

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(["a", "b"], f)
        p = Path(f.name)
    try:
        result = read_file(p)
        assert result == "['a', 'b']", f"Got {result}"
    finally:
        p.unlink(missing_ok=True)


def test_read_file_nonexistent():
    from app.rag.ingestion import read_file

    try:
        read_file(Path("nonexistent_file_12345.txt"))
        assert False, "Should have raised"
    except (ValueError, OSError):
        pass


def test_config_import():
    from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

    assert ".js" in ALLOWED_EXTENSIONS
    assert MAX_FILE_SIZE > 0
    assert UPLOAD_DIR.is_dir() or UPLOAD_DIR.name == "uploads"


def test_knowledge_dir_exists():
    from app.rag.ingestion import KNOWLEDGE_DIR
    from app.rag.ingestion import COLLECTION_DIR_MAP

    assert KNOWLEDGE_DIR.is_dir()
    for subdir in COLLECTION_DIR_MAP.values():
        assert (KNOWLEDGE_DIR / subdir).is_dir(), f"Missing {subdir}"


def test_schemas_import():
    from app.models.schemas import (
        HealthResponse, ReviewResponse, UploadResponse, ErrorResponse,
        CodeReviewResult, TutorResult, RubricResult, FeedbackResult,
        ReviewResponseV2, KnowledgeStatsResponse, KnowledgeSearchResponse,
        KnowledgeAddRequest, KnowledgeAddResponse, KnowledgeDeleteResponse,
        KnowledgeIngestResponse,
    )
    # all good if no ImportError


def test_collection_map_keys():
    from app.rag.retriever import COLLECTION_MAP
    from app.rag.qdrant_service import COLLECTIONS as QDRANT_COLLECTIONS

    # Every collection in Qdrant must be in retriever map
    assert set(COLLECTION_MAP.keys()) == set(QDRANT_COLLECTIONS.keys())


def test_agent_schemas_match_orchestrator():
    from app.agents.code_review_agent import CodeReviewAgent
    from app.agents.tutor_agent import TutorAgent
    from app.agents.rubric_agent import RubricAgent
    from app.agents.feedback_agent import FeedbackAgent
    from app.models.schemas import CodeReviewResult, TutorResult, RubricResult, FeedbackResult

    cr_schema = CodeReviewAgent.__new__(CodeReviewAgent)._get_schema()
    assert set(cr_schema.get("required", [])) == {"summary", "mistakes", "suggestions"}
    assert "corrected_code" in cr_schema.get("properties", {})
    tr_schema = TutorAgent.__new__(TutorAgent)._get_schema()
    assert set(tr_schema.get("required", [])) == {"concepts_explained", "learning_resources", "misconceptions"}
    rr_schema = RubricAgent.__new__(RubricAgent)._get_schema()
    assert set(rr_schema.get("required", [])) == {"scores", "total_score", "max_score", "comments"}
    fr_schema = FeedbackAgent.__new__(FeedbackAgent)._get_schema()
    assert set(fr_schema.get("required", [])) == {"strengths", "improvements", "overall_comment"}


def test_tutor_prompt_includes_roman_urdu():
    from app.agents.tutor_agent import TutorAgent
    prompt = TutorAgent.__new__(TutorAgent)._build_prompt("code", {})
    assert "Roman Urdu" in prompt or "RomanUrdu" in prompt, "Tutor prompt must mention Roman Urdu"
    assert "yeh" in prompt, "Tutor prompt should include Roman Urdu example text"


def test_rag_singletons():
    from app.rag.embeddings import _get_model
    from app.rag.qdrant_service import get_qdrant, QdrantService

    q1 = QdrantService()
    q2 = QdrantService()
    assert q1._client is q2._client, "QdrantService should share singleton client"


def test_collections_descriptions():
    from app.rag.qdrant_service import COLLECTIONS

    assert len(COLLECTIONS) == 5
    for name, desc in COLLECTIONS.items():
        assert name, f"Empty collection name"
        assert desc, f"Empty description for {name}"


def test_production_config():
    from app.config import (
        QDRANT_PATH, API_KEY_ENABLED, CORS_ORIGINS, RATE_LIMIT_PER_MINUTE,
        UPLOAD_RETENTION_SECONDS, SSL_ENABLED, API_KEY,
    )
    assert isinstance(QDRANT_PATH, str) and len(QDRANT_PATH) > 0
    assert isinstance(API_KEY_ENABLED, bool)
    assert isinstance(CORS_ORIGINS, list) and len(CORS_ORIGINS) > 0
    assert RATE_LIMIT_PER_MINUTE > 0
    assert UPLOAD_RETENTION_SECONDS > 0
    assert isinstance(SSL_ENABLED, bool)
    assert isinstance(API_KEY, str)


def test_middleware_import():
    from app.middleware import AuthMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware
    assert AuthMiddleware is not None
    assert RateLimitMiddleware is not None
    assert SecurityHeadersMiddleware is not None


def test_health_response_schema():
    from app.models.schemas import HealthResponse
    h = HealthResponse(status="ok", service="test")
    assert h.version == "1.0.0"
    assert h.qdrant_connected is False
    assert h.auth_enabled is False
    assert h.client_host is None
    # Check serialization
    d = h.model_dump()
    assert d["status"] == "ok"
    assert d["version"] == "1.0.0"


def test_qdrant_persistent_path():
    from app.rag.qdrant_service import QdrantService, get_qdrant
    from app.config import QDRANT_PATH
    # Qdrant should be using the config path, not :memory:
    assert "memory" not in QDRANT_PATH, "Qdrant should use persistent path, not :memory:"
    assert "qdrant_data" in QDRANT_PATH


def test_global_exception_handler():
    from app.main import app
    routes = {r.path for r in app.routes}
    assert "/" in routes
    assert "/upload" in routes
    assert "/review" in routes


def test_rate_store_clears():
    from app.middleware import _rate_store
    _rate_store["test_ip"] = [0.0, 1.0]
    assert "test_ip" in _rate_store


def test_config_cors_default():
    from app.config import CORS_ORIGINS
    assert "http://localhost:3000" in CORS_ORIGINS


def test_validator_filename_valid():
    from app.validators import FileValidator
    r = FileValidator.validate_filename("app.js")
    assert r.passed is True
    assert "Valid" in r.message


def test_validator_filename_valid_index():
    from app.validators import FileValidator
    r = FileValidator.validate_filename("index.js")
    assert r.passed is True


def test_validator_filename_invalid():
    from app.validators import FileValidator
    r = FileValidator.validate_filename("test.js")
    assert r.passed is False
    assert "Expected" in r.message or "received" in r.message


def test_validator_filename_empty():
    from app.validators import FileValidator
    r = FileValidator.validate_filename("")
    assert r.passed is False


def test_validator_structure_valid():
    from app.validators import FileValidator
    r = FileValidator.validate_structure("app.js")
    assert r.passed is True


def test_validator_structure_invalid():
    from app.validators import FileValidator
    r = FileValidator.validate_structure("test.js")
    assert r.passed is False


def test_validator_integration():
    from app.validators import FileValidator
    v = FileValidator()
    r = v.validate("app.js")
    assert "filename_check" in r
    assert "structure_check" in r
    assert r["filename_check"]["passed"] is True
    assert r["structure_check"]["passed"] is True


def test_validator_invalid_integration():
    from app.validators import FileValidator
    v = FileValidator()
    r = v.validate("wrong.js")
    assert r["filename_check"]["passed"] is False
    assert r["structure_check"]["passed"] is False


def test_code_review_result_has_checks():
    from app.models.schemas import CodeReviewResult
    r = CodeReviewResult(summary="test", mistakes=[], suggestions=[])
    assert r.filename_check is None
    assert r.structure_check is None
    assert r.corrected_code is None
    # With values
    r2 = CodeReviewResult(
        summary="test", mistakes=[], suggestions=[],
        corrected_code="function test() { return 1; }",
        filename_check={"passed": True, "message": "ok"},
        structure_check={"passed": True, "message": "ok"},
    )
    assert r2.filename_check == {"passed": True, "message": "ok"}
    assert r2.corrected_code == "function test() { return 1; }"


def test_assignment_config():
    from app.assignment_config import ALLOWED_FILENAMES
    assert "app.js" in ALLOWED_FILENAMES
    assert "index.js" in ALLOWED_FILENAMES


def test_code_review_agent_schema_has_checks():
    from app.agents.code_review_agent import CodeReviewAgent
    schema = CodeReviewAgent.__new__(CodeReviewAgent)._get_schema()
    props = schema.get("properties", {})
    assert "filename_check" in props
    assert "structure_check" in props
    assert "corrected_code" in props
    assert props["corrected_code"]["type"] == "string"


if __name__ == "__main__":
    passed = 0
    failed = 0
    for name in sorted([k for k in dir() if k.startswith("test_")]):
        try:
            globals()[name]()
            print(f"  PASS {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL {name}: {e}")
            failed += 1
    print(f"\nUnit tests: {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
