import os
import time
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")  # VD: -1002254220043
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"

# ===== STEP 1: Chụp ảnh Google Sheet =====
print("📸 Đang chụp ảnh Google Sheet...")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_SHEET_URL)

time.sleep(5)  # Chờ trang load

screenshot_path = "sheet.png"
driver.save_screenshot(screenshot_path)
driver.quit()

print("✅ Đã chụp xong, chuẩn bị gửi Telegram...")

# ===== STEP 2: Gửi ảnh lên Telegram =====
bot = telegram.Bot(token=TELEGRAM_TOKEN)

with open(screenshot_path, "rb") as image_file:
    bot.send_photo(
        chat_id=CHAT_ID,
        photo=image_file,
        caption="📊 Báo cáo số liệu HCM4 sáng nay!"
    )

print("✅ Gửi thành công!")
