# tests/test_fraud.py
from analysis.analytics import FraudDetectorAnalyzer

def test_fraud_detection():
    analyzer = FraudDetectorAnalyzer(
        thresholds={"KZT": 500000}
    )

    transactions = [
        {"amount": 200000, "currency": "KZT"},
        {"amount": 700000, "currency": "KZT"},  # күдікті
    ]

    suspects = analyzer.analyze(transactions)

    assert len(suspects) == 1
    assert suspects[0]["amount"] == 700000
