import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id
from BotTeacher.EGE import EGE


class Server:
    dictErrorMessages = {"noCommand": "Прости, не понимаю тебя :("}
    keyboard = "C:/Users/vnich/YandexDisk/Bot_VK/keyboards/keyboard.json"

    def __init__(self, api_token, app_token, group_id, server_name="Empty"):
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

        classEGE = EGE(self)
        self.dictCommands = {"егэ": (classEGE.GreetingText(), self.ChangeKeyboard("C:/Users/vnich/YandexDisk/Bot_VK/keyboards/keyboardEGE.json")),
                             "математика": (classEGE.Mathematics(), None),
                             "к выбору егэ/огэ": (None, self.ChangeKeyboard("C:/Users/vnich/YandexDisk/Bot_VK/keyboards/keyboard.json")),
                            }
        # Запуск цикла программы
        self.ProgramCycle()

    def ProgramCycle(self):
        for event in self.long_poll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:
                # Сообщение пользователя
                userMessage = event.obj.text.lower()
                if event.object.text.lower() in self.dictCommands:
                    self.SendMessage(event.object.peer_id, self.dictCommands[event.object.text.lower()][0])
                else:
                    self.SendMessage(event.object.peer_id, self.dictErrorMessages["noCommand"])

    def SendMessage(self, send_id, message):
        print(self.keyboard)
        return self.vk_api.messages.send(peer_id=send_id,
                                         random_id=get_random_id(),
                                         message=message,
                                         keyboard=open(self.keyboard, "r", encoding="UTF-8").read())

    def ChangeKeyboard(self, keyboard):
        self.keyboard = keyboard
