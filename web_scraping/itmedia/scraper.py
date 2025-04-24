import requests
from bs4 import BeautifulSoup

def scrape_itmedia_news():
    url = "https://www.itmedia.co.jp/news/"
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print("取得に失敗しました")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    articles = []

    # トップページの見出し記事一覧を取得（2025年4月時点の構造）
    for item in soup.select("div.colBoxTitle h3 a"):
        title = item.get_text(strip=True)
        link = item.get("href")

        if link.startswith("/"):
            link = f"https://www.itmedia.co.jp{link}"

        articles.append({
            "title": title,
            "url": link
        })

    return articles
