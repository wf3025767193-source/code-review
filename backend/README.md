# Backend

FastAPI backend for the AI code review tool.

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```text
GET http://localhost:8000/api/v1/health
```

## GitHub PR API

Fetch pull request metadata and changed files:

```text
POST http://localhost:8000/api/v1/github/pr
Content-Type: application/json

{
  "url": "https://github.com/owner/repo/pull/123"
}
```

Private repositories require `GITHUB_TOKEN` in `.env`.

If your browser can access GitHub but the backend cannot, configure an HTTP proxy:

```env
GITHUB_API_PROXY=http://127.0.0.1:7890
```
