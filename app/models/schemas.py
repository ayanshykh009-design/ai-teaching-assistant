from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str = "1.0.0"
    qdrant_connected: bool = False
    auth_enabled: bool = False
    client_host: str | None = None


class ReviewResponse(BaseModel):
    summary: str
    mistakes: list[str]
    suggestions: list[str]


class UploadResponse(BaseModel):
    filename: str
    review: ReviewResponse


class ErrorResponse(BaseModel):
    detail: str


class CodeReviewResult(BaseModel):
    summary: str
    mistakes: list[str]
    suggestions: list[str]
    corrected_code: str | None = None
    filename_check: dict | None = None
    structure_check: dict | None = None


class TutorResult(BaseModel):
    concepts_explained: list[str]
    learning_resources: list[str]
    misconceptions: list[str]


class RubricResult(BaseModel):
    scores: dict[str, int]
    total_score: int
    max_score: int
    comments: list[str]


class FeedbackResult(BaseModel):
    strengths: list[str]
    improvements: list[str]
    overall_comment: str


class ReviewResponseV2(BaseModel):
    filename: str
    code_review: CodeReviewResult
    tutor_explanation: TutorResult
    rubric: RubricResult
    feedback: FeedbackResult


class KnowledgeStatsResponse(BaseModel):
    collections: dict[str, dict]


class KnowledgeSearchItem(BaseModel):
    id: str
    score: float
    text: str
    source: str


class KnowledgeSearchResponse(BaseModel):
    query: str
    collection: str
    results: list[KnowledgeSearchItem]


class KnowledgeAddRequest(BaseModel):
    collection: str
    text: str
    source: str = ""


class KnowledgeAddResponse(BaseModel):
    collection: str
    points_added: int


class KnowledgeDeleteResponse(BaseModel):
    collection: str
    deleted: bool


class KnowledgeIngestResponse(BaseModel):
    collections: dict[str, int]
    total_points: int
