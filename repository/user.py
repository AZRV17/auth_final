import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from utils.password_generator import generate_password

DB_PATH = "database/users.db"
ROLES = ['Администратор', 'Клиент', 'Менеджер', 'Оператор']


class User:
    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._create_table()
        self._init_data()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                login TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                registered_at TEXT,
                role TEXT,
                is_active INTEGER
            )
        """)
        self.conn.commit()

    def _init_data(self):
        count = self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

        if count > 0:
            return

        np.random.seed(1)
        df = pd.DataFrame({
            'id': range(1, 21),
            'first_name': np.random.choice(
                ['Иван', 'Александр', 'Петр', 'Дмитрий', 'Даниил'], 20),
            'last_name': np.random.choice(
                ['Иванов', 'Александров', 'Петров', 'Дмитриев', 'Данилов'], 20),
            'login': [f'user{i}' for i in range(1, 21)],
            'email': [f'newuser{i}@gmail.com' for i in range(1, 21)],
            'password': [generate_password() for _ in range(20)],
            'registered_at': datetime.now().strftime('%Y-%m-%d'),
            'role': np.random.choice(ROLES, 20),
            'is_active': np.random.choice([0, 1], 20)
        })

        df.to_sql("users", self.conn, if_exists="append", index=False)

    def get_all_users(self):
        return pd.read_sql("SELECT * FROM users", self.conn)

    def update_users(self, df: pd.DataFrame):
        df = df.rename(columns={
            'ID': 'id',
            'Имя': 'first_name',
            'Фамилия': 'last_name',
            'Логин': 'login',
            'Email': 'email',
            'Пароль': 'password',
            'Дата регистрации': 'registered_at',
            'Роль': 'role',
            'Активен': 'is_active'
        })

        df['is_active'] = df['is_active'].astype(int)

        self.conn.execute("DELETE FROM users")
        df.to_sql("users", self.conn, if_exists="append", index=False)
        self.conn.commit()

def get_connection():
    return sqlite3.connect(DB_PATH)
