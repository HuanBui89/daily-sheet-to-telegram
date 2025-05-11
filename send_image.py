import os
import time
import undetected_chromedriver as uc
from telegram import Bot
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === ENV ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"
SHEET_ID = "1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U"
SCREENSHOT_PATH = "sheet.png"

# === Chụp ảnh Sheet ===
def take_screenshot(url, output_path):
    print("📸 Đang chụp ảnh Google Sheet...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(10)
    driver.save_screenshot(output_path)
    driver.quit()
    print("✅ Đã chụp xong.")

# === Đọc dữ liệu Google Sheet ===
def get_sales_data():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID)
    worksheet = sheet.get_worksheet(0)  # sheet đầu tiên
    data = worksheet.get_all_values()
    rows = data[1:]  # bỏ header

    # Giả định: [Tên, Doanh thu hôm nay, Bán mới, Hôm qua]
    result = ""
    for row in rows:
        name = row[0]
        total = row[1]
        new_sale = row[2]
        yesterday = row[3] if len(row) > 3 else "0"
        result += f"{name}: Hôm nay {total} triệu | Bán mới: {new_sale} triệu | Hôm qua: {yesterday} triệu\n"

    return result.strip()

# === GPT phân tích nhận xét ===
def generate_comment():
    print("🧠 GPT đang phân tích dữ liệu...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    sales_text = get_sales_data()

    prompt = f"""
Dưới đây là số liệu doanh thu team HCM4 hôm nay:

{sales_text}

Yêu cầu:
1. Nhận định nhanh từng người (tổng, bán mới, tăng giảm so với hôm qua).
2. Dự báo doanh thu cuối tháng nếu giữ tốc độ này.
3. Tính phần còn thiếu để đạt 80 triệu/người.
4. Hành động toàn team nên làm từ hôm nay.
5. Kết thúc bằng một câu động viên mạnh mẽ.

Viết ngắn gọn, rõ ràng, theo phong cách trưởng nhóm sales chuyên nghiệp.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là trưởng nhóm sales chuyên nghiệp, có chiến lược và biết truyền cảm hứng."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.8,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

# === Gửi ảnh + nhận xét vào Telegram ===
def send_to_telegram():
    print("📤 Đang gửi báo cáo vào Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)

    # Gửi ảnh trước
    with open(SCREENSHOT_PATH, "rb") as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption="📊 Báo cáo doanh thu hôm nay")

    # Gửi đoạn GPT nhận xét sau ảnh
    comment = generate_comment()
    bot.send_message(chat_id=CHAT_ID, text=f"🧠 GPT Nhận xét:\n\n{comment}")

# === MAIN ===
if __name__ == "__main__":
    print("🚀 Bắt đầu gửi báo cáo...")
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_to_telegram()
    print("🎉 Gửi xong!")
