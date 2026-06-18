from app.agents.base_agent import BaseAgent


class FeedbackAgent(BaseAgent):
    def _build_prompt(self, code: str, context: dict | None = None) -> str:
        ctx = context or {}
        context_section = "Previous analysis:\n"
        if "summary" in ctx:
            context_section += f"- Code summary: {ctx['summary']}\n"
        if ctx.get("mistakes"):
            context_section += (
                "- Mistakes identified: " + "; ".join(ctx["mistakes"]) + "\n"
            )
        if ctx.get("suggestions"):
            context_section += (
                "- Suggestions given: " + "; ".join(ctx["suggestions"]) + "\n"
            )
        if ctx.get("concepts"):
            context_section += (
                "- Concepts explained: " + "; ".join(ctx["concepts"]) + "\n"
            )
        if ctx.get("misconceptions"):
            context_section += (
                "- Misconceptions: " + "; ".join(ctx["misconceptions"]) + "\n"
            )
        if "scores" in ctx:
            s = ctx["scores"]
            total = sum(s.values()) if isinstance(s, dict) else 0
            context_section += f"- Rubric scores: {s} (total: {total}/40)\n"

        previous_feedback = ""
        if ctx.get("previous_feedback"):
            context_section += "\n"
            previous_feedback = "Examples of previous feedback:\n" + ctx["previous_feedback"] + "\n\n"

        context_section += "\n"

        return (
            "You are an encouraging programming instructor. "
            "Generate constructive, supportive feedback for the student.\n\n"
            f"{context_section}"
            f"{previous_feedback}"
            "Provide:\n\n"
            "1. **strengths**: What the student did well (list specific positives).\n"
            "2. **improvements**: What they should focus on improving (actionable items).\n"
            "3. **overall_comment**: A short, encouraging summary to motivate the student.\n\n"
            "Be supportive but honest. The goal is to help the student learn.\n\n"
            f"```js\n{code}\n```"
        )

    def _get_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific things the student did well",
                },
                "improvements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Actionable improvement suggestions",
                },
                "overall_comment": {
                    "type": "string",
                    "description": "Encouraging summary comment",
                },
            },
            "required": ["strengths", "improvements", "overall_comment"],
        }
