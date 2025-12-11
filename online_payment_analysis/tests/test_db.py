# tests/test_db.py
import os
from models.db import Database
from models.models import Transaction
from datetime import datetime

TEST_DB = "test_payments.db"

def setup_module(module):
    # тест үшін бөлек база
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_insert_and_fetch():
    tx = Transaction(10000, "KZT", "Aigerim", "Market", datetime.now())

    with Database(TEST_DB) as db:
        db.create_tables()
        db.insert_transaction(tx)
        rows = db.fetch_all_transactions()

    assert len(rows) == 1
    assert rows[0]["amount"] == 10000
    assert rows[0]["currency"] == "KZT"
