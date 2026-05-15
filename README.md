# Data Engineering Test Task

# Опис проєкту

В рамках тестового завдання реалізував простий Data Engineering pipeline для обробки та аналітики даних продажів.

Проєкт включає:

- завантаження та підготовку даних
- очищення та перевірки якості даних
- побудову підготовленого аналітичного датасету
- SQL DDL та аналітичні SQL-запити
- приклад chunk-based processing для роботи з великими обсягами даних
- реалізацію простого pipeline orchestration

---

# Структура проєкту

```text
data-engineering-test-task/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── quality_checks.py
│   ├── analytics.py
│   └── chunk_processing.py
│
├── sql/
│   ├── ddl.sql
│   └── analytical_queries.sql
│
├── docs/
│
├── main.py
├── requirements.txt
└── README.md

Було використано 4 вхідні таблиці

customers
products
purchases
invoice_items

Під час обробки було реалізовано

приведення типів даних
конвертацію дат у datetime
пошук дублювання
очищення дублікатів
об’єднання таблиць у фінальний аналітичний датасет

Було виявлено
дублікати

Було реалізовано перевірки

NULL values
exact duplicates
аномалії quantity
аномалії price
перевірка line_total consistency
referential integrity checks

Також було перевірено:
наявність customer_id у customers
наявність product_id у products

Було реалізовано

Top-N товарів по revenue
monthly revenue
category revenue share
cumulative monthly revenue
month-over-month growth
Для аналітики було підготовлено єдиний sales dataset після очищення та об’єднання таблиць.

Результати аналітики зберігаються у:

top_products.csv
monthly_revenue.csv
category_revenue_share.csv
Робота з великими обсягами даних

Для моделювання обробки великих обсягів даних реалізовав chunk-based processing через pandas chunksize.

Дані обробляв частинами без необхідності завантаження всього файлу в RAM.

Під час chunk processing:

дані читаються частинами
виконуються cleaning та deduplication
виконуються chunk-level aggregation
результати об’єднуються у фінальний aggregate dataset

SQL
Реалізував:

DDL для target tables
Top-N query
Retention query
Anti-join query
cumulative metrics через window functions
Pipeline

Pipeline реалізовано через main.py

Основні етапи:

Data transformation
Data quality checks
Analytics

Ідемпотентність

Pipeline підтримує повторний запуск без дублювання результатів.
видаляються дублі
processed файли перезаписуються при кожному запуску

Запуск pipeline
python main.py
