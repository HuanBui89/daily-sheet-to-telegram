import os
import time
import openai
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# === Biến môi trường ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === File và URL cần xử lý ===
SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/preview"
SCREENSHOT_PATH = "sheet.png"
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"

# === Cấu hình OpenAI client mới ===
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# === Chụp ảnh Google Sheet ===
def take_screenshot(url, output_path):
    print("📷 Đang chụp ảnh Google Sheet...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    time.sleep(10)  # Đợi trang Google Sheet load hoàn chỉnh
    driver.save_screenshot(output_path)
    driver.quit()

# === Tạo nhận xét bằng ChatGPT ===
def generate_comment():
    print("🧠 GPT đang viết nhận xét...")
    prompt = (
        "Viết một đoạn nhận xét tích cực, ngắn gọn (4-6 câu) về hiệu suất làm việc nhóm HCM4 hôm nay. "
        "Giọng văn truyền động lực, phong cách gần gũi, vui vẻ như một team leader Gen Z gửi cho team."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

# === Gửi ảnh + nhận xét lên Telegram ===
def send_to_telegram():
    print("📤 Đang gửi ảnh và nhận xét vào Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)
    comment = generate_comment()

    with open(SCREENSHOT_PATH, "rb") as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=f"📊 Báo cáo sáng nay:\n\n📝 {comment}")

# === MAIN ===
if __name__ == "__main__":
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_to_telegram()
