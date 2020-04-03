import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from datetime import datetime
from vk_api.utils import get_random_id
import os.path
import requests
import threading
from KateBot.work_bd import WorkBD
from vk_api.bot_longpoll import VkBotEventType
from KateBot.work_image import TransformationImage


# Доступ открыт только людям с данными id
open_door = [332244874, 306255161]


class Server:
    # Преобразуем аремя
    #  utc = pytz.utc
    #  moscow = timezone('Europe/Moscow')

    # Дата дня рождения
    #  date_end = moscow.localize(datetime(2020, 4, 14))
    date_end = datetime(2020, 4, 14)

    def __init__(self, api_token, app_token, group_id, server_name="None"):
        # Имя сервера
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Для работы с приложением
        self.app = vk_api.VkApi(token=app_token)
        # Для работы с уведомлениями
        #  self.notification = vk_api.VkApi(token=key_notification)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()
        # Для работы с функциями приложения
        self.vk_app = self.app.get_api()
        # id группы
        self.group_id = group_id

        # Запуск уведомлений
        for peer_id in open_door:
            self.start_notification(peer_id)
        print("Бот живой!")

    # Отправка сообщений
    def send_msg(self, send_id, message, attachment=None):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(), attachment=attachment)

    # Запуск сервера
    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                # Сообщение пользователя
                user_message = str(event.object.message['text']).lower()
                peer_id = int(event.object.message['from_id'])
                if peer_id in open_door and user_message == 'фото':
                    print('Отправка фото и не только')
                    self.send_msg_every_day(peer_id)

    # Вычитает даты
    def period(self, day=False):
        # Дата сейчас
        date_now = datetime.now()
        period_data = self.date_end - date_now
        if not day:
            return self.get_date(period_data)
        return period_data.days

    # Отпрака сообщений каждый день
    def send_msg_every_day(self, user_peer_id):
        # Номер дня
        num_day = self.period(True)
        # Текст, который отправится в сообщение, отправка мини-фраз
        text = self.mini_phrases(num_day)
        # Отправка сообщения
        #  print('Отправка сообщения:', text)
        if text is not False or self.check_audio(num_day) is not False:
            self.send_msg(user_peer_id, text, self.load_audio(num_day))
        self.send_msg(user_peer_id, "", self.load_image(num_day))

    # Загрузка фото (Возвращает фото по дате)
    def load_image(self, num_day):
        # Текст, который буден написан на фото
        text = str(self.period())
        # Класс, который преобразует изображение
        transformation_image = TransformationImage(f'KateBot/static/images/kate_{num_day}.jpeg')
        # Готовое изображение, которое мы отправляем пользователю
        transformation_image.add_panel_text(text)
        # Загрузка изображения
        upload = vk_api.VkUpload(self.vk)
        photo = upload.photo_messages("KateBot/static/ready_image.jpeg")
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        print("Фото создано")
        return attachment

    # Загрузка аудио файла (Возвращает аудио по дате)
    def load_audio(self, num_day):
        # Путь к файлу
        path = f"KateBot/static/audios/ten_days/days_left_{num_day}.mp3"
        # Открываем файл аудио
        audio_file = open(path, "rb")
        # Получение URL куда загружать аудио
        url = self.vk_app.audio.getUploadServer()
        # Загрузка аудио файла на сервер
        load_url = requests.post(url["upload_url"], files={"file": audio_file}).json()
        # Сохранение аудио файла
        audio_save = self.vk_app.audio.save(server=load_url["server"], audio=load_url["audio"],
                                            hash=load_url['hash'], artist="Cactus Bot", title="NotBdayBot")
        # Готовая строка для отправки в сообщения
        attachment = f"audio{audio_save['owner_id']}_{audio_save['id']}"
        print("Аудио создано")
        return attachment

    # Проверяет, есть ли аудио файл
    def check_audio(self, num_day):
        path = f"KateBot/static/audios/ten_days/days_left_{num_day}.mp3"
        file = os.path.exists(path)
        if file:
            return True
        return False

    # Словарь с мини фразами
    dict_mini_phrases = {
        30: 'Милый сурок, будь веселее, хорошего дня и настроения!',
        25: 'Успех - это успеть. Опа. 25 дней! Небольшой намек(11)!',
        20: '20 дней, если 10 * 2, то будет 20. ПРИКИНЬ',
        15: 'Если проблему можно разрешить, не стоит о ней беспокоиться. '
            'Если проблема неразрешима, беспокоиться о ней бессмысленно.',
        10: '10 ДНЕЙ. УРА. СОВСЕМ СКОРО БУДЕТ ПРАЗДНИК!!!!!',
        9: '9 ДНЕЙ. Привет милый сурок. Я скучаю!',
        8: '8 ДНЕЙ. Осталось совсем немного!',
        7: '7 ДНЕЙ. Что делаешь, как дела, как настроение? Праздник близок!',
        6: '6 ДНЕЙ. Любишь день рождения? Я да)',
        5: '5 ДНЕЙ. Готовь торт, шарики, свечи, праздник вышел! А я пойду спать, но это не точно)))',
        4: '4 ДНЯ. Ты прекрасно выглядишь!(ВСЕГДА)',
        3: 'БОГ ЛЮБИТ ТРОЕЦУ (И ТРОИЦКОЮ), ТРИ МЕСЯЦА ВО ВРЕМЕНИ ГОДА, ТРИ ДНЯ!)',
        2: '2 ДНЯ. Торт готов?',
        1: '1 ДЕНЬ. Помнишь, я говорил, что люблю дни рождения? Тебя я люблю больше)',
        0: 'ССЫЛКА НА ВИДЕО'
    }

    # Запускает уведомления
    def start_notification(self, peer_id):
        notification = threading.Thread(target=self.notification, name="Notification",
                                        args=(peer_id,), daemon=True)
        notification.start()

    # Мини фразы, которые отправляются каждый 5 день
    def mini_phrases(self, num_day):
        if num_day in self.dict_mini_phrases:
            return self.dict_mini_phrases[num_day]
        return False

    # Возвращает информацию, сколько дней, часов и минут осталось до дня рождения
    def get_date(self, date):
        res_date = str(date).split()
        day = res_date[0]
        _time = res_date[-1].split(':')
        hours = _time[0]
        minutes = _time[1]
        seconds = _time[-1].split('.')[0]

        res_line = f"{day} дней; {hours}:{minutes}:{seconds}"
        return res_line

    # Уведомление, они будут приходить в новый день
    def notification(self, peer_id):
        while True:
            day = self.period(True)
            key = f"{day}_{peer_id}"
            name = self.vk_api.users.get(user_ids=[peer_id])[0]['first_name']
            bd = WorkBD()
            if bd.check_send_notification(key):
                print("Отправка фото")
                bd.add_info_user_bd(key, name, True)
                # Отправка фото
                self.send_msg_every_day(peer_id)

