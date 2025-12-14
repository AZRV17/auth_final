from collections import Counter

import matplotlib.pyplot as plt
import os

from service.user import get_active_users_by_role_from_logs
from utils.logger import log_action


def show(fig, filename):
    os.makedirs("graphs", exist_ok=True)
    fig.tight_layout()
    path = f"graphs/{filename}"
    fig.savefig(path)
    print(f"График сохранён: {path}")
    log_action(f"Сохрание графика: {path}")
    plt.show()


def users_by_role(df):
    role_counts = df['Роль'].value_counts()

    fig = plt.figure()
    role_counts.plot(kind='bar')
    plt.title("Распределение пользователей по ролям")
    plt.xlabel("Роль")
    plt.ylabel("Количество")

    show(fig, "users_by_role.png")

def registrations_by_date(df):
    df['Дата регистрации'] = df['Дата регистрации'].astype(str)
    date_counts = df['Дата регистрации'].value_counts().sort_index()

    fig = plt.figure()
    date_counts.plot(kind='line', marker='o')
    plt.title("Частота регистраций по датам")
    plt.xlabel("Дата")
    plt.ylabel("Количество регистраций")

    show(fig, "registrations_by_date.png")

def active_users_by_role():
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
