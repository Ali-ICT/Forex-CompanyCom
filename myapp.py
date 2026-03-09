from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = "signals.json"

# تحميل البيانات
try:
    with open(DATA_FILE,"r") as f:
        signals = json.load(f)
except:
    signals = []

def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(signals,f)

@app.route("/signals")
def get_signals():
    active = [s for s in signals if s["active"]]
    closed = [s for s in signals if not s["active"]]
    ordered = active[::-1] + closed[::-1]
    return jsonify(ordered)

@app.route("/stats")
def stats():
    total = len(signals)
    wins = len([s for s in signals if s.get("result")=="win"])
    losses = len([s for s in signals if s.get("result")=="loss"])
    winrate = round((wins/total)*100,2) if total>0 else 0
    pips = sum([s.get("pips",0) for s in signals])
    return jsonify({
        "total":total,
        "wins":wins,
        "losses":losses,
        "winrate":winrate,
        "pips":pips
    })

@app.route("/add-signal",methods=["POST"])
def add_signal():
    data = request.json
    signal_id = data["id"]
    existing = next((s for s in signals if s["id"]==signal_id),None)

    if existing:
        existing.update(data)
        save_data()
        return jsonify({"status":"updated"})
    else:
        data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        signals.append(data)
        save_data()
        return jsonify({"status":"added"})

@app.route("/clear-signals", methods=["POST"])
def clear_signals():
    global signals
    signals = []
    save_data()
    return jsonify({"status":"all deleted"})


TOKEN = "8633209473:AAFIhyWX1RzBjl7XrJAVFFOPTrV7LeXAEMg"

async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()

    global signals

    # ---- حذف كل التوصيات ----
    if msg.lower() == "delete all":
        signals = []
        save_data()
        await update.message.reply_text("✅ All signals deleted successfully")
        return

    # ---- حذف توصية فردية ----
    parts = [p.strip() for p in msg.split("|")]
    if len(parts) == 2 and parts[1].lower() == "delete":
        signals = [s for s in signals if s["id"] != parts[0]]
        save_data()
        await update.message.reply_text(f"✅ Signal {parts[0]} deleted")
        return

    # ---- إضافة / تعديل توصية ----
    if len(parts)<2:
        await update.message.reply_text("❌ Incorrect format! Use ID|Type|Pair|Entry|SL|Targets|Status")
        return

    signal = {
        "id":parts[0],
        "type":parts[1],
        "pair":parts[2],
        "entry":parts[3],
        "sl":parts[4],
        "targets":parts[5].split(),
        "active":"🟢" in parts[6],
        "pips":0
    }

    r = requests.post("http://127.0.0.1:5000/add-signal",json=signal)
    await update.message.reply_text(r.json()["status"])


def run_bot():
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND),handle)
    )
    bot.run_polling()


if __name__=="__main__":
    threading.Thread(
        target=lambda:app.run(host="0.0.0.0",port=5000)
    ).start()
    run_bot()