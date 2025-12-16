import matplotlib.pyplot as plt
import os

import pandas as pd

from repository.user import get_connection
from service.user import get_active_users_by_role_from_logs
from utils.logger import log_action


def show(fig, filename):
    try:
        os.makedirs("graphs", exist_ok=True)
        fig.tight_layout()
        path = f"graphs/{filename}"
        fig.savefig(path)
        print(f"График сохранён: {path}")
        log_action(f"Сохрание графика: {path}")
        plt.show()
    except:
        print("Ошибка при отображении или сохранении графика")


def users_by_role():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()

        role_counts = df['role'].value_counts()

        fig = plt.figure()
        role_counts.plot(kind='bar')
        plt.title("Распределение пользователей по ролям")
        plt.xlabel("Роль")
        plt.ylabel("Количество")

        show(fig, "users_by_role.png")
    except:
        print("Ошибка при отрисковке графика")

def registrations_by_date():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()

        df['registered_at'] = df['registered_at'].astype(str)
        date_counts = df['registered_at'].value_counts().sort_index()

        fig = plt.figure()
        date_counts.plot(kind='line', marker='o')
        plt.title("Частота регистраций по датам")
        plt.xlabel("Дата")
        plt.ylabel("Количество регистраций")

        show(fig, "registrations_by_date.png")
    except:
        print("Ошибка при отрисковке графика")

def active_users_by_role():
    try:
        role = input("Введите роль: ").strip()

        data = get_active_users_by_role_from_logs(role)

        if not data:
            print("Нет данных для выбранной роли.")
            return

        dates = sorted(data.keys())
        counts = [data[d] for d in dates]

        fig = plt.figure(figsize=(10, 6))
        plt.plot(dates, counts, marker='o')

        plt.title(f"Активные пользователи по дням (роль: {role})")
        plt.xlabel("Дата")
        plt.ylabel("Количество активных пользователей")
        plt.xticks(rotation=45, ha='right')

        show(fig, f"active_users_{role}.png")
    except:
        print("Ошибка при отрисковке графика")
