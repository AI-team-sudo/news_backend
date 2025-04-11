from fastapi import APIRouter, Query
from typing import List
from app.models.article import Article
from app.services.search_service import load_articles, search_articles
from app.utils.github_utils import download_articles_from_github
from app.core.config import settings

router = APIRouter()

@router.get("/search", response_model=List[Article])
def search_news(
    query: str = Query(..., description="Gujarati search keyword"),
    newspaper: str = Query(..., description="Newspaper name"),
    search_type: str = Query("contains", description="Search type: contains or matches with")
):
    content = download_articles_from_github(settings.REPO_URL, settings.FILE_PATHS[newspaper])
    if not content:
        return []
    articles = load_articles(content, newspaper)
    return search_articles(articles, query, search_type, newspaper)
