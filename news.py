import requests

# 🔑 Put your NewsAPI key here
NEWS_API_KEY = "66f54301cbd048e29b20a0c5b025fbb3"  # ← Replace this with your API key


def fetch_crypto_news(query="cryptocurrency"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("articles", [])
    except Exception as e:
        print("News API Error:", e)
        return []
