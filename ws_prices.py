# import json
# import websocket
# import threading
# import random
# import string
# import time
# from flask import Flask, jsonify
# from flask_cors import CORS

# # ---------------------------
# # تخزين الأسعار
# # ---------------------------

# price_data = {}
# previous_prices = {}

# # ---------------------------
# # Flask API
# # ---------------------------

# app = Flask(__name__)
# CORS(app)

# @app.route("/prices")
# def get_prices():

#     data = {}

#     for symbol, price in price_data.items():

#         prev = previous_prices.get(symbol, price)

#         data[symbol] = {
#             "price": price,
#             "change": round(price - prev, 5),
#             "high": price,
#             "low": round(price - 0.08, 5)
#         }

#     return jsonify(data)


# def run_flask():

#     print("🌐 Flask API running on http://127.0.0.1:5002/prices")

#     app.run(
#         host="0.0.0.0",
#         port=5002,
#         debug=False,
#         use_reloader=False
#     )


# # ---------------------------
# # أدوات WebSocket
# # ---------------------------

# def random_session():
#     return "qs_" + "".join(random.choice(string.ascii_lowercase) for _ in range(12))


# def send(ws, message):
#     ws.send("~m~" + str(len(message)) + "~m~" + message)


# def create_message(func, args):
#     return json.dumps({"m": func, "p": args})


# # ---------------------------
# # استقبال الأسعار
# # ---------------------------

# def on_message(ws, message):

#     global price_data, previous_prices

#     try:

#         if "lp" in message:

#             raw = message.split("~")[-1]

#             data = json.loads(raw)

#             if isinstance(data, dict) and "p" in data:

#                 items = data["p"]

#                 for item in items:

#                     if isinstance(item, dict):

#                         symbol = item.get("n")
#                         values = item.get("v")

#                         if symbol and values:

#                             price = values.get("lp")

#                             if isinstance(price, (int, float)):

#                                 clean_symbol = symbol.replace("OANDA:", "")

#                                 previous_prices[clean_symbol] = price_data.get(clean_symbol, price)

#                                 price_data[clean_symbol] = price

#                                 print(f"📈 {clean_symbol} = {price}")

#     except Exception as e:

#         print("❌ WebSocket Error:", e)


# # ---------------------------
# # عند الاتصال
# # ---------------------------

# def on_open(ws):

#     try:

#         session = random_session()

#         send(ws, create_message("quote_create_session", [session]))

#         send(ws, create_message("quote_set_fields", [session, "lp"]))

#         symbols = [
#             "OANDA:XAUUSD",
#             "OANDA:EURUSD",
#             "OANDA:GBPUSD",
#             "OANDA:USDJPY",
#             "OANDA:USDCHF"
#         ]

#         for s in symbols:
#             send(ws, create_message("quote_add_symbols", [session, s]))

#         print("📡 Connected to TradingView WebSocket")

#     except Exception as e:

#         print("❌ WebSocket Open Error:", e)


# # ---------------------------
# # تشغيل WebSocket
# # ---------------------------

# def start_ws():

#     while True:

#         try:

#             ws = websocket.WebSocketApp(
#                 "wss://data.tradingview.com/socket.io/websocket",
#                 on_message=on_message,
#                 on_open=on_open
#             )

#             ws.run_forever()

#         except Exception as e:

#             print("🔄 Reconnecting:", e)

#             time.sleep(5)


# # ---------------------------
# # تشغيل السيرفر
# # ---------------------------

# threading.Thread(target=run_flask, daemon=True).start()

# threading.Thread(target=start_ws, daemon=True).start()

# # إبقاء البرنامج شغال
# while True:
#     time.sleep(1)