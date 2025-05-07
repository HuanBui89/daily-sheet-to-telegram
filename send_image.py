import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ví dụ: -1002254220043
IMAGE_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/export?format=png&gid=0&range=A2:N26"

def send_photo_to_telegram():
    print("📥 Đang tải ảnh báo cáo...")

    response = requests.get(IMAGE_URL)
    if response.status_code != 200:
        raise Exception("Không thể tải ảnh từ Google Sheet.")

    print("✅ Đang gửi tới Telegram...")
    files = {'photo': response.content}
    data = {
        'chat_id': CHAT_ID,
        'caption': "📊 Báo cáo số liệu HCM4 sáng nay!"
    }

    res = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
        files={'photo': ('report.png', response.content)},
        data=data
    )

    if not res.ok:
        raise Exception(f"❌ Lỗi gửi Telegram: {res.text}")
    print("✅ Gửi thành công!")

if __name__ == "__main__":
    send_photo_to_telegram()
