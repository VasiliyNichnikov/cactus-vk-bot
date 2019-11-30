from vk_api.utils import get_random_id


class WorkMessage:
    def __init__(self, vkApi, chatId, parent=None):
        self.parent = parent
        self.vkApi = vkApi
        self.chatId = chatId

    def SendMessage(self, message, file=None):
        self.vkApi.messages.send(chat_id=self.chatId, random_id=get_random_id(), message=message, attachment=file)