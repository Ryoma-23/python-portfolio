import pandas as pd
import os
from datetime import datetime
from scraper import scrape_itmedia_news

def main():
    articles = scrape_itmedia_news()
    if not articles:
        print("記事が取得できませんでした。")
        return

    # CSVに保存
    df = pd.DataFrame(articles)

    today = datetime.now().strftime("%Y%m%d")
    os.makedirs("data", exist_ok=True)
    filename = f"data/itmedia_news_{today}.csv"

    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"{len(articles)}件の記事を取得しました。CSVに保存しました。")

if __name__ == "__main__":
    main()
