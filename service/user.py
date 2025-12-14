from utils.logger import log_action
from utils.password_generator import generate_password
from collections import defaultdict
import re

import pandas as pd

LOG_FILE = "app.log"

def login(df):
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    user = df[(df['Логин'] == login) & (df['Пароль'] == password)]
    if not user.empty:
        df.loc[df['Логин'] == login, 'Активен'] = True
        role = user.iloc[0]['Роль']
        log_action(f"Успешный вход пользователя: {login}")
        log_action(f"LOGIN {login} role={role}")
        print(f"Вход выполнен: {login}")
    else:
        log_action(f"Неудачный вход пользователя: {login}")
        print("Неверный логин или пароль.")
    return df

def logout(df):
    login = input("Введите логин для выхода: ")
    user = df[df['Логин'] == login]
    if not user.empty:
        role = user.iloc[0]['Роль']
        df.loc[df['Логин'] == login, 'Активен'] = False
        print(f"Пользователь {login} вышел из системы.")
        log_action(f"Выход из системы: {login}")
        log_action(f"LOGOUT {login} role={role}")
    else:
        print("Логин не найден.")
    return df

def register(df):
    login = input("Введите логин: ")
    if login in df['Логин'].values:
        print("Такой логин уже существует.")
        return df

    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    role = input("Введите роль (по умолчанию Клиент): ") or "Клиент"

    while True:
        password = input("Введите новый пароль (a для генерации пароля): ").strip()
        if password == "a":
            password = generate_password()
        elif len(password) < 6:
            print("Пароль должен содрежать минимум 6 символов")
            continue
        break

    new_user = {
        'ID': df['ID'].max() + 1,
        'Имя': name,
        'Фамилия': surname,
        'Логин': login,
        'Пароль': password,
        'Дата регистрации': pd.Timestamp.now().strftime("%Y-%m-%d"),
        'Роль': role,
        'Активен': False
    }
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    print(f"Регистрация успешна! Ваш пароль: {password}")
    log_action(f"Успешная регистрация: {login}")
    return df

def change_password(df):
    login = input("Введите логин: ")
    if login in df['Логин'].values:
        while True:
            new_pass = input("Введите новый пароль (a для генерации пароля): ").strip()
            if new_pass == "a":
                new_pass = generate_password()
            elif len(new_pass) < 6:
                print("Пароль должен содрежать минимум 6 символов")
                continue
            break

        df.loc[df['Логин'] == login, 'Пароль'] = new_pass
        print(f"Новый пароль: {new_pass}")
        log_action(f"Успешная смена пароля: {login}")
    else:
        print("Пользователь не найден.")
    return df

def edit_user(df):
    login = input("Введите логин пользователя: ")
    if login not in df['Логин'].values:
        print("Нет такого пользователя.")
        return df

    name = input("Новое имя (Enter — пропустить): ")
    surname = input("Новая фамилия (Enter — пропустить): ")
    role = input("Новая роль (Enter — пропустить): ")

    if name: df.loc[df['Логин'] == login, 'Имя'] = name
    if surname: df.loc[df['Логин'] == login, 'Фамилия'] = surname
    if role: df.loc[df['Логин'] == login, 'Роль'] = role

    print("Данные обновлены.")
    log_action(f"Изменение данных пользователя: {login}")
    return df

def search(df):
    term = input("Введите имя, роль или статус (True/False): ")
    res = df[df.astype(str).apply(lambda x: x.str.contains(term, case=False, na=False)).any(axis=1)]
    print(res if not res.empty else "Ничего не найдено.")
    return df

def filter_users(df):
    role = input("Введите роль (Enter — пропустить): ")
    status = input("Введите статус (True/False или Enter): ")

    filtered = df.copy()
    if role:
        filtered = filtered[filtered['Роль'].str.lower() == role.lower()]
    if status:
        filtered = filtered[filtered['Активен'] == (status.lower() == 'true')]

    print(filtered if not filtered.empty else "Совпадений нет.")
    return df

def mass_status(df):
    new_status = input("Введите новый статус для всех (True/False): ")
    if new_status.lower() in ['true', 'false']:
        df['Активен'] = (new_status.lower() == 'true')
        print("Статусы изменены.")
        log_action(f"Успешное изменение статусов")
    else:
        print("Некорректный ввод.")
    return df

def logins_with_surname(df):
    count = 0
    for _, row in df.iterrows():
        if str(row['Фамилия']).lower() in str(row['Логин']).lower():
            count += 1
    print(f"Пользователей, чей логин содержит фамилию: {count}")
    return count

def show_stats(df):
    print(f"Активных пользователей: {df['Активен'].sum()}")
    print("Пользователи по ролям:")
    print(df['Роль'].value_counts())
    print("Повторяющиеся имена:")
    print(df['Имя'].value_counts()[df['Имя'].value_counts() > 1])
    
def export_csv(df):
    try:
        df.to_csv('export/users.csv', index=False, encoding='utf-8')
        print("База данный успешно сохранена в export/users.csv")
        log_action("База данных сохранена в CSV")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

def get_active_users_by_role_from_logs(role_input):
    daily_counts = {}

    try:
        with open("app.log", encoding="utf-8") as f:
            for line in f:
                if "LOGIN" in line or "LOGOUT" in line:
                    parts = line.split()

                    date = parts[0]
                    action = parts[5]
                    role = parts[7].split("=")[1]

                    if role != role_input:
                        continue

                    if date not in daily_counts:
                        daily_counts[date] = 0

                    if action == "LOGIN":
                        daily_counts[date] += 1
                    elif action == "LOGOUT":
                        daily_counts[date] -= 1

    except FileNotFoundError:
        print("Лог-файл не найден.")
        return {}

    return daily_counts
