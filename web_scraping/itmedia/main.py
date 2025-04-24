import pandas as pd
import os
import glob
from datetime import datetime
from scraper import scrape_itmedia_news
from spreadsheet import write_to_spreadsheet

def get_existing_titles_and_urls():
    existing_titles = set()
    existing_urls = set()
    files = glob.glob("data/itmedia_*.csv")
    for file in files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                existing_titles.update(df["title"].dropna().tolist())
                existing_urls.update(df["url"].dropna().tolist())
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            continue
    return existing_titles, existing_urls

def remove_duplicates(articles, existing_titles, existing_urls):
    filtered = []
    for article in articles:
        if article["title"] not in existing_titles and article["url"] not in existing_urls:
            filtered.append(article)
    return filtered

def main():
    articles = scrape_itmedia_news()

    # 重複チェック
    existing_titles, existing_urls = get_existing_titles_and_urls()
    articles = remove_duplicates(articles, existing_titles, existing_urls)

    # 結果が0件なら処理終了
    if not articles:
        print("新しい記事はありませんでした。")
        exit()

    # CSVに保存
    df = pd.DataFrame(articles)

    today = datetime.now().strftime("%Y%m%d")
    os.makedirs("data", exist_ok=True)
    filename = f"data/itmedia_news_{today}.csv"

    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"{len(articles)}件の記事を取得しました。CSVに保存しました。")
    write_to_spreadsheet(articles)

if __name__ == "__main__":
    main()
