import psycopg2


class WorkBD:
    # Инициализация и подключение к БД heroku
    def __init__(self):
        self.connection = None
        self.connection = psycopg2.connect(
            database="dckdmspjfi40au",
            user="cozvlczrmakcgy",
            password="7efb344b3b78fc7eb389f8570bd0edfbb9d4a607c586232e2c03940f0d10ed29",
            host="ec2-18-235-20-228.compute-1.amazonaws.com",
            port="5432"
        )
        self.cursor = self.connection.cursor()
    print("БД загружена")

    # Создание таблицы для хранения пользователей
    def create_table_bd(self):
        self.cursor.execute('''CREATE TABLE USERS (USER_ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, 
        NOTIFICATION_SEND BOOL DEFAULT FALSE)''')
        print("Таблица создана")
        self.connection.commit()
        self.connection.close()

    # Добавление информации о пользователе в БД
    def add_info_user_bd(self, user_id, name, notification_send):
        sql = '''INSERT INTO USERS(USER_ID, NAME, NOTIFICATION_SEND) VALUES (%s, %s, %s);'''
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
                self.connection.close()
                return False
        self.connection.close()
        return True
