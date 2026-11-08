# ==================================================
# ЗАДАЧА 3. Топ пользователей по сумме заказов (Python + SQL)
# ==================================================

# Дан список заказов:

# orders = [
#     {"user_id": 1, "amount": 100, "status": "paid"},
#     {"user_id": 2, "amount": 300, "status": "paid"},
#     {"user_id": 1, "amount": 250, "status": "paid"},
#     {"user_id": 3, "amount": 500, "status": "cancelled"},
#     {"user_id": 2, "amount": 50,  "status": "paid"},
# ]

# Часть А.
# Напишите функцию top_users(orders, n), которая возвращает топ-N
# пользователей по сумме ОПЛАЧЕННЫХ заказов (status == "paid")
# в виде списка кортежей (user_id, total), отсортированного по убыванию суммы.

# Пример: top_users(orders, 2) -> [(1, 350), (2, 350)]

# Часть Б.
# Сохраните эти же данные в SQLite (sqlite3, база в памяти) и напишите
# функцию get_top_users(conn, status, limit), которая решает ту же задачу
# одним SQL-запросом. Статус и лимит передаются как параметры функции.

import sqlite3
from collections import defaultdict


# ЧАСТЬ А.

def top_users(orders, n):
    """Топ-N пользователей по сумме оплаченных заказов."""
    totals = defaultdict(int)

    for order in orders:
        if order.get("status") == "paid":
            totals[order["user_id"]] += order["amount"]

    sorted_users = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return sorted_users[:n]


# ЧАСТЬ Б.

def build_db(orders):
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE orders (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   INTEGER NOT NULL,
            amount    INTEGER NOT NULL,
            status    TEXT NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)",
        [(o["user_id"], o["amount"], o["status"]) for o in orders],
    )
    conn.commit()
    return conn


def get_top_users(conn, status, limit):
    cursor = conn.execute("""
        SELECT user_id, SUM(amount) AS total
        FROM orders
        WHERE status = ?
        GROUP BY user_id
        ORDER BY total DESC, user_id ASC
        LIMIT ?
    """, (status, limit))
    return cursor.fetchall()


if __name__ == "__main__":
    orders = [
        {"user_id": 1, "amount": 100, "status": "paid"},
        {"user_id": 2, "amount": 300, "status": "paid"},
        {"user_id": 1, "amount": 250, "status": "paid"},
        {"user_id": 3, "amount": 500, "status": "cancelled"},
        {"user_id": 2, "amount": 50, "status": "paid"},
    ]

    # ---------- Часть А ----------
    assert top_users(orders, 2) == [(1, 350), (2, 350)], \
        f"top_users(orders, 2): {top_users(orders, 2)}"

    assert top_users(orders, 1) == [(1, 350)], \
        f"top_users(orders, 1): {top_users(orders, 1)}"

    assert top_users(orders, 5) == [(1, 350), (2, 350)], \
        f"top_users(orders, 5): {top_users(orders, 5)}"

    assert top_users(orders, 0) == [], \
        f"top_users(orders, 0): {top_users(orders, 0)}"

    # ---------- Часть Б ----------
    conn = build_db(orders)

    assert get_top_users(conn, "paid", 2) == [(1, 350), (2, 350)], \
        f'get_top_users(conn, "paid", 2): {get_top_users(conn, "paid", 2)}'

    assert get_top_users(conn, "cancelled", 5) == [(3, 500)], \
        f'get_top_users(conn, "cancelled", 5): {get_top_users(conn, "cancelled", 5)}'

    assert get_top_users(conn, "paid", 10) == [(1, 350), (2, 350)], \
        f'get_top_users(conn, "paid", 10): {get_top_users(conn, "paid", 10)}'

    assert get_top_users(conn, "unknown", 5) == [], \
        f'get_top_users(conn, "unknown", 5): {get_top_users(conn, "unknown", 5)}'

    conn.close()

    # ---------- Сверка А и Б ----------
    conn = build_db(orders)
    a = top_users(orders, 2)
    b = get_top_users(conn, "paid", 2)
    assert a == b, f"Результаты не совпадают: A={a}, B={b}"
    conn.close()

    print("Все проверки пройдены ✅")
