# Backend Restructure Design

## Goal

Refactor the backend into smaller, consistently organized modules while keeping existing public API behavior compatible. Internal names and module boundaries may be adjusted when they make responsibilities clearer.

## Current Pain Points

- `app/services/llm_review.py` mixes prompt construction, LLM client creation, retry behavior, error classification, payload building, and JSON parsing.
- `app/services/github_pr.py` mixes PR URL parsing, GitHub HTTP calls, pagination, error mapping, schema conversion, service caching, and shutdown lifecycle.
- `app/agents/nodes.py` mixes LangGraph workflow nodes with review-context selection, patch truncation, result normalization, metrics recomputation, and response assembly.
- `app/api/v1/endpoints/health.py` mixes route handlers with readiness dependency probes.
- API endpoint files currently construct services directly, which makes dependency wiring inconsistent as the codebase grows.

## Chosen Approach

Use capability-based modules inside the existing backend structure. Keep `api`, `core`, `schemas`, `services`, and `agents`, but split large files into focused packages:

- `app/services/github/`
  - Parse GitHub PR URLs.
  - Build GitHub API headers.
  - Own the async HTTP client and pagination.
  - Map GitHub API responses into `GitHubPR` and `GitHubPRFile`.
  - Expose a cached service factory and shutdown helper.
- `app/services/llm/`
  - Build the LangChain chat model.
  - Build the review prompt.
  - Classify and sanitize LLM errors.
  - Retry retriable LLM failures.
  - Parse model output into `ReviewResult`.
  - Build mock review payloads.
- `app/agents/review/`
  - Keep graph construction and workflow node methods together.
  - Move context selection/truncation into a dedicated context builder.
  - Move analysis normalization and metrics recomputation into a dedicated normalizer.
  - Keep response assembly in the workflow layer.
- `app/services/health/`
  - Move readiness checks out of the route handler.
  - Keep `/health` and `/ready` route behavior compatible.

## Public Compatibility

- Keep existing HTTP paths, request models, response models, auth, and rate limiting behavior.
- Keep existing `uvicorn app.main:app` startup command.
- Preserve current GitHub and LLM error status codes and user-facing messages unless a small wording cleanup is required for consistency.
- Preserve `X-Request-ID` request logging behavior.

## Import Compatibility

Where low cost, provide compatibility exports so existing imports continue to work:

- `app.services.github_pr` should continue exposing `GitHubPRService`, `get_github_pr_service`, and `close_github_pr_services`.
- `app.services.llm_review` should continue exposing `LLMReviewService`.
- `app.agents.graph` and `app.agents.nodes` should continue exposing their current public classes while delegating to the new `app.agents.review` package.

## Testing And Verification

- Add focused tests for pure extraction logic where possible:
  - GitHub PR URL parsing.
  - Review context file selection and patch truncation.
  - Review result normalization.
  - LLM JSON extraction/parsing edge cases.
- Run backend tests if present.
- Run a Python compile check over `backend/app`.
- Verify imports used by endpoint modules still resolve.

## Non-Goals

- Do not introduce a database, background jobs, or new external services.
- Do not change frontend API usage.
- Do not rewrite the LangGraph workflow behavior beyond moving responsibilities into clearer files.
- Do not perform broad style-only rewrites outside the backend restructure.
