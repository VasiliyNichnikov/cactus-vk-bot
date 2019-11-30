import vk_api
import requests
import json
#  from vk_api import VkUpload
from Bot.GeneralGathering import GeneralGathering
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
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
        # Запуск команды, которая получает и обрабатывает сообщения
        self.ObtainingInformation()

    # Получение информации
    def ObtainingInformation(self):
        for event in self.long_poll.listen():
            self.chat_id = event.chat_id
            # Сообщение пользователя
            userMessage = event.obj.text.lower()
            # Имя пользователя
            user_name = self.vk_api.users.get(user_ids=event.object.from_id)[0]['first_name']  # Имя пользователя
            # Создает классы всех команд
            dictCommandsBot = {'!общий сбор': GeneralGathering(self.vk_api, self.chat_id,
                                                               isAdmin=self.CheckAdminGroup(user_name), parent=self)}
            try:
                # работа с сообщением пользователя
                if userMessage in dictCommandsBot.keys():
                    dictCommandsBot[userMessage].Command()
            except:
                self.SendMessage(self.chat_id, "Error 01")

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


# class MainClass:
#     # Инициализация токенов
#     vk_session = vk_api.VkApi(token=tokenBot)
#     vk_user = vk_api.VkApi(token=tokenApp)
#
#     # Создание основных переменных
#     vk = vk_session.get_api()
#     vkUser = vk_user.get_api()
#     NUMBERGROUP = '187407860'
#     longpoll = VkBotLongPoll(vk_session, NUMBERGROUP)
#     upload = vk_api.VkUpload(vk_session)
#     session = requests.Session()
#     idBot = '306255161'  # id бота
#     attached_user = ''  # пользователь за которым бот наблюдает
#     allCommands = ['!добавь', '!опрос']
#     pollClass = None
#
#     #dictCommandsBot = {}
#
#     #listAllowedUsers = ['мария', 'василий']  # Только пользователи в этом списке могут управлять некоторыми функциями
#     #dictDomains = {'Stop Train (0)': 'stoptrain'}
#
#     for event in longpoll.listen():  # Обработка сообщения
#         #  print(event.object.from_id, event.object['action']['type'])
#         #  print(event.object.from_id, idBot)
#         #  print(event.object['action']['type'] == 'chat_invite_user', int(event.object.from_id) == int(idBot))
#         # Приветвсие при первом запуске
#         print('New', event)
#         try:
#             if event.object['action']['type'] == 'chat_invite_user' and int(event.object.from_id) == int(idBot) \
#                     and event.from_chat:
#                 workMessage = WorkMessage(vkApi=vk, chatId=event.chat_id)
#                 workMessage.SendMessage('Привет всем! Кактус-бот прибыл! '
#                                         'Для полного функционала меня нужно сделать администратором :]')
#         except:
#             pass
#
#         if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:  # Проверка, что сообщение идет из чата
#             workMessage = WorkMessage(vkApi=vk, chatId=event.chat_id)
#             userName = vk.users.get(user_ids=event.object.from_id)[0]['first_name']  # Имя пользователя
#             userMessage = event.obj.text.lower()  # Сообщение, которое отправил пользователь
#             CollectionTeamsClass = GeneralGatheringClass(userName, vk, event.chat_id)  # Создание класса
#             #  print(userMessage)
#             if userMessage == "!общий сбор":
#                 CollectionTeamsClass.CollectionTeamsOutput(CollectionTeamsClass.CollectionTeamsReminder())
#             if pollClass is not None and int(attached_user) == int(event.object.from_id) and attached_user != '':
#                 if pollClass.CheckPoll():
#                     attached_user = ''
#                     pollClass = None
#                 else:
#                     pollClass.AcceptMessage(userMessage)
#
#             polls = []
#             if 'привет' in userMessage:
#                 workMessage.SendMessage('Привет {}'.format(userName))
#             elif '!добавь' == userMessage and attached_user == '':  # Пишет коммент
#                 try:
#                     domain = vk.users.get(user_ids=event.object.from_id, fields='domain')[0]
#                     postToUserOrGroup = vkUser.wall.get(domain=domain['domain'], count='1')
#                     post = postToUserOrGroup['items']
#                     vkUser.wall.createComment(owner_id=post[0]['owner_id'], post_id=post[0]['id'], message='КРУТО')
#                     print('Ok')
#                 except:
#                     workMessage.SendMessage('У вас закрыты комментарии {}'.format(userName))
#             elif '!опрос' == userMessage and attached_user == '':
#                 #poll = vkUser.polls.create(question='Сколько тут слов?', owner_id='-187407860',
#                 #                           add_answers=json.dumps({'1': 'одно', '2': 'два', '3': 'три'}))
#                 #polls.append(
#                 #    'poll{}_{}'.format(poll['owner_id'], poll['id'])
#                 #)
#                 # print(polls)
#                 #CollectionTeamsClass.CollectionTeamsOutput('Message', polls)
#                 print(event.object.from_id)
#                 pollClass = Survey(vkApi=vk, vkUser=vkUser, chatId=event.chat_id,
#                                    userId=event.object.from_id, group_id=event.group_id)
#                 attached_user = vk.users.get(user_ids=event.object.from_id)[0]['id']
#                 print(attached_user)
#                 print('Пользователь', userName, 'прикреплен')
#             elif userMessage in allCommands and attached_user != '':
#                 workMessage.SendMessage('На данный момент бот работает с другим пользователем.')
#
#         elif event.type == VkBotEventType.GROUP_JOIN:
#             vk = vk_session.get_api()
#            vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Привет всем! Кактус-бот прибыл')
            #CollectionTeamsClass = GeneralGatheringClass(userName, vk, event.chat_id)  # Класс для сбора

            #print(event.obj)
            #if 'ок' in userMessage:
            #    vk.messages.edit(peer_id=2000000000 + event.chat_id, message='БЕЗ МАТА', message_id=event.obj['conversation_message_id'])
            #if 'ок' in userMessage:
            #    vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), attachment='photo')
            #dictTeams = {'общий сбор': CollectionTeamsClass.CollectionTeamsReminder(),
             #            'участники': CollectionTeamsClass.CollectionTeamsNames()}.get(userMessage)
            #print(userMessage)
            #print(userMessage)

            #attachments = []
            #posts = []
            #if userMessage == '!выйти':
            #CollectionTeamsClass.CollectionTeamsNames(userName)
            #elif userMessage == '!мем':  # Загружает и отправляет сообщения
            #    imageUrl = 'https://sun1-91.userapi.com/c543108/v543108093/67f8b/ASSnpqx1ak4.jpg'
            #    image = session.get(imageUrl, stream=True)
            #    photo = upload.photo_messages(photos=image.raw)[0]
            #    attachments.append(
            #        'photo{}_{}'.format(photo['owner_id'], photo['id'])
            #    )
            #    CollectionTeamsClass.CollectionTeamsOutput('МЕМ 2.0', ','.join(attachments))
            #elif userMessage == '!новости': # owner_id='',
            #    postToUserOrGroup = vkPost.wall.get(domain='', count='1')
            #    print(postToUserOrGroup)
            #    post = postToUserOrGroup['items']
            #    print(post)
            #    print(post[0]['owner_id'], post[0]['id'])
            #    posts.append(
            #        'wall{}_{}'.format(post[0]['owner_id'], post[0]['id'])
            #    )
            #    CollectionTeamsClass.CollectionTeamsOutput('Новость', ','.join(posts))
            #    print('ok')
                #vk.messages.send(user_id=event.user_id, attachment=, message='Пост')
            #  print(event)
            #print(event.obj['conversation_message_id'])
            #listMes = vk.messages.get(message_ids=event.obj['conversation_message_id'])
            #print(listMes)
            #  vk.messages.edit(peer_id=event.chat_id + 2000000000, message='Hello', message_id=event.object['conversation_message_id'])
                #print(CollectionTeamsClass.CollectionTeamsNames())

            #if dictTeams is not None and userName.lower() in listAllowedUsers:
            #    CollectionTeamsClass.CollectionTeamsOutput(dictTeams)


#if __name__ == '__main__':
#    Server(tokenBot, "187407860", "MISSiS")
