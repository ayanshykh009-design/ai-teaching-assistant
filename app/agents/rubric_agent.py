from app.agents.base_agent import BaseAgent


class RubricAgent(BaseAgent):
    def _build_prompt(self, code: str, context: dict | None = None) -> str:
        ctx = context or {}
        context_section = ""
        if ctx:
            parts = []
            if ctx.get("mistakes"):
                parts.append(
                    "Mistakes found: " + "; ".join(ctx["mistakes"])
                )
            if ctx.get("concepts"):
                parts.append(
                    "Concepts covered: " + "; ".join(ctx["concepts"])
                )
            if parts:
                context_section = "Previous analysis:\n" + "\n".join(parts) + "\n\n"

        stored_rubrics = ""
        if ctx.get("rubrics"):
            stored_rubrics = "Reference grading rubric:\n" + ctx["rubrics"] + "\n\n"

        return (
            "You are an automated grading assistant. Score the following JavaScript code "
            "on these criteria (each out of 10):\n\n"
            f"{context_section}"
            f"{stored_rubrics}"
            "1. **correctness**: Does the code work correctly? Are there bugs?\n"
            "2. **efficiency**: Is the code efficient? Could it be optimized?\n"
            "3. **style**: Is the code well-formatted? Follows best practices?\n"
            "4. **documentation**: Are variables well-named? Is the code readable?\n\n"
            "Provide:\n"
            "- Individual scores (1-10) for each criterion\n"
            "- total_score (sum of all scores)\n"
            "- max_score (always 40)\n"
            "- comments explaining the reasoning\n\n"
            f"```js\n{code}\n```"
        )

    def _get_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "scores": {
                    "type": "object",
                    "properties": {
                        "correctness": {"type": "integer"},
                        "efficiency": {"type": "integer"},
                        "style": {"type": "integer"},
                        "documentation": {"type": "integer"},
                    },
                    "required": ["correctness", "efficiency", "style", "documentation"],
                },
                "total_score": {"type": "integer"},
                "max_score": {"type": "integer"},
                "comments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Explanatory comments for the scores",
                },
            },
            "required": ["scores", "total_score", "max_score", "comments"],
        }
