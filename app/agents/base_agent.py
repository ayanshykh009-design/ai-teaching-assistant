import logging
from abc import ABC, abstractmethod

from app.services.gemini_service import GeminiService, GeminiServiceError

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(self, gemini_service: GeminiService) -> None:
        self.gemini_service = gemini_service

    @abstractmethod
    def _build_prompt(self, code: str, context: dict | None = None) -> str:
        pass

    @abstractmethod
    def _get_schema(self) -> dict:
        pass

    def run(self, code: str, context: dict | None = None) -> dict:
        prompt = self._build_prompt(code, context)
        schema = self._get_schema()
        try:
            logger.info("%s running", self.__class__.__name__)
            return self.gemini_service.generate(prompt, schema)
        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.exception("%s failed", self.__class__.__name__)
            raise GeminiServiceError(f"{self.__class__.__name__} failed: {exc}") from exc
