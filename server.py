# # server.py
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import json
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# DATA_FILE = "signals.json"

# # تحميل البيانات من JSON
# try:
#     with open(DATA_FILE, "r") as f:
#         signals = json.load(f)
# except:
#     signals = []

# def save_data():
#     with open(DATA_FILE, "w") as f:
#         json.dump(signals, f)

# @app.route("/signals")
# def get_signals():
#     active = [s for s in signals if s["active"]]
#     closed = [s for s in signals if not s["active"]]
#     return jsonify(active[::-1] + closed[::-1])

# @app.route("/stats")
# def stats():
#     total = len(signals)
#     wins = len([s for s in signals if s.get("result")=="win"])
#     losses = len([s for s in signals if s.get("result")=="loss"])
#     winrate = round((wins/total)*100,2) if total>0 else 0
#     pips = sum([s.get("pips",0) for s in signals])
#     return jsonify({
#         "total": total,
#         "wins": wins,
#         "losses": losses,
#         "winrate": winrate,
#         "pips": pips
#     })

# @app.route("/add-signal", methods=["POST"])
# def add_signal():
#     data = request.json
#     signal_id = data["id"]
#     existing = next((s for s in signals if s["id"]==signal_id), None)

#     if existing:
#         existing.update(data)
#         save_data()
#         return jsonify({"status":"updated"})
#     else:
#         data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
#         signals.append(data)
#         save_data()
#         return jsonify({"status":"added"})

# @app.route("/clear-signals", methods=["POST"])
# def clear_signals():
#     global signals
#     signals = []
#     save_data()
#     return jsonify({"status":"all deleted"})

# if __name__ == "__main__":
#     app.run()