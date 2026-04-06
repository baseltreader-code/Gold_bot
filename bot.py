import time
import requests
import numpy as np
from datetime import datetime

# --- إعدادات باسل الخاصة ---
TOKEN = "7969317588:AAGoV9V10LAtZlS_8-O7N5yFm_46A6O0S0M"
CHAT_ID = "6197171454"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.get(url, params=params, timeout=10)
    except: pass

def get_gold_price():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return float(data['chart']['result'][0]['meta']['regularMarketPrice'])
    except: return None

prices = []
last_sig = None

print("🚀 انطلاق نظام باسل V19...")
send_telegram("✅ **تم تفعيل نظام باسل V19**\nالرصد السحابي بدأ الآن...")

while True:
    price = get_gold_price()
    if price:
        prices.append(price)
        if len(prices) > 30: prices.pop(0)
        if len(prices) >= 10:
            low, high = min(prices), max(prices)
            t_val = (price - low) / (high - low + 1e-9) * 100
            vel = prices[-1] - prices[-2]
            if t_val < 20 and vel > 0.05 and last_sig != "BUY":
                send_telegram(f"🟢 **إشارة شراء ذهب**\n📍 السعر: {price:.2f}")
                last_sig = "BUY"
            elif t_val > 80 and vel < -0.05 and last_sig != "SELL":
                send_telegram(f"🔴 **إشارة بيع ذهب**\n📍 السعر: {price:.2f}")
                last_sig = "SELL"
    time.sleep(60)
