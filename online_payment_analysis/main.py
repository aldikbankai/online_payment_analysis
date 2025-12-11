"""Басты файл — транзакция енгізу, сақтау және анализ жасау"""
from models.db import Database
from analysis.analytics import TotalVolumeAnalyzer, FraudDetectorAnalyzer
from models.models import Transaction
from datetime import datetime
import re
from logs.logger_config import logger

logger.info("Жүйе іске қосылды.")



def parse_transaction_line(line: str):
    """
    Лексикалық және синтаксистік талдау.
    Формат: amount currency payer payee
    Мысалы: 50000 KZT Aigerim Market
    """
    pattern = r"^([0-9]+(\.[0-9]{1,2})?)\s+([A-Z]{3})\s+([A-Za-z]+)\s+([A-Za-z]+)$"
    match = re.match(pattern, line)
    if not match:
        return None

    amount = float(match.group(1))
    currency = match.group(3)
    payer = match.group(4)
    payee = match.group(5)

    return amount, currency, payer, payee


def run_manual_input():
    print("Онлайн төлемдерді енгізу жүйесіне қош келдіңіз!")
    print("0 деп жазсаңыз — тоқтайды\n")

    transactions = []
    currencies = ["KZT", "USD", "EUR", "RUB", "GBP", "JPY"]

    while True:
        line = input("Транзакция енгізіңіз (Сома Валюта Пайер Пайи): ").strip()

        if line == "0":
            print("Енгізу аяқталды.\n")
            break

        parsed = parse_transaction_line(line)
        if not parsed:
            print(" Қате формат! Мысалы: 50000 KZT Aigerim Market\n")
            continue

        amount, currency, payer, payee = parsed

        if amount <= 0:
            print(" Сома 0 немесе теріс болмауы керек!\n")
            continue

        if currency not in currencies:
            print(" Валюта дұрыс емес!\n")
            continue

        if not payer.isalpha() or not payee.isalpha():
            print(" Аты-жөн тек әріптер!\n")
            continue

        tx = Transaction(amount, currency, payer, payee, datetime.now())
        transactions.append(tx)
        print(" Транзакция енгізілді!\n")

    # Базаға жазу
    with Database("payments.db") as db:
        db.create_tables()
        for tx in transactions:
            db.insert_transaction(tx)
        stored = db.fetch_all_transactions()

    # Анализ
    total_analyzer = TotalVolumeAnalyzer()
    fraud_analyzer = FraudDetectorAnalyzer()

    totals = total_analyzer.analyze(stored)
    suspects = fraud_analyzer.analyze(stored)

    print("=== Жалпы көлем (валюта бойынша) ===")
    for c, t in totals.items():
        print(f"{c}: {t:.2f}")

    print(f"\n=== Күдікті транзакциялар ({len(suspects)}) ===")
    for s in suspects[:10]:
        print(s)


if __name__ == "__main__":
    run_manual_input()
