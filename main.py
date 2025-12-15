from repository.user import User
from service.user import *
from service.visualization import *

def main():
    users = User()
    # conn = users.ge

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
        13. Диаграмма пользователей по ролям
        14. График регистраций по датам
        15. Активные пользователи по роли
        0. Выйти
        """)

        choice = input("Выберите действие: ").strip()

        match choice:
            case '1': login()
            case '2': logout()
            case '3': register()
            case '4': change_password()
            case '5': edit_user()
            case '6': search()
            case '7': filter_users()
            case '8': mass_status()
            case '9': show_stats()
            case '10': print_all_users()
            case '11': logins_with_surname()
            case '12': export_csv()
            case '13': users_by_role()
            case '14': registrations_by_date()
            case '15': active_users_by_role()
            case '0':
                print("Программа завершена.")
                break
            case _: print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
