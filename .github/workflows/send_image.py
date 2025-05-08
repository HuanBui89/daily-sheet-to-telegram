name: send_image

on:
  schedule:
    - cron: '0 2 * * *'  # 9h sáng Việt Nam (UTC+7)
  workflow_dispatch:

jobs:
  send:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Chrome & dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y wget unzip
          wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
          sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
          sudo apt-get install -y chromium-driver
          pip install --upgrade pip
          pip install selenium openai requests python-telegram-bot==13.15

      - name: Run bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          GROUP_CHAT_ID: ${{ secrets.GROUP_CHAT_ID }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python send_image.py
