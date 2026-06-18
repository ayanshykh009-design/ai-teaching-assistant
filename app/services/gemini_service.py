import json
import logging
import os

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    pass


class GeminiService:
    def __init__(self) -> None:
        self._client: genai.Client | None = None
        self._model: str | None = None

    def _ensure_initialized(self) -> None:
        if self._client is not None:
            return
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise GeminiServiceError("GEMINI_API_KEY environment variable is not set")
        self._client = genai.Client(api_key=api_key)
        self._model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.2,
    ) -> dict:
        self._ensure_initialized()

        logger.info("Sending request to Gemini model: %s", self._model)

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=temperature,
                ),
            )

            result = response.parsed

            if result is None:
                text = (response.text or "").strip()
                if not text:
                    raise GeminiServiceError("Gemini returned an empty response")
                try:
                    result = json.loads(text)
                except json.JSONDecodeError as exc:
                    raise GeminiServiceError(
                        "Failed to parse Gemini response as JSON"
                    ) from exc

            if not isinstance(result, dict):
                raise GeminiServiceError(
                    f"Unexpected response type from Gemini: {type(result).__name__}"
                )

            logger.info("Gemini response received successfully")
            return result

        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.exception("Gemini API call failed")
            raise GeminiServiceError(f"Gemini API request failed: {exc}") from exc

    def review_code(self, code: str) -> dict:
        if not code.strip():
            raise GeminiServiceError("Cannot review empty code")

        prompt = (
            "You are an expert JavaScript instructor reviewing a beginner's code.\n\n"
            "Review the following JavaScript code and provide structured feedback.\n\n"
            "1. **Summary**: A brief overview of what the code does and overall quality.\n"
            "2. **Mistakes**: List specific syntax errors, logic errors, or bad practices. "
            "Explain each mistake simply so a beginner can understand.\n"
            "3. **Suggestions**: Provide actionable suggestions for improvement.\n\n"
            f"```js\n{code}\n```"
        )

        schema = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "mistakes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of specific mistakes found in the code",
                },
                "suggestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of actionable improvement suggestions",
                },
            },
            "required": ["summary", "mistakes", "suggestions"],
        }

        result = self.generate(prompt, schema, temperature=0.2)

        validated = {
            "summary": result.get("summary", "No summary provided."),
            "mistakes": result.get("mistakes", []),
            "suggestions": result.get("suggestions", []),
        }

        logger.info(
            "Gemini review completed: %d mistakes, %d suggestions",
            len(validated["mistakes"]),
            len(validated["suggestions"]),
        )

        return validated
