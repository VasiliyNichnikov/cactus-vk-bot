import sqlite3
from datetime import datetime
from sqlite3 import Error


class WorkingDataBase:
    def __init__(self, path):
        self.connection = self.create_connection(path)
        self.creating_table_users()

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print('БД успешна подключена')
        except Error as e:
            print(f'Ошибка: {e}')
        return connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f'Ошибка: {e}')

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f'Ошибка: {e}')

    def creating_table_users(self):
        create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                selected_function TEXT,
                phase_function TEXT
            );
        """
        self.execute_query(create_users_table)

    def add_user(self, user_id):
        print('Новый пользователь добавлен в БД')
        add_user_bd = """
            INSERT INTO 
                users (user_id, selected_function, phase_function) 
            VALUES 
                ({}, {}, {});
        """.format(user_id, 'null', 'null')
        self.execute_query(add_user_bd)

    def update_phase_function(self, user_id, phase_function):
        change_selected_function = """
            UPDATE 
                users 
            SET 
                phase_function = "{}" 
            WHERE 
                user_id = {}""".format(phase_function, user_id)
        self.execute_query(change_selected_function)

    def update_selected_function(self, user_id, selected_function):
        change_selected_function = """
                    UPDATE 
                        users 
                    SET 
                        selected_function = "{}" 
                    WHERE 
                        user_id = {}""".format(selected_function, user_id)
        self.execute_query(change_selected_function)

    def get_user(self, user_id):
        select_user = """
            SELECT user_id, selected_function, phase_function  FROM users WHERE user_id == {}
        """.format(user_id)
        user = self.execute_read_query(select_user)
        if len(user) != 0:
            dict_user = {
                'user_id': user[0][0],
                'selected_function': user[0][1],
                'phase_function': user[0][2]
            }

            return dict_user
        return None
