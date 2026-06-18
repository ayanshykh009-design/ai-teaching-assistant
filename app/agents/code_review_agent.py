from app.agents.base_agent import BaseAgent


class CodeReviewAgent(BaseAgent):
    def _build_prompt(self, code: str, context: dict | None = None) -> str:
        ctx = context or {}

        common_mistakes = ""
        if ctx.get("common_mistakes"):
            common_mistakes = "Reference common mistakes students make:\n" + ctx["common_mistakes"] + "\n\n"

        checks_section = ""
        fc = ctx.get("filename_check")
        sc = ctx.get("structure_check")
        if fc or sc:
            checks_section = "Assignment requirement checks:\n"
            if fc:
                status = "✅ Valid" if fc.get("passed") else "❌ Invalid"
                checks_section += f"  Filename Check: {status} — {fc.get('message', '')}\n"
            if sc:
                status = "✅ Valid" if sc.get("passed") else "❌ Invalid"
                checks_section += f"  Structure Check: {status} — {sc.get('message', '')}\n"
            checks_section += (
                "Include these exact check results in your response "
                "under filename_check and structure_check fields.\n\n"
            )

        return (
            "You are an expert JavaScript code reviewer. "
            "Review the following code and provide structured feedback.\n\n"
            f"{common_mistakes}"
            f"{checks_section}"
            "1. **Summary**: A brief overview of what the code does and overall quality.\n"
            "2. **Mistakes**: List specific syntax errors, logic errors, or bad practices. "
            "Explain each mistake simply so a beginner can understand.\n"
            "3. **Suggestions**: Provide actionable suggestions for improvement.\n"
            "4. **Corrected Code**: Provide a fully corrected version of the code "
            "with all mistakes fixed and improvements applied. "
            "Wrap the corrected code in a single JavaScript code block.\n\n"
            f"```js\n{code}\n```"
        )

    def _get_schema(self) -> dict:
        return {
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
                "corrected_code": {
                    "type": "string",
                    "description": "Fully corrected version of the code with all mistakes fixed, wrapped in a JavaScript code block",
                },
                "filename_check": {
                    "type": "object",
                    "properties": {
                        "passed": {"type": "boolean"},
                        "message": {"type": "string"},
                    },
                    "description": "Result of filename validation check",
                },
                "structure_check": {
                    "type": "object",
                    "properties": {
                        "passed": {"type": "boolean"},
                        "message": {"type": "string"},
                    },
                    "description": "Result of folder structure validation check",
                },
            },
            "required": ["summary", "mistakes", "suggestions"],
        }
