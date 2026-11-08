# ==================================================
# ЗАДАЧА 1. Вторая по величине зарплата (SQL)
# ==================================================

# Есть таблица:

# CREATE TABLE employees (
#     id     INT PRIMARY KEY,
#     name   TEXT,
#     salary INT
# );

# Напишите запрос, который возвращает вторую по величине зарплату.
# Если такой зарплаты нет, запрос должен вернуть NULL, а не пустой результат.

# Пример данных:

#  id | name | salary
# ----+------+-------
#   1 | Аня  |  300
#   2 | Боря |  200
#   3 | Вика |  300
#   4 | Гоша |  100

# Ожидаемый ответ: 200

import sqlite3


def make_db(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            salary INTEGER
        )
    """)
    conn.executemany(
        "INSERT INTO employees (id, name, salary) VALUES (?, ?, ?)", rows
    )
    conn.commit()
    return conn


def second_highest_salary(conn):
    row = conn.execute("""
        SELECT MAX(salary)
        FROM employees
        WHERE salary < (SELECT MAX(salary) FROM employees)
    """).fetchone()
    return row[0] if row else None

if __name__ == "__main__":
    print(second_highest_salary(make_db([
        (1, "Аня", 300), (2, "Боря", 200), (3, "Вика", 300), (4, "Гоша", 100),
    ])))  # 200

# SELECT MAX(salary) AS second_highest_salary
# FROM employees
# WHERE salary < (SELECT MAX(salary) FROM employees);