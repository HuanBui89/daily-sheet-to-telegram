import os
import time
from shutil import which
import undetected_chromedriver as uc
from telegram import Bot
from openai import OpenAI

# === ENV ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === CONFIG ===
SHEET_URL = "https://docs.google.com/spreadsheets/d/1G7ql9O5J0nMJ9qkiOsadjPYATo3ZhCgXPTAlx8oUo4U/edit#gid=0"
SCREENSHOT_PATH = "sheet.png"

# === Chụp ảnh Google Sheet ===
def take_screenshot(url, output_path):
    print("📸 Đang khởi chạy Chrome để chụp ảnh...")

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

# === GPT Viết nhận xét chi tiết ===
def generate_comment():
    print("🧠 GPT đang viết nhận xét...")
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = """
Bạn là trưởng nhóm sales, đang đánh giá hiệu suất làm việc hàng ngày của nhóm HCM4.

Dữ liệu hôm nay:
- Mai Lan Anh dẫn đầu về bán mới, rất mạnh về khai thác KH mới.
- Tấn Đạt tăng trưởng tổng vượt trội nhưng mất điểm nặng vì bán mới quá thấp.
- Lục Tiểu Phụng duy trì tốt cả hai mảng.
- Tâm có tổng ổn nhưng cần duy trì đà tăng của bán mới.

Viết nhận xét gồm 2 phần:
1. Nhận định nhanh theo từng cá nhân (gạch đầu dòng rõ ràng).
2. Kêu gọi hành động chung cho toàn team với nội dung:
   - Toàn team chỉ có 1/4 BD đạt nhịp vượt target.
   - Nếu giữ nguyên tốc độ hiện tại, chỉ có Mai Lan Anh đạt.
   - Hành động ngay từ hôm nay:
     + Tăng tiếp cận KH mới ít nhất 2 lần/ngày.
     + Ưu tiên xử lý KH tiềm năng (đã có quan tâm/gửi báo giá).
     + Chăm sóc kỹ sau telesales để kéo lại deal.
     + Gặp khó, chủ động xin tệp hỗ trợ từ team lead.

Kết thúc bằng một câu động viên ngắn, mạnh mẽ.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là trưởng nhóm sales có tư duy chiến lược và truyền cảm hứng."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.8,
        max_tokens=350
    )

    return response.choices[0].message.content.strip()

# === Gửi báo cáo Telegram ===
def send_to_telegram():
    print("📤 Đang gửi báo cáo vào Telegram...")
    bot = Bot(token=TELEGRAM_TOKEN)

    with open(SCREENSHOT_PATH, "rb") as photo:
        comment = generate_comment()
        caption = f"📊 Báo cáo số liệu HCM4 sáng nay!\n\n🗣 {comment}"
        bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)

# === MAIN ===
if __name__ == "__main__":
    print("🚀 Bắt đầu gửi báo cáo tự động...")
    take_screenshot(SHEET_URL, SCREENSHOT_PATH)
    send_to_telegram()
    print("🎉 Gửi thành công!")
