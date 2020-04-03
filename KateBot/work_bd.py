import psycopg2


class WorkBD:
    # Инициализация и подключение к БД heroku
    def __init__(self):
        self.connection = None
        self.connection = psycopg2.connect(
            database="da7jf64t7k39md",
            user="tabuknomivnqmy",
            password="a8831b83d310061f306cbaa4d3c14ebf77d2344795e6b22d1176dea370d59a28",
            host="ec2-23-22-156-110.compute-1.amazonaws.com",
            port="5432"
        )
        self.cursor = self.connection.cursor()
    print("БД загружена")

    # Создание таблицы для хранения пользователей
    def create_table_bd(self):
        self.cursor.execute('''CREATE TABLE USERS (USER_ID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, 
        NOTIFICATION_SEND BOOL DEFAULT FALSE)''')
        print("Таблица создана")
        self.connection.commit()
        self.connection.close()

    # Добавление информации о пользователе в БД
    def add_info_user_bd(self, user_id, name, notification_send):
        print(user_id, name, notification_send)
        sql = '''INSERT INTO USERS(USER_ID, NAME, NOTIFICATION_SEND) VALUES (%s, %s, %s);'''
        print(self.cursor)
        self.cursor.execute(sql, (user_id, name, notification_send))
        print("User добавлен в таблицу")
        self.connection.commit()
        self.connection.close()

    # Получение информации из БД
    def get_info_user_bd(self):
        self.cursor.execute("SELECT USER_ID, NAME, NOTIFICATION_SEND from USERS")
        rows = self.cursor.fetchall()
        for i in rows:
            print('User id -', i[0])
            print('Name -', i[1])
            print('NOTIFICATION_SEND -', i[2])
        self.connection.close()
        print('Все пользователи получены')

    # Проверка, отправлено ли сообщение или нет
    def check_send_notification(self, user_id):
        self.cursor.execute("SELECT USER_ID, NAME, NOTIFICATION_SEND from USERS")
        users = self.cursor.fetchall()
        print('Проверка завершена')
        for i in users:
            user_id_bd = i[0]
            notification_send_bd = i[-1]
            if user_id_bd == user_id and notification_send_bd:
                return False
        return True