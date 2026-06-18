from app.agents.base_agent import BaseAgent


class TutorAgent(BaseAgent):
    def _build_prompt(self, code: str, context: dict | None = None) -> str:
        ctx = context or {}
        mistakes = ctx.get("mistakes", [])

        mistakes_section = ""
        if mistakes:
            mistakes_section = "The code review found these mistakes:\n"
            for m in mistakes:
                mistakes_section += f"- {m}\n"
            mistakes_section += "\n"

        class_notes = ""
        if ctx.get("class_notes"):
            class_notes = "Refer to these class notes when explaining concepts:\n" + ctx["class_notes"] + "\n\n"

        return (
            "You are a patient programming tutor helping a beginner understand JavaScript.\n\n"
            f"{mistakes_section}"
            f"{class_notes}"
            "Review the code and explain:\n\n"
            "1. **concepts_explained**: List the programming concepts this code demonstrates. "
            "Explain each in simple English mixed with Roman Urdu (e.g., 'yeh variable let se declare hota hai')\n"
            "2. **learning_resources**: Suggest specific topics or resources the student should study.\n"
            "3. **misconceptions**: Identify any misunderstandings the student likely has "
            "based on their code.\n\n"
            f"```js\n{code}\n```"
        )

    def _get_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "concepts_explained": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Programming concepts explained in simple terms",
                },
                "learning_resources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Suggested topics or resources to study",
                },
                "misconceptions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Likely misunderstandings the student has",
                },
            },
            "required": ["concepts_explained", "learning_resources", "misconceptions"],
        }
