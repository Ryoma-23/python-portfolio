from datetime import datetime
import requests
from bs4 import BeautifulSoup
import chardet


def scrape_itmedia_news():
    url = "https://www.itmedia.co.jp/news/"
    response = requests.get(url)
    raw_data = response.content
    detected = chardet.detect(raw_data)
    encoding = detected['encoding']

    html = raw_data.decode(encoding, errors='replace')

    if response.status_code != 200:
        print("取得に失敗しました")
        return []

    soup = BeautifulSoup(html, "html.parser")

    articles = []
    seen_urls = set()

    # トップページの見出し記事一覧を取得（2025年4月時点の構造）
    for item in soup.select("div.colBoxTitle h3 a"):
        title = item.get_text(strip=True)
        link = item.get("href")

        if link.startswith("/"):
            link = f"https://www.itmedia.co.jp{link}"

        if link in seen_urls:
            continue # すでに追加したURLはスキップ
        seen_urls.add(link)
    
        articles.append({
            "title": title,
            "url": link,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M") # 仮の日付
        })

    return articles
