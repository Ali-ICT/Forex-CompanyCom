from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
from datetime import datetime

TOKEN = "8633209473:AAFIhyWX1RzBjl7XrJAVFFOPTrV7LeXAEMg"
BASE_URL = "https://ictfx.pythonanywhere.com"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    parts = [p.strip() for p in msg.split("|")]

    if msg.lower() == "delete all":
        r = requests.post(f"{BASE_URL}/clear-signals")
        await update.message.reply_text(r.json()["status"])
        return

    if len(parts) == 2 and parts[1].lower() == "delete":
        signal_id = parts[0]
        signals = requests.get(f"{BASE_URL}/signals").json()
        signals = [s for s in signals if s["id"] != signal_id]
        requests.post(f"{BASE_URL}/clear-signals")
        for s in signals:
            requests.post(f"{BASE_URL}/add-signal", json=s)
        await update.message.reply_text(f"✅ Signal {signal_id} deleted")
        return

    if len(parts) < 7:
        await update.message.reply_text("❌ Incorrect format! Use ID|Type|Pair|Entry|SL|Targets|Status")
        return

    signal = {
        "id": parts[0],
        "type": parts[1],
        "pair": parts[2],
        "entry": parts[3],
        "sl": parts[4],
        "targets": parts[5].split(),
        "active": "🟢" in parts[6],
        "pips": 0,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    r = requests.post(f"{BASE_URL}/add-signal", json=signal)
    await update.message.reply_text(r.json()["status"])


def run_bot():
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))
    bot.run_polling()


if __name__ == "__main__":
    run_bot()