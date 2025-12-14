import pandas as pd
import numpy as np
from datetime import datetime
from utils.password_generator import generate_password

ROLES = ['Администратор', 'Клиент', 'Менеджер', 'Оператор']

class User:
    def __init__(self):
        np.random.seed(1)
        data = {
            'ID': range(1, 21),
            'Имя': np.random.choice(['Иван', 'Александр', 'Петр', 'Дмитрий', 'Даниил'], 20),
            'Фамилия': np.random.choice(['Иванов', 'Александров', 'Петров', 'Дмитриев', "Данилов"], 20),
            'Логин': [f'user{i}' for i in range(1, 21)],
            'Email': [f"newuser{i}@mail.com" for i in range(1, 21)],
            'Пароль': [generate_password() for _ in range(20)],
            'Дата регистрации': [datetime.now().strftime('%Y-%m-%d')] * 20,
            'Роль': np.random.choice(ROLES, 20),
            'Активен': np.random.choice([True, False], 20)
        }
        self.users = pd.DataFrame(data)

    def get_all_users(self):
        return self.users

    def update_users(self, df):
        self.users = df
