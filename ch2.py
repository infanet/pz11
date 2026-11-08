# ==================================================
# ЗАДАЧА 2. Клиенты без заказов (SQL)
# ==================================================

# Есть две таблицы:

# CREATE TABLE customers (
#     id   INT PRIMARY KEY,
#     name TEXT
# );

# CREATE TABLE orders (
#     id          INT PRIMARY KEY,
#     customer_id INT,
#     amount      INT
# );

# Выведите имена клиентов, которые ни разу не делали заказ.

# Пример данных:

# customers:
#  id | name
# ----+------
#   1 | Аня
#   2 | Боря
#   3 | Вика

# orders:
#  id | customer_id | amount
# ----+-------------+-------
#   1 |      1      |  500
#   2 |      1      |  300
#   3 |      3      |  100

# Ожидаемый ответ: Боря

import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount INTEGER
    );

    INSERT INTO customers VALUES (1, 'Аня'), (2, 'Боря'), (3, 'Вика');
    INSERT INTO orders VALUES (1, 1, 500), (2, 1, 300), (3, 3, 100);
""")

cursor = conn.execute("""
    SELECT c.name
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.id
    WHERE o.id IS NULL
""")

if __name__ == "__main__":
    for (name,) in cursor.fetchall():
        print(name)


# SELECT c.name
# FROM customers c
# LEFT JOIN orders o ON o.customer_id = c.id
# WHERE o.id IS NULL;