import requests

def download_articles_from_github(repo_url, filename):
    url = f"{repo_url}/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
