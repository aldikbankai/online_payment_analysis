import sqlite3
from logs.logger_config import logger

def insert_transaction(self, tx):
    if not self.conn:
        self.connect()

    logger.info(f"Транзакция енгізілуде: {tx}")

    try:
        self.conn.execute(
            """
            INSERT INTO transactions (amount, currency, payer, payee, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (tx.amount, tx.currency, tx.payer, tx.payee, tx.timestamp),
        )
        self.conn.commit()
        logger.info("Транзакция базаға сәтті енгізілді.")
    except Exception as e:
        logger.error(f"Транзакция енгізу кезінде қате: {e}")
        raise


DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    payer TEXT NOT NULL,
    payee TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
"""


class Database:
    """Онлайн төлемдерді сақтайтын деректер базасы"""

    def __init__(self, db_name="payments.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self):
        if not self.conn:
            self.connect()
        self.conn.executescript(DB_SCHEMA)
        self.conn.commit()

    def insert_transaction(self, tx):
        if not self.conn:
            self.connect()
        self.conn.execute(
            """
            INSERT INTO transactions (amount, currency, payer, payee, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (tx.amount, tx.currency, tx.payer, tx.payee, tx.timestamp),
        )
        self.conn.commit()

    def fetch_all_transactions(self):
        if not self.conn:
            self.connect()

        rows = self.conn.execute("SELECT * FROM transactions").fetchall()

        return [
            {
                "id": r[0],
                "amount": r[1],
                "currency": r[2],
                "payer": r[3],
                "payee": r[4],
                "timestamp": r[5],
            }
            for r in rows
        ]

    # Context Manager
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
