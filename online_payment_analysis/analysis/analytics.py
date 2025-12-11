"""Аналитикалық модуль — мұрагерлік және полиморфизм мысалы"""
from abc import ABC, abstractmethod
from logs.logger_config import logger

def analyze(self, transactions):
    suspects = []
    for tx in transactions:
        amount = tx["amount"]
        currency = tx["currency"]

        limit = self.thresholds.get(currency, self.thresholds["KZT"])

        if amount >= limit:
            logger.warning(f"Күдікті транзакция анықталды: {tx}")
            suspects.append(tx)

    logger.info(f"Барлығы {len(suspects)} күдікті табылды.")
    return suspects



class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, transactions):
        pass


class TotalVolumeAnalyzer(BaseAnalyzer):
    """Жалпы соманы есептеу"""

    def analyze(self, transactions):
        totals = {}
        for tx in transactions:
            currency = tx["currency"]
            amount = tx["amount"]
            totals.setdefault(currency, 0)
            totals[currency] += amount
        return totals


class FraudDetectorAnalyzer(BaseAnalyzer):
    """Әр валютаға арналған күдікті лимит бойынша анықтайды"""

    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            "KZT": 500000,
            "USD": 1000,
            "EUR": 900,
            "RUB": 100000,
            "GBP": 800,
            "JPY": 150000,
            "CNY": 7000,
        }

    def analyze(self, transactions):
        suspects = []
        for tx in transactions:
            amount = tx["amount"]
            currency = tx["currency"]
            limit = self.thresholds.get(currency, self.thresholds["KZT"])
            if amount >= limit:
                suspects.append(tx)
        return suspects
