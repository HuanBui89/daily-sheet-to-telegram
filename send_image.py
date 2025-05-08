import os
import requests
import openai
from telegram import Bot

# 🔐 ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IMAGE_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/export?format=png&gid=0&range=A2:N26"

# ✅ Cấu hình OpenAI
openai.api_key = OPENAI_API_KEY

# 🧠 Hàm lấy đánh giá tự động từ GPT
def get_gpt_comment():
    prompt = """
    Dựa trên báo cáo bán hàng của một nhóm nhân viên, hãy đưa ra một đoạn nhận xét ngắn (5-7 câu) thể hiện tình hình hiện tại, nhấn mạnh người đang làm tốt, người cần cải thiện, và kêu gọi hành động tích cực. Văn phong tích cực, ngắn gọn, rõ ràng như 1 team leader gửi cho team.    
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200,
    )
    return response.choices[0].message["content"]

# 📤 Gửi ảnh kèm đánh giá
def send_photo_to_telegram():
    print("📥 Đang tải ảnh báo cáo...")
    response = requests.get(IMAGE_URL)
    if response.status_code != 200:
        raise Exception("Không thể tải ảnh từ Google Sheet.")

    photo_data = response.content
    comment = get_gpt_comment()

    print("📤 Đang gửi tới Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_photo(chat_id=CHAT_ID, photo=photo_data, caption=f"📊 Báo cáo sáng nay:\n\n{comment}")

# ▶️ Run
if __name__ == "__main__":
    send_photo_to_telegram()
