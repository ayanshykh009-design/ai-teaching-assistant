# AI Teaching Assistant

A production-ready FastAPI backend that provides AI-powered code reviews for JavaScript assignments using Google's Gemini API.

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd project
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your Gemini API key:

   ```env
   GEMINI_API_KEY=your_actual_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

   > Get a free API key at: https://aistudio.google.com/apikey

5. **Run the server**

   ```bash
   uvicorn app.main:app --reload
   ```

   Server starts at: http://127.0.0.1:8000

## API Documentation

Interactive Swagger docs are available at:

- http://127.0.0.1:8000/docs

## Endpoints

### `GET /`

Health check.

**Response:**

```json
{
  "status": "running",
  "service": "AI Teaching Assistant"
}
```

### `POST /upload`

Upload a JavaScript file for single-agent code review (Phase 1).

**Request:** `multipart/form-data` with field `file` containing a `.js` file.

**Response:**

```json
{
  "filename": "app.js",
  "review": {
    "summary": "...",
    "mistakes": ["...", "..."],
    "suggestions": ["...", "..."]
  }
}
```

### `POST /review`

Upload a JavaScript file for multi-agent code review (Phase 2).

Runs 4 agents sequentially: **CodeReview → Tutor → Rubric → Feedback**.

Each agent receives context from the previous one for deeper analysis.

**Request:** `multipart/form-data` with field `file` containing a `.js` file.

**Response:**

```json
{
  "filename": "app.js",
  "code_review": {
    "summary": "...",
    "mistakes": ["...", "..."],
    "suggestions": ["...", "..."]
  },
  "tutor_explanation": {
    "concepts_explained": ["...", "..."],
    "learning_resources": ["...", "..."],
    "misconceptions": ["...", "..."]
  },
  "rubric": {
    "scores": {
      "correctness": 8,
      "efficiency": 7,
      "style": 6,
      "documentation": 5
    },
    "total_score": 26,
    "max_score": 40,
    "comments": ["...", "..."]
  },
  "feedback": {
    "strengths": ["...", "..."],
    "improvements": ["...", "..."],
    "overall_comment": "..."
  }
}
```

## Architecture

### Phase 1 — Single Agent

```
POST /upload
    |
    ▼
GeminiService.review_code()
    |
    ▼
Structured review response
```

### Phase 2 — Multi-Agent Pipeline

```
POST /review
    |
    ▼
AssignmentOrchestrator
    |
    ├──► CodeReviewAgent   — syntax errors, logic mistakes, suggestions
    ├──► TutorAgent         — concept explanations, misconceptions, resources
    ├──► RubricAgent        — 4-criteria scoring (correctness, efficiency, style, docs)
    └──► FeedbackAgent      — strengths, improvements, encouraging comment
    |
    ▼
Combined response (4 agents)
```

Each agent has:
- A dedicated prompt engineered for its role
- Its own JSON response schema
- Context from prior agents (sequential pipeline)
- Graceful fallback if the agent fails (non-blocking)

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── agents/                    # Phase 2 — multi-agent system
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Abstract base with run/prompt/schema pattern
│   │   ├── code_review_agent.py   # Code review agent
│   │   ├── tutor_agent.py         # Tutoring agent
│   │   ├── rubric_agent.py        # Grading rubric agent
│   │   └── feedback_agent.py      # Feedback agent
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic response models (Phases 1 & 2)
│   │
│   ├── orchestrator/              # Phase 2 — pipeline coordinator
│   │   ├── __init__.py
│   │   └── assignment_orchestrator.py  # Runs agents sequentially with context
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py              # POST /upload (Phase 1)
│   │   └── review.py              # POST /review (Phase 2)
│   │
│   └── services/
│       ├── __init__.py
│       └── gemini_service.py      # Gemini API client (reused by all agents)
│
├── uploads/                       # Uploaded files stored here
├── .env / .env.example
├── requirements.txt
└── README.md
```

## Configuration

| Variable        | Default            | Description          |
| --------------- | ------------------ | -------------------- |
| `GEMINI_API_KEY` | —                 | Gemini API key       |
| `GEMINI_MODEL`   | `gemini-2.5-flash` | Gemini model name   |
| `UPLOAD_DIR`     | `uploads`          | Upload directory     |
