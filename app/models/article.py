from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    date: str
    content: str
    link: Optional[str] = None
