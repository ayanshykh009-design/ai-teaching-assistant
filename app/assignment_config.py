import os

ALLOWED_FILENAMES = os.getenv(
    "ALLOWED_FILENAMES", "app.js,index.js"
).split(",")

# Expected assignment structure — mapping of role to expected files
# 'required' files must be present; 'optional' files are suggested
ASSIGNMENT_STRUCTURE: dict[str, dict[str, list[str]]] = {
    "default": {
        "required": [],
        "optional": [],
    },
}
