from datetime import datetime

from repository.user import get_connection
from service.email import send_email
from utils.logger import log_action
from utils.password_generator import generate_password

import pandas as pd

from utils.password_hash import hash_password, verify_password

LOG_FILE = "app.log"
ROLES = ['Администратор', 'Клиент', 'Менеджер', 'Оператор']

def login():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    conn = get_connection()
    cur = conn.cursor()

    password_hash, role = cur.execute("""
                SELECT password, role
                FROM users
                WHERE login = ?
                """, (login,)).fetchone()

    if not verify_password(password, password_hash):
        print("Неправильный логин или пароль")

    if role:
        cur.execute("""
                    UPDATE users
                    SET is_active=1
                    WHERE login = ?
                    """, (login,))
        conn.commit()

        log_action(f"Успешный вход пользователя: {login}")
        log_action(f"LOGIN {login} role={role[0]}")
        print(f"Вход выполнен: {login}")
    else:
        log_action(f"Неудачный вход пользователя: {login}")
        print("Неверный логин или пароль.")
    conn.close()

def logout():
    login = input("Введите логин для выхода: ")

    conn = get_connection()
    cur = conn.cursor()

    role = cur.execute("SELECT role FROM users WHERE login=?", (login,)).fetchone()
    if role:
        cur.execute("""
                    UPDATE users
                    SET is_active=0
                    WHERE login = ?
                    """, login)
        conn.commit()
        print(f"Пользователь {login} вышел из системы.")
        log_action(f"Выход из системы: {login}")
        log_action(f"LOGOUT {login} role={role[0]}")
    else:
        print("Логин не найден.")
    conn.close()

def register():
    conn = get_connection()
    cur = conn.cursor()

    login = input("Введите логин: ")
    email = input("Введите email: ").strip()

    cur.execute("SELECT 1 FROM users WHERE login=? OR email=?", (login, email))
    if cur.fetchone():
        print("Логин или email уже существует")
        conn.close()
        return

    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    role = input("Введите роль (по умолчанию Клиент): ") or "Клиент"
    if role not in ROLES:
        print("Неверная роль (Администратор, Клиент, Менеджер, Оператор)")
        conn.close()
        return

    while True:
        password = input("Введите пароль (a для генерации пароля): ").strip()
        if password == "a":
            password = generate_password()
        elif len(password) < 6:
            print("Пароль должен содрежать минимум 6 символов")
            continue
        break

    password_hash = hash_password(password)

    try:
        code = send_email(email)
        print("Код отправлен на почту")
    except:
        print("Регистрация прервана из-за ошибки отправки email")
        log_action(f"EMAIL_ERROR email={email}")
        conn.close()
        return

    confirm = input("Введите код, полученный по почте: ")
    if confirm != code:
        print("Неверный код. Регистрация отменена")
        log_action(f"Неудачная регистрация email={email}")
        conn.close()
        return

    cur.execute("""
                INSERT INTO users
                (first_name, last_name, login, email, password, registered_at, role, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """, (
                    name, surname, login, email,
                    password_hash, datetime.now().strftime("%Y-%m-%d"), role
                ))

    conn.commit()
    conn.close()
    print(f"Регистрация успешна! Ваш пароль: {password}")
    log_action(f"Успешная регистрация: {login}")

def change_password():
    login = input("Введите логин: ")
    conn = get_connection()
    cur = conn.cursor()

    user_id = cur.execute("SELECT id FROM users WHERE login=?", (login,)).fetchone()

    if user_id:
        while True:
            new_pass = input("Введите новый пароль (a для генерации пароля): ").strip()
            if new_pass == "a":
                new_pass = generate_password()
            elif len(new_pass) < 6:
                print("Пароль должен содрежать минимум 6 символов")
                continue
            break

        password_hash = hash_password(new_pass)

        cur.execute("""
                    UPDATE users
                    SET password=?
                    WHERE login = ?
                    """, (password_hash, login))

        conn.commit()
        conn.close()
        print(f"Новый пароль: {new_pass}")
        log_action(f"Успешная смена пароля: {login}")
    else:
        print("Пользователь не найден.")

def edit_user():
    login = input("Введите логин пользователя: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE login=?", (login,))
    if not cur.fetchone():
        print("Пользователь не найден")
        conn.close()
        return

    name = input("Новое имя (Enter — пропустить): ")
    surname = input("Новая фамилия (Enter — пропустить): ")
    role = input("Новая роль (Enter — пропустить): ")

    if name:
        cur.execute("UPDATE users SET first_name=? WHERE login=?", (name, login))
    if surname:
        cur.execute("UPDATE users SET last_name=? WHERE login=?", (surname, login))
    if role:
        cur.execute("UPDATE users SET role=? WHERE login=?", (role, login))

    conn.commit()
    conn.close()

    print("Данные обновлены")
    log_action(f"Изменение данных пользователя: {login}")

def search():
    term = input("Введите имя, роль или статус (True/False): ").lower()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM users
        WHERE lower(first_name) LIKE ?
           OR lower(last_name) LIKE ?
           OR lower(role) LIKE ?
           OR CAST(is_active AS TEXT) LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("Ничего не найдено")
    else:
        for r in rows:
            print(r)

def filter_users():
    role = input("Введите роль (Enter — пропустить): ")
    status = input("Введите статус (True/False или Enter): ")

    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if role:
        query += " AND role=?"
        params.append(role)

    if status.lower() in ["true", "false"]:
        query += " AND is_active=?"
        params.append(1 if status.lower() == "true" else 0)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("Совпадений нет")
    else:
        for r in rows:
            print(r)

def mass_status():
    new_status = input("Введите новый статус для всех (True/False): ").lower()

    if new_status not in ["true", "false"]:
        print("Некорректный ввод")
        return

    if new_status == "true":
        status_value = 1
    else:
        status_value = 0

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET is_active=?", (status_value,))
    conn.commit()
    conn.close()

    log_action(f"Успешное изменение статусов")
    print("Статусы всех пользователей изменены")

def logins_with_surname():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                SELECT login, last_name
                FROM users
                WHERE lower(login) LIKE '%' || lower(last_name) || '%'
                """)

    rows = cur.fetchall()
    conn.close()

    count = len(rows)

    print(f"Пользователей, чей логин содержит фамилию: {count}")

    if count > 0:
        for login, last_name in rows:
            print(f"Логин: {login}, Фамилия: {last_name}")

def show_stats():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    print(f"Активных пользователей: {df['is_active'].sum()}")
    print("Пользователи по ролям:")
    for role, count in df['role'].value_counts().items():
        print(f"  {role}: {count}")
    print("Повторяющиеся имена:")
    repeated = df['first_name'].value_counts()
    repeated = repeated[repeated > 1]

    if repeated.empty:
        print("  Нет повторяющихся имен")
    else:
        for name, count in repeated.items():
            print(f"  {name}: {count}")
    
def export_csv():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()
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

def print_all_users():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    print(df)
    conn.close()
