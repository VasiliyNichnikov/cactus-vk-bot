import vk_api
import requests
import json
from Bot.GeneralGathering import GeneralGathering
from Bot.InfoWeather import InfoWeather
from Bot.Reminder import Reminder
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

# Токен бота
token_bot = '4f22434cd699dd0209b3c5e60f9d5aac529c9364f88da3a3c4d4b7b6c2251f7cecc4f0836a5b59788317e'
# Токен пользователя
token_user = '73c46d213cebd5794a7dfc5471a792bc670b0be4c7452191f25bfdd094b70a78b620994d19e001d883688'
# Токен приложения
token_app = '3cd9d1bedb7358529b317062d172112e43c81afa025349c82b33382310535f38c79ca58499718324f7ce2'


class Server:
    # инициализация группы
    def __init__(self, api_token, app_token,  group_id, server_name="Empty"):
        print("Create server")
        # Даем имя серверу
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        self.app = vk_api.VkApi(token=app_token)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()
        self.vk_app_api = self.app.get_api()
        # id чата
        self.chat_id = 0
        self.group_id = group_id
        # Запуск команды, которая получает и обрабатывает сообщения
        self.ObtainingInformation()

    # Получение информации
    def ObtainingInformation(self):
        for event in self.long_poll.listen():
            self.chat_id = event.chat_id
            print(event.obj.message_id)
            # Сообщение пользователя
            userMessage = event.obj.text.lower()
            # Имя пользователя
            user_name = self.vk_api.users.get(user_ids=event.object.from_id)[0]['first_name']  # Имя пользователя
            # Создает классы всех команд
            dictCommandsBot = {'!общий сбор': GeneralGathering(self.vk_api, self.chat_id,
                                                               isAdmin=self.CheckAdminGroup(user_name), parent=self),
                               '!погода': InfoWeather(self.vk_api, self.chat_id, self),
                               '!напоминание': Reminder(self.vk_api, self.chat_id, self)
                               }
            if userMessage.lower() in dictCommandsBot.keys():
                dictCommandsBot[userMessage].Command()
            # try:
            #     #  работа с сообщением пользователя
            #     if userMessage.lower() in dictCommandsBot.keys():
            #         dictCommandsBot[userMessage].Command()
            # except:
            #     self.SendMessage(self.chat_id, "Error 01")

    # Метод для отправки сообщений в группу
    def SendMessage(self, chat_id, messageText, addFiles=None):
        self.vk_api.messages.send(chat_id=chat_id, random_id=get_random_id(), message=messageText, attachment=addFiles)

    # Проверяет пользователя, если пользлователь Админ, возвращает True, иначе False
    def CheckAdminGroup(self, user_name_check):
        arrayParticipants = self.vk_api.messages.getConversationMembers(peer_id=2000000000 + self.chat_id)
        for user in arrayParticipants['items']:
            user_id = user['member_id']
            user_admin = False
            try:
                user_admin = user['is_admin']
            except:
                pass
            if user_id >= 0:
                user_name = self.vk_api.users.get(user_ids=user_id)[0]['first_name']  # Имя пользователя
                if user_name == user_name_check and user_admin:
                    return True
        print(user_name_check, ", данный пользователь не является администратором")
        return False