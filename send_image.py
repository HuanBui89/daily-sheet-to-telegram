import requests
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")

# ✅ Thay bằng link export Google Sheet dạng PNG (lưu ý file công khai!)
IMAGE_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAIx8oUo4U/export?format=png&id=1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAIx8oUo4U&gid=0&range=A2:N26"

bot = Bot(token=TELEGRAM_TOKEN)
print("📤 Đang tải ảnh báo cáo...")
image_data = requests.get(IMAGE_URL).content
print("✅ Đang gửi tới Telegram...")
bot.send_photo(chat_id=CHAT_ID, photo=image_data, caption="📊 Báo cáo số liệu HCM4 sáng nay!")
print("🎉 Đã gửi thành công.")
