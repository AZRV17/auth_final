from utils.password_generator import generate_password
import pandas as pd

def login(df):
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    match = df[(df['Логин'] == login) & (df['Пароль'] == password)]
    if not match.empty:
        df.loc[df['Логин'] == login, 'Активен'] = True
        print(f"Вход выполнен: {login}")
    else:
        print("Неверный логин или пароль.")
    return df

def logout(df):
    login = input("Введите логин для выхода: ")
    if login in df['Логин'].values:
        df.loc[df['Логин'] == login, 'Активен'] = False
        print(f"Пользователь {login} вышел из системы.")
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
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
