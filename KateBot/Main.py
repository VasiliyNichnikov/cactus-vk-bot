import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from datetime import timedelta, datetime
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType


# Доступ открыт только людям с данными id
open_door = [332244874, 306255161]


class Server:
    # команды, которые поддерживаются ботом
    teams = {}
    # Дата сейчас
    date_now = datetime.now()
    # Дата дня рождения
    date_end = datetime(2020, 4, 14)

    def __init__(self, api_token, group_id, server_name="None"):
        # Имя сервера
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    # Отправка сообщений
    def send_msg(self, send_id, message, attachment=None):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(), attachment=attachment)

    # Запуск сервера
    def start(self):
        for event in self.long_poll.listen():
            if event.object.from_id in open_door:
                print('Доступ открыт')
                print(self.period())
                self.send_msg(event.object.peer_id, "ФОТО", self.load_image())

    # Вычитает даты
    def period(self):
        period_data = self.date_end - self.date_now
        return datetime.fromtimestamp(period_data.total_seconds()).strftime("%d, %I:%M:%S")

    # Загрузка фото (Возвращает фото по дате)
    def load_image(self):
        upload = vk_api.VkUpload(self.vk)
        photo = upload.photo_messages('KateBot/static/images/kate_1.jpeg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        return attachment
