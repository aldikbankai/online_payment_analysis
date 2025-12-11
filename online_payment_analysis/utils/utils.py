"""Көмекші модуль — тестке арналған транзакция генераторы"""
import random
from datetime import datetime, timedelta
from models import Transaction


def generate_sample_transactions(n=50):
    currencies = ["KZT", "USD", "EUR"]
    payers = ["user1", "user2", "user3"]
    payees = ["shop1", "shop2", "shop3"]

    now = datetime.utcnow()
    data = []

    for _ in range(n):
        tx = Transaction(
            amount=round(random.uniform(10, 200000), 2),
            currency=random.choice(currencies),
            payer=random.choice(payers),
            payee=random.choice(payees),
            timestamp=now - timedelta(minutes=random.randint(1, 10000)),
        )
        data.append(tx)

    return data
