import asyncio
import logging

from app.agents.code_review_agent import CodeReviewAgent
from app.agents.feedback_agent import FeedbackAgent
from app.agents.rubric_agent import RubricAgent
from app.agents.tutor_agent import TutorAgent
from app.rag.retriever import Retriever
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.validators import FileValidator

logger = logging.getLogger(__name__)


class AssignmentOrchestrator:
    def __init__(self, gemini_service: GeminiService, retriever: Retriever | None = None) -> None:
        self.code_review_agent = CodeReviewAgent(gemini_service)
        self.tutor_agent = TutorAgent(gemini_service)
        self.rubric_agent = RubricAgent(gemini_service)
        self.feedback_agent = FeedbackAgent(gemini_service)
        self._retriever = retriever
        self._validator = FileValidator()

    async def review(self, code: str, filename: str = "") -> dict:
        logger.info("Starting multi-agent review for: %s", filename or "(no filename)")

        rag_context: dict[str, str] = {}
        if self._retriever is not None:
            try:
                rag_context = await asyncio.to_thread(self._retriever.retrieve_context, code)
                logger.info("RAG context retrieved: %d keys", len(rag_context))
            except Exception as exc:
                logger.warning("RAG retrieval failed (non-fatal): %s", exc)

        # Run file validators
        file_checks = self._validator.validate(filename)
        logger.info("File checks: filename=%s, structure=%s",
                     file_checks["filename_check"]["passed"],
                     file_checks["structure_check"]["passed"])

        code_review_ctx = {
            "filename": filename,
            **file_checks,
            **rag_context,
        }

        code_review = await self._run_agent(
            self.code_review_agent,
            code,
            code_review_ctx,
            fallback={
                "summary": "",
                "mistakes": [],
                "suggestions": [],
                "corrected_code": "",
                **file_checks,
            },
        )
        # Ensure file checks and corrected_code are present even if agent drops them
        if "filename_check" not in code_review:
            code_review["filename_check"] = file_checks["filename_check"]
        if "structure_check" not in code_review:
            code_review["structure_check"] = file_checks["structure_check"]
        if "corrected_code" not in code_review:
            code_review["corrected_code"] = ""
        logger.info("CodeReviewAgent completed")

        tutor = await self._run_agent(
            self.tutor_agent,
            code,
            {"mistakes": code_review.get("mistakes", []), **rag_context},
            fallback={
                "concepts_explained": [],
                "learning_resources": [],
                "misconceptions": [],
            },
        )
        logger.info("TutorAgent completed")

        rubric = await self._run_agent(
            self.rubric_agent,
            code,
            {
                "mistakes": code_review.get("mistakes", []),
                "concepts": tutor.get("concepts_explained", []),
                **rag_context,
            },
            fallback={
                "scores": {"correctness": 0, "efficiency": 0, "style": 0, "documentation": 0},
                "total_score": 0,
                "max_score": 40,
                "comments": ["Grading unavailable due to service error."],
            },
        )
        logger.info("RubricAgent completed")

        feedback = await self._run_agent(
            self.feedback_agent,
            code,
            {
                "summary": code_review.get("summary", ""),
                "mistakes": code_review.get("mistakes", []),
                "suggestions": code_review.get("suggestions", []),
                "concepts": tutor.get("concepts_explained", []),
                "misconceptions": tutor.get("misconceptions", []),
                "scores": rubric.get("scores", {}),
                **rag_context,
            },
            fallback={
                "strengths": [],
                "improvements": [],
                "overall_comment": "Feedback unavailable due to a service error.",
            },
        )
        logger.info("FeedbackAgent completed")

        return {
            "code_review": code_review,
            "tutor_explanation": tutor,
            "rubric": rubric,
            "feedback": feedback,
        }

    async def _run_agent(
        self,
        agent,
        code: str,
        context: dict | None = None,
        fallback: dict | None = None,
    ) -> dict:
        try:
            return await asyncio.to_thread(agent.run, code, context)
        except GeminiServiceError as exc:
            logger.exception("Agent %s failed", agent.__class__.__name__)
            if fallback is not None:
                logger.warning(
                    "Using fallback result for %s", agent.__class__.__name__
                )
                return fallback
            return {"error": str(exc)}
