import requests
import time
from datetime import datetime
import pytz
from concurrent.futures import ThreadPoolExecutor

CHECK_PHRASE = "<span>This beta is full.</span>"

# Telegram
TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHATID"
TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ESP32 Web Alarm When Using Alarm micro controller
ESP_ALARM_URL = "http://localhost/alarm"
ESP_STOP_URL  = "http://localhost/stop"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36"
}

jakarta = pytz.timezone("Asia/Jakarta")
def now():
    return datetime.now(jakarta).strftime("%d-%m-%Y %H:%M:%S")

def notify_telegram(msg):
    requests.post(TG_API, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

notified_status = {}

def load_urls():
    with open("url.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_url(url):
    global notified_status
    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
        is_full = CHECK_PHRASE in html

        if is_full:
            print(f"[{now()}] FULL → {url}")
            if notified_status.get(url) != "FULL":
                requests.get(ESP_STOP_URL)  # matikan alarm
                notify_telegram(f"🔴 FULL kembali → {url}")
                notified_status[url] = "FULL"

        else:
            print(f"[{now()}] AVAILABLE → {url}")
            if notified_status.get(url) != "AVAILABLE":
                notify_telegram(f"🟢 AVAILABLE! ({now()})\n{url}")
                requests.get(ESP_ALARM_URL)  # bunyikan alarm
                notified_status[url] = "AVAILABLE"

            # tetap bunyikan selama masih AVAILABLE
            requests.get(ESP_ALARM_URL)

    except Exception as e:
        print(f"[{now()}] ERROR → {url} → {e}")

MAX_THREADS = 2

while True:
    urls = load_urls()
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(check_url, urls)
    time.sleep(10)

