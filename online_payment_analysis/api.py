# api.py — Онлайн төлемдерге арналған REST API
from flask import Flask, request, jsonify
from models.db import Database
from models.models import Transaction
from analysis.analytics import FraudDetectorAnalyzer, TotalVolumeAnalyzer
from datetime import datetime

app = Flask(__name__)

# Валюта тізімі
VALID_CURRENCIES = ["KZT", "USD", "EUR", "RUB", "GBP", "JPY"]

# Fraud тексеру шектері
THRESHOLDS = {
    "KZT": 500000,
    "USD": 1000,
    "EUR": 900,
    "RUB": 100000,
    "GBP": 800,
    "JPY": 150000
}

# ---------------------------- API ROOT ----------------------------
@app.route("/")
def home():
    return {
        "status": "OK",
        "message": "Online Payment API is running",
        "routes": [
            "/add  (POST)",
            "/transactions  (GET)",
            "/stats  (GET)",
            "/suspects  (GET)"
        ]
    }


# ---------------------------- API ҚАТЕ ӨҢДЕУ ----------------------------
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 400


# ---------------------------- 1) Транзакция қосу ----------------------------
@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json

    # Поле тексеру
    for field in ["amount", "currency", "payer", "payee"]:
        if field not in data:
            return jsonify({"error": f"{field} енгізілмеген"}), 400

    amount = float(data["amount"])
    currency = data["currency"].upper()
    payer = data["payer"]
    payee = data["payee"]

    # Валидация
    if amount <= 0:
        return jsonify({"error": "Сома 0 немесе теріс болмауы керек"}), 400

    if currency not in VALID_CURRENCIES:
        return jsonify({"error": "Мұндай валюта қолжетімсіз"}), 400

    if not payer.isalpha() or not payee.isalpha():
        return jsonify({"error": "payer/payee тек әріп болуы керек"}), 400

    # Транзакция объект
    tx = Transaction(amount, currency, payer, payee, datetime.now())

    # БД-ға жазу
    with Database("payments.db") as db:
        db.create_tables()
        db.insert_transaction(tx)

    return jsonify({"status": "OK", "message": "Транзакция сақталды"})


# ---------------------------- 2) Барлық транзакция ----------------------------
@app.route("/transactions", methods=["GET"])
def get_all():
    with Database("payments.db") as db:
        rows = db.fetch_all_transactions()
    return jsonify(rows)


# ---------------------------- 3) Жалпы статистика ----------------------------
@app.route("/stats", methods=["GET"])
def stats():
    with Database("payments.db") as db:
        rows = db.fetch_all_transactions()

    analyzer = TotalVolumeAnalyzer()
    totals = analyzer.analyze(rows)
    return jsonify(totals)


# ---------------------------- 4) Күдікті транзакциялар ----------------------------
@app.route("/suspects", methods=["GET"])
def suspects():
    with Database("payments.db") as db:
        rows = db.fetch_all_transactions()

    analyzer = FraudDetectorAnalyzer(thresholds=THRESHOLDS)
    items = analyzer.analyze(rows)

    return jsonify(items)


# ---------------------------- API іске қосу ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
