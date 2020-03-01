import vk_api
from CactusDel.CreatingCases import CreateCaseOnDay
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from CactusDel.SendMessages import SendMessages


class Server:
    def __init__(self, api_token, app_token,  group_id, server_name="Empty"):
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
        # Переменная, которая говорит, что программа выполняется в другом скрипте
        self.functionOn = False
        # Класс, который сейчас работает
        self.workClass = None
        self.peer_id = None

        # Инициализация словаря
        self.dictFunctions = {
            'создание дел': CreateCaseOnDay(self)
        }

        # Инициализация дополнительных классов
        self.classSendMessage = SendMessages(self.vk_api, self)

        # Запуск команды, которая получает и обрабатывает сообщения
        self.MainFunction()

    def MainFunction(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.peer_id = event.object.peer_id
                # Сообщение пользователя
                userMessage = event.obj.text.lower()
                if not self.functionOn:
                    self.functionOn = True
                    classStart = self.dictFunctions[userMessage]
                    self.workClass = classStart
                    classStart.Start_func()
                    print(userMessage)
                else:
                    self.workClass.Work(userMessage)
            # self.chat_id = event.chat_id
