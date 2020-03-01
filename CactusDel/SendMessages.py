from vk_api.utils import get_random_id


# Данный класс нужен для отправки сообщений
class SendMessages:
    def __init__(self, vk_api, parent):
        self.parent = parent
        self.vk_api = vk_api

    # Метод для отправки сообщений в лс (Сообщения только с тексом)
    def SendMessage(self, messageText):
        self.vk_api.messages.send(peer_id=self.parent.peer_id, random_id=get_random_id(), message=messageText)

