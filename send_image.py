import os
import time
import undetected_chromedriver as uc
from telegram import Bot
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"
SCREENSHOT_PATH = "sheet.png"

def take_screenshot(url, output_path):
    print("📸 Đang mở trình duyệt Chrome tự động (UC)...")
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
    print("✅ Đã chụp ảnh Google Sheet.")

def generate_comment():
    print("🧠 GPT đang viết nhận xét...")
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia đánh giá hiệu suất bán hàng."},
            {"role": "user", "content": "Viết nhận xét tích cực, ngắn gọn cho team HCM4 dựa trên báo cáo hôm nay."}
        ],
        temperature=0.8,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def send_to_telegram():
    print("📤 Gửi báo cáo vào Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)
    with open(SCREENSHOT_PATH, "rb") as photo:
        comment = generate_comment()
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=f"📊 Báo cáo HCM4\n\n🗣 {comment}")

if __name__ == "__main__":
    print("🚀 Bắt đầu gửi báo cáo tự động...")
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_to_telegram()
    print("🎉 Gửi thành công!")
