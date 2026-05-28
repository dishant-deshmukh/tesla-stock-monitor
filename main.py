from playwright.sync_api import sync_playwright
import requests
import time
import os

BOT_TOKEN = os.getenv("8904730768:AAGPU7LbFiZbSCh0ns6Kfajh4ij1VBdpKG4")
CHAT_ID = os.getenv("1424140602")

URL = "https://shop.tesla.com/en_au/product/model-yl-all-weather-interior-liners"

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

def check_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, timeout=60000)

        page.wait_for_timeout(5000)

        content = page.content().lower()

        browser.close()

        print(content)

        if "out of stock" in content:
            return False

        if "add to cart" in content:
            return True

        return False

already_notified = False

while True:
    try:
        available = check_stock()

        if available and not already_notified:

            send_telegram(
                "Tesla Model YL Floor Mats are AVAILABLE!\n\n"
                + URL
            )

            already_notified = True

        elif not available:
            already_notified = False

    except Exception as e:
        print(e)

    time.sleep(300)
