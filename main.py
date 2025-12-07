from repository.user import User
from service.user import *

def main():
    users = User()
    df = users.get_all_users()

    while True:
        print("""
        ---------------------------------
                      МЕНЮ
        ---------------------------------
        1. Вход
        2. Выход
        3. Регистрация
        4. Сменить пароль
        5. Изменить данные пользователя
        6. Поиск
        7. Фильтрация по роли/статусу
        8. Массовое изменение статуса
        9. Статистика
        10. Показать всех пользователей
        11. Логины содержащие фамилию
        12. Экспортировать таблицу в csv
        0. Выйти
        """)

        choice = input("Выберите действие: ").strip()

        match choice:
            case '1': df = login(df)
            case '2': df = logout(df)
            case '3': df = register(df)
            case '4': df = change_password(df)
            case '5': df = edit_user(df)
            case '6': df = search(df)
            case '7': df = filter_users(df)
            case '8': df = mass_status(df)
            case '9': show_stats(df)
            case '10': print(df)
            case '11': logins_with_surname(df)
            case '12': export_csv(df)
            case '0':
                print("Программа завершена.")
                break
            case _: print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
