import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_to_spreadsheet(data, sheet_name="ITmedia News"):
    # 認証情報とスコープ
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("python-scraper-457813-100182638b77.json", scope)
    client = gspread.authorize(creds)

    # スプレッドシートを開く
    spreadsheet = client.open(sheet_name)
    worksheet = spreadsheet.sheet1

    # ヘッダー行の設定（1回目だけ）
    if not worksheet.get_all_values():
        worksheet.append_row(["title", "url", "date"])

    # データを書き込む（複数行）
    for row in data:
        worksheet.append_row([row["title"], row["url"], row["date"]])
