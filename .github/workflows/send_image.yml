name: send_image

on:
  schedule:
    - cron: '0 2 * * *' # 9h sáng giờ VN (UTC+7)
  workflow_dispatch:

jobs:
  send_image:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          sudo apt-get update
          sudo apt-get install -y chromium-browser
          if [ ! -f /usr/bin/google-chrome ]; then
            sudo ln -s /usr/bin/chromium-browser /usr/bin/google-chrome
          fi

      - name: Run bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: |
          python send_image.py
