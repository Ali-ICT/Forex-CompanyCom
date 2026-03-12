from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes
import json
from datetime import datetime
import os

# ---------------- Configuration ----------------
BOT_TOKEN = "8633209473:AAFIhyWX1RzBjl7XrJAVFFOPTrV7LeXAEMg"
DATA_FILE = "signals.json"

# ---------------- Flask setup ----------------
app = Flask(__name__)
CORS(app)

# تحميل بيانات التوصيات إذا موجودة
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        signals = json.load(f)
else:
    signals = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(signals, f)

# ---------------- Routes ----------------
@app.route("/signals")
def get_signals():
    return jsonify(signals)

@app.route("/stats")
def stats():
    total = len(signals)
    wins = len([s for s in signals if s.get("result")=="win"])
    losses = len([s for s in signals if s.get("result")=="loss"])
    winrate = round((wins/total)*100,2) if total>0 else 0
    pips = sum([s.get("pips",0) for s in signals])
    return jsonify({
        "total": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
        "pips": pips
    })

# ---------------- Telegram Webhook ----------------
bot = Bot(token=BOT_TOKEN)
app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    """ استقبال رسائل البوت عن طريق Webhook """
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        msg = update.message.text.strip()

        # تقسيم الرسالة | ID|Type|Pair|Entry|SL|Targets|Status
        parts = [p.strip() for p in msg.split("|")]
        if len(parts) >= 7:
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
            # تحديث إذا موجود
            existing = next((s for s in signals if s["id"]==signal["id"]), None)
            if existing:
                existing.update(signal)
            else:
                signals.append(signal)
            save_data()
        return "ok"
    except Exception as e:
        return str(e)

# ---------------- Clear signals (اختياري) ----------------
@app.route("/clear-signals", methods=["POST"])
def clear_signals():
    global signals
    signals = []
    save_data()
    return jsonify({"status": "all deleted"})