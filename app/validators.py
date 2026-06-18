import logging
from pathlib import Path

from app.assignment_config import ALLOWED_FILENAMES

logger = logging.getLogger(__name__)


class FileCheckResult:
    """Result of a single validation check."""

    def __init__(self, passed: bool, message: str) -> None:
        self.passed = passed
        self.message = message

    def to_dict(self) -> dict:
        return {"passed": self.passed, "message": self.message}


class FileValidator:
    """Validates uploaded file naming and expected assignment structure."""

    @staticmethod
    def validate_filename(filename: str) -> FileCheckResult:
        if not filename:
            return FileCheckResult(
                passed=False,
                message="No filename provided.",
            )
        basename = Path(filename).name
        if basename in ALLOWED_FILENAMES:
            return FileCheckResult(
                passed=True,
                message=f"Valid filename: {basename}",
            )
        allowed = ", ".join(ALLOWED_FILENAMES)
        return FileCheckResult(
            passed=False,
            message=f"Expected {allowed} but received {basename}",
        )

    @staticmethod
    def validate_structure(filename: str) -> FileCheckResult:
        if not filename:
            return FileCheckResult(passed=False, message="No file provided.")
        basename = Path(filename).name
        if basename in ALLOWED_FILENAMES:
            return FileCheckResult(
                passed=True,
                message="File is at the expected root level.",
            )
        return FileCheckResult(
            passed=False,
            message=f"Unexpected file: {basename}",
        )

    def validate(self, filename: str) -> dict[str, dict]:
        name_check = self.validate_filename(filename)
        struct_check = self.validate_structure(filename)
        return {
            "filename_check": name_check.to_dict(),
            "structure_check": struct_check.to_dict(),
        }
