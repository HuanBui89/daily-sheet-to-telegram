import os
import time
import requests
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# Load biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cấu hình API key của OpenAI
openai.api_key = OPENAI_API_KEY

# Google Sheet cần chụp
SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/preview"
SCREENSHOT_PATH = "sheet.png"

def take_screenshot(url, output_path):
    print("📷 Đang chụp ảnh Google Sheet...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(10)  # Chờ Google Sheet load xong
    driver.save_screenshot(output_path)
    driver.quit()

def generate_comment():
    print("🧠 Đang tạo nhận xét tự động từ GPT...")
    prompt = (
        "Viết một đoạn nhận xét truyền động lực về hiệu suất làm việc của nhóm HCM4 trong báo cáo, "
        "ngắn gọn, rõ ràng, mang phong cách Gen Z, tích cực, hỗ trợ thúc đẩy tinh thần đội nhóm."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def send_photo_to_telegram():
    print("📤 Đang gửi ảnh vào Telegram...")

    bot = Bot(token=TELEGRAM_TOKEN)

    if not os.path.exists(SCREENSHOT_PATH):
        raise Exception("Ảnh chưa được tạo!")

    with open(SCREENSHOT_PATH, "rb") as photo:
        caption = f"📊 Báo cáo số liệu HCM4 sáng nay!\n\n📝 {generate_comment()}"
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)

if __name__ == "__main__":
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_photo_to_telegram()
