import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    REPO_URL = "https://raw.githubusercontent.com/Mokshaa-Joshi/news_bot/main"
    FILE_PATHS = {
        "Gujarat Samachar": "gs.txt",
        "Divya Bhaskar": "db.txt",
        "Sandesh": "s.txt"
    }

settings = Settings()
