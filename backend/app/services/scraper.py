import httpx
from app.config import SERPER_API_KEY


def search_company(company_name):
    response = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY},
        json={"q": f"{company_name} Qatar", "num": 5}
    )
    results = response.json().get("organic", [])
    return [{"title": r.get("title"), "snippet": r.get("snippet"), "link": r.get("link")} for r in results]


def search_company_news(company_name):
    response = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY},
        json={"q": f"{company_name} Qatar", "num": 5, "tbs": "qdr:w"}
    )
    results = response.json().get("organic", [])
    return [{"title": r.get("title"), "snippet": r.get("snippet"), "link": r.get("link")} for r in results]