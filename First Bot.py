#import vk_api

#vk = vk_api.VkApi(token='f4e3202c31d3cf981103ba94c17d4a08a412e02349a58d1849e95833538f5ea68ac40c2f14babc785d386')

#while True:
#    messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
#    if messages["count"] >= 1:
#        id = messages["items"][0]["last_message"]["from_id"]
#        body = messages["items"][0]["last_message"]["text"]
#        if body.lower() == 'привет':
#            vk.method("messages.send", {"peer_id": id, "random_id":  0, "message": "дарова стасян"})

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message)

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(255396611, "Привет-привет!")

#from server import Server
# Получаем из config.py наш api-token
#from config import vk_api_token


#server1 = Server(vk_api_token, 172998024, "server1")
# vk_api_token - API токен, который мы ранее создали
# 172998024 - id сообщества-бота
# "server1" - имя сервера

#server1.test()