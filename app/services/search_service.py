import re
from typing import List, Dict
from app.models.article import Article

def load_articles(content: str, newspaper: str) -> List[str]:
    articles = []
    if content:
        content = content.replace("\r\n", "\n")
        if newspaper in ["Gujarat Samachar", "Divya Bhaskar"]:
            articles = content.split("="*80)
        elif newspaper == "Sandesh":
            articles = re.split(r"(?=\w{3} \d{1,2}, \d{4} \d{2}:\d{2} (am|pm))", content)
            articles = [a.strip() for a in articles if a.strip()]
    return [a.strip() for a in articles if a.strip()]

def parse_article(article: str, newspaper: str) -> Dict:
    article = article.strip().replace("\r\n", "\n")
    if newspaper in ["Gujarat Samachar", "Divya Bhaskar"]:
        match = re.search(r"Title:\s*(.*?)\nDate:\s*(.*?)\nLink:\s*(.*?)\nContent:\s*(.*)", article, re.DOTALL)
        if match:
            return {
                "title": match.group(1).strip(),
                "date": match.group(2).strip(),
                "link": match.group(3).strip(),
                "content": match.group(4).strip()
            }
    elif newspaper == "Sandesh":
        lines = article.split("\n")
        if len(lines) >= 3:
            return {
                "date": lines[0].strip(),
                "title": lines[1].strip(),
                "content": "\n".join(lines[2:]).strip()
            }
    return None

def search_articles(articles: List[str], query: str, search_type: str, newspaper: str) -> List[Article]:
    results = []
    if " અને " in query:
        query_keywords = query.strip().split(" અને ")
        keyword_pattern = r".*".join(re.escape(k) for k in query_keywords)
    elif " અથવા " in query or " કે " in query:
        query_keywords = re.split(r" અથવા | કે ", query.strip())
        keyword_pattern = r"|".join(re.escape(k) for k in query_keywords)
    else:
        query_keywords = [query.strip()]
        keyword_pattern = re.escape(query.strip())

    for article in articles:
        parsed = parse_article(article, newspaper)
        if parsed:
            content_to_search = f"{parsed['title']} {parsed['content']}".lower()
            if search_type == "contains":
                match = re.search(keyword_pattern, content_to_search, re.IGNORECASE)
            else:
                match = re.search(r"\b" + keyword_pattern + r"\b", content_to_search, re.IGNORECASE)
            if match:
                results.append(Article(**parsed))
    return results
