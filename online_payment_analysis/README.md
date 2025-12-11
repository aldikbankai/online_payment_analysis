#Онлайн төлемдерді бақылау және талдау жүйесі

##Online Payment Analysis Platform
Бұл жоба онлайн төлемдерді сақтау, талдау, күдікті транзакцияларды (fraud) анықтау және API арқылы жұмыс істеу үшін жазылған оқу жобасы.
Python, OOP, SQLite, Flask, логтау, модульдік тесттер, Git және CI/CD толық қолданылған.

Мүмкіндіктері
1) Транзакцияларды енгізу
– қолмен (main.py)
– REST API арқылы (api.py)

2) SQLite базаға сақтау
Database класы арқылы транзакциялар автоматты түрде базаға жазылады.

3) Аналитика
– Жалпы көлемді есептеу (TotalVolumeAnalyzer)
– Күдікті транзакцияларды анықтау (FraudDetectorAnalyzer)

4) Логтау
Барлық әрекет logs/app.log ішінде сақталады.

5) Unit тесттер (pytest)
– Транзакция моделі
– Fraud анализаторы
– Деректер базасы

6) Git тармақтары
main — тұрақты код
dev — жаңа мүмкіндіктер

7) CI/CD (GitHub Actions)
PR және push кезінде тесттер автоматты жүреді.


##Жоба құрылымы
online_payment_analysis/
│
├── analysis/
│   ├── analytics.py          # Аналитика (Fraud, Volume)
│
├── api/
│   └── api.py                # Flask REST API
│
├── logs/
│   ├── app.log               # Логтар
│   └── logger_config.py      # Лог баптауы
│
├── models/
│   ├── db.py                 # SQLite база
│   └── models.py             # Transaction, User
│
├── tests/
│   ├── test_transaction.py
│   ├── test_fraud.py
│   └── test_db.py
│
├── utils/
│   └── utils.py              # Тестке арналған генератор
│
├── main.py                   # Қолмен енгізу жүйесі
├── README.md
├── .gitignore
└── payments.db (git-те салынбайды)



##API қолдану

API серверді іске қосу:
python api/api.py

1) Транзакция қосу
POST /add
{
  "amount": 50000,
  "currency": "KZT",
  "payer": "Aigerim",
  "payee": "Market"
}

2) Барлық транзакциялар
GET /transactions

3) Жалпы статистика
GET /stats

4) Күдікті транзакциялар
GET /suspects

Тесттерді іске қосу
pytest -v

Тест модульдері:
test_transaction.py
test_fraud.py
test_db.py


##Пайдаланылған тақырыптар
Класс, инкапсуляция
@property, @setter
Арнайы әдістер (__repr__, __eq__)
Мұрагерлік және полиморфизм
SQLite database
Логтау (logging)
Flask API
Модульдік тест (pytest)
Git branch, PR, merge
CI/CD (GitHub Actions)