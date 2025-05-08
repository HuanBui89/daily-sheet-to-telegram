import os
import time
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from telegram import Bot
from openai import OpenAI

# Lấy biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Sheet và đường dẫn ảnh
SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"
SCREENSHOT_PATH = "sheet.png"

def take_screenshot(url, output_path):
    print("📸 Đang khởi chạy Chrome để chụp ảnh...")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_path = "/usr/bin/google-chrome-stable"
    driver_path = "/usr/lib/chromium-browser/chromedriver"  # Hoặc bạn dùng: `which chromedriver`

    chrome_options.binary_location = chrome_path
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(10)
    driver.save_screenshot(output_path)
    driver.quit()
    print("✅ Chụp ảnh hoàn tất.")

def generate_comment():
    print("🧠 GPT đang viết nhận xét...")
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia đánh giá hiệu suất bán hàng."},
            {"role": "user", "content": "Viết nhận xét tích cực, ngắn gọn và truyền động lực cho team HCM4 dựa trên báo cáo hôm nay."}
        ],
        temperature=0.8,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def send_to_telegram():
    print("📤 Đang gửi báo cáo vào Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)

    with open(SCREENSHOT_PATH, "rb") as photo:
        comment = generate_comment()
        caption = f"📊 Báo cáo số liệu HCM4 sáng nay!\n\n🗣 Nhận xét:\n{comment}"
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)

if __name__ == "__main__":
    print("🚀 Bắt đầu gửi báo cáo tự động...")
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_to_telegram()
    print("🎉 Gửi thành công!")
