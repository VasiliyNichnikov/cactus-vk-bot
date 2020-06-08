import sqlite3
import psycopg2
from contextlib import closing
from psycopg2 import OperationalError, Error
# from sqlite3 import Error


class WorkingDataBase:
    def __init__(self):
        self.connection = self.create_connection()
        self.create_table_users()

    def create_connection(self):
        connection = None
        try:
            connection = psycopg2.connect(
                database='d4jdnn5eo5il2s',
                user='hwibtovddiqcpt',
                password='b217efb730ad4ab9747dcdfab2189ace3010c486e2612de0855229f308184aa5',
                host='ec2-3-222-30-53.compute-1.amazonaws.com',
                port='5432'
            )
            print('Подключение завершено корректно')
        except OperationalError as e:
            print('Error %s', e)
        return connection

    def execute_read_cursor(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print('Error %s' % e)
        return result

    def execute_query(self, query):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print('Ок (execute_query)')
        except OperationalError as e:
            print('Error %s', e)

    def create_table_users(self):
        create_users_table = ''' CREATE TABLE IF NOT EXISTS users_vk (user_id INT PRIMARY KEY NOT NULL,
            selected_function TEXT, phase_function TEXT) '''
        self.execute_query(create_users_table)

    def add_user(self, user_id):
        with closing(self.create_connection()) as connect:
            with connect.cursor() as cursor:
                add_user = '''INSERT INTO users_vk (user_id, selected_function, phase_function) VALUES (%s, %s, %s); '''
                cursor.execute(add_user, (user_id, 'null', 'null'))
                connect.commit()

    def update_phase_function(self, user_id, phase_function):
        change_selected_function = ''' UPDATE users_vk SET phase_function = '{}' WHERE user_id = {}'''\
            .format(phase_function, user_id)
        self.execute_query(change_selected_function)

    def update_selected_function(self, user_id, selected_function):
        change_selected_function = ''' UPDATE users_vk SET selected_function = '{}' WHERE user_id = {}'''\
            .format(selected_function, user_id)
        self.execute_query(change_selected_function)

    def reset_selected_function(self):
        reset_selected_function = ''' UPDATE users_vk SET selected_function = 'null' '''
        self.execute_query(reset_selected_function)

    def get_user(self, user_id):
        select_user = ''' SELECT * FROM users_vk WHERE user_id = '{}' '''.format(user_id)
        user = self.execute_read_cursor(select_user)
        if len(user) == 0:
            return None
        print(user)
        dict_user = {
            'user_id': user[0][0],
            'selected_function': user[0][1],
            'phase_function': user[0][2]
        }
        return dict_user



    # def get_user(self, user_id):
    #     select_user = """
    #         SELECT user_id, selected_function, phase_function  FROM users WHERE user_id == {}
    #     """.format(user_id)
    #     user = self.execute_read_query(select_user)
    #     if len(user) != 0:
    #         dict_user = {
    #             'user_id': user[0][0],
    #             'selected_function': user[0][1],
    #             'phase_function': user[0][2]
    #         }
    #         return dict_user
    #     return None
