import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from datetime import timedelta, datetime
from vk_api.utils import get_random_id
import requests
import asyncio
import time
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

    # словарь, который проверяет, отправлял бот или нет уведомление
    dict_date_check = {}

    def __init__(self, api_token, app_token, group_id, server_name="None"):
        test = requests.get('http://carbrain.org/vk_bot/')
        print(test.text)
        # Имя сервера
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Для работы с приложением
        self.app = vk_api.VkApi(token=app_token)
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
            if event.type == VkBotEventType.MESSAGE_NEW:
                # Сообщение пользователя
                user_message = event.obj.text.lower()
                if event.object.from_id in open_door and user_message == 'фото':
                    print('Отправка фото и не только')
                    self.send_msg_every_day(event.object.peer_id)
                else:
                    self.send_msg(event.object.peer_id, "I do not understand вас :)")

    # Вычитает даты
    def period(self, day=False):
        period_data = self.date_end - self.date_now
        if not day:
            return datetime.fromtimestamp(period_data.total_seconds()).strftime("%d, %I:%M:%S")
        return int(datetime.fromtimestamp(period_data.total_seconds()).strftime("%d"))

    # Отпрака сообщений каждый день
    def send_msg_every_day(self, user_peer_id):
        num_day = self.period(True)
        if num_day not in self.dict_date_check:
            # Добавляем в словарь
            self.dict_date_check[num_day] = True
            num_day = self.period(True)
            # Текст, который отправится в сообщение
            text = f'{self.period()}. {self.mini_phrases(num_day)}'
            # Отправка сообщения
            print('Отправка сообщения:', text)
            self.send_msg(user_peer_id, text, self.load_image(num_day))

    # Загрузка фото (Возвращает фото по дате)
    def load_image(self, num_day):
        upload = vk_api.VkUpload(self.vk)
        #  test = upload.photo_messages(f"../static/images/kate_{num_day}.jpeg")
        photo = upload.photo_messages(f'KateBot/static/images/kate_{num_day}.jpeg')
        print("Фото создано")
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        return attachment

    # Словарь с мини фразами
    dict_mini_phrases = {
        30: 'Милый сурок, будь веселее, хорошего дня и настроения!',
        25: 'Успех - это успеть. Опа. 25 дней! Небольшой намек(11)!',
        20: '20 дней, если 10 * 2, то будет 20. ПРИКИНЬ',
        15: 'Если проблему можно разрешить, не стоит о ней беспокоиться. '
            'Если проблема неразрешима, беспокоиться о ней бессмысленно.',
        10: '10 ДНЕЙ. УРА. СОВСЕМ СКОРО БУДЕТ ПРАЗДНИК!!!!!',
        5: '5 дней. Готовь торт, шарики, свечи, праздник вышел! А я пойду спать, но это не точно)))'
    }

    # Мини фразы, которые отправляются каждый 5 день
    def mini_phrases(self, num_day):
        if num_day in self.dict_mini_phrases:
            return self.dict_mini_phrases[num_day]
        return ""
