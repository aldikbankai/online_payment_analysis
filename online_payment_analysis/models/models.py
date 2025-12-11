"""Модельдер модулі: Transaction (транзакция), User (пайдаланушы)"""

from datetime import datetime
from typing import Optional
from logs.logger_config import logger


class Transaction:
    """
    Төлем транзакциясын сипаттайтын класс.

    Атрибуттар:
        id (int): бірегей идентификатор
        _amount (float): жеке (инкапсуляцияланған) сома
        currency (str): валюта
        payer (str): төлеуші
        payee (str): алушы
        timestamp (datetime): уақыт
    """

    def __init__(
        self,
        amount: float,
        currency: str,
        payer: str,
        payee: str,
        timestamp: Optional[datetime] = None,
        transaction_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ):
        self._id = transaction_id
        self.amount = amount  # setter жұмыс істейді
        self.currency = currency
        self.payer = payer
        self.payee = payee
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata = metadata or {}

        logger.info(f"Жаңа транзакция құрылды: {self}")

    # ---------- Арнайы әдістер ----------
    def __repr__(self):
        return (
            f"Transaction(id={self._id}, amount={self._amount}, currency={self.currency}, "
            f"payer={self.payer}, payee={self.payee}, time={self.timestamp})"
        )

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented
        return self._amount == other._amount and self.currency == other.currency

    # ---------- Инкапсуляция ----------
    @property
    def amount(self):
        """Соманы оқу"""
        return self._amount

    @amount.setter
    def amount(self, value: float):
        """Соманы орнату — тек оң сандар"""
        if value <= 0:
            logger.error(f"Теріс немесе 0 сома енгізілді: {value}")
            raise ValueError("Сома теріс немесе 0 болмауы керек!")
        self._amount = float(value)
        logger.info(f"Сома орнатылды: {self._amount}")

    @classmethod
    def from_dict(cls, data: dict):
        """Сөздіктен Transaction жасау"""
        return cls(
            amount=data["amount"],
            currency=data["currency"],
            payer=data["payer"],
            payee=data["payee"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            transaction_id=data.get("id"),
        )


class User:
    """Пайдаланушы класы"""

    def __init__(self, user_id: str, email: Optional[str] = None):
        self._user_id = user_id
        self._email = email

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: str):
        if value and "@" not in value:
            logger.error(f"Қате email: {value}")
            raise ValueError("Email дұрыс емес!")
        self._email = value
        logger.info(f"Email орнатылды: {value}")
