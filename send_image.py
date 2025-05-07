import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"
SCREENSHOT_PATH = "sheet.png"

def take_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(10)  # Đợi sheet load xong
    driver.save_screenshot(output_path)
    driver.quit()

def send_photo_to_telegram():
    print("📤 Đang gửi ảnh vào Telegram...")

    bot = Bot(token=TELEGRAM_TOKEN)
    with open(SCREENSHOT_PATH, "rb") as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption="📊 Báo cáo số liệu HCM4 sáng nay!")

if __name__ == "__main__":
    print("📷 Đang chụp ảnh Google Sheet...")
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)

    send_photo_to_telegram()
