# tests/test_transaction.py
import pytest
from models.models import Transaction

def test_transaction_positive_amount():
    tx = Transaction(1000, "KZT", "Aigerim", "Market")
    assert tx.amount == 1000

def test_transaction_negative_amount():
    with pytest.raises(ValueError):
        Transaction(-500, "KZT", "Aigerim", "Market")

def test_transaction_zero_amount():
    with pytest.raises(ValueError):
        Transaction(0, "KZT", "Aigerim", "Market")

def test_transaction_repr():
    tx = Transaction(1500, "KZT", "Aigerim", "Market")
    text = repr(tx)
    assert "Transaction" in text
    assert "amount" in text