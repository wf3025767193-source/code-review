from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.github import GitHubPR, GitHubPRRequest
from app.services.github_pr import GitHubPRService

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/pr", response_model=GitHubPR)
async def get_github_pr(
    request: GitHubPRRequest,
    settings: Settings = Depends(get_settings),
) -> GitHubPR:
    service = GitHubPRService(
        token=settings.github_token,
        proxy=settings.github_api_proxy,
    )
    return await service.fetch_pr(str(request.url))
