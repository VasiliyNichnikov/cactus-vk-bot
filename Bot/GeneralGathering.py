class GeneralGathering:
    def __init__(self, vk_api, chatId, isAdmin=False, parent=None):
        self.parent = parent
        self.vk_api = vk_api
        self.chatId = chatId
        # Данная команда будет работать, если пользователь администратор
        self.isAdmin = isAdmin

    def Command(self):
        print('Общий сбор запущен')
        listUsers = []
        arrayParticipants = self.vk_api.messages.getConversationMembers(peer_id=2000000000 + self.chatId)
        # Если данная перемнная == False, то бот пишет участников, иначе нет
        error = False
        for user in arrayParticipants['items']:
            if error:
                self.parent.SendMessage(self.chatId, "Только администраторы могут пользоваться данной командой :(")
                return
            try:
                user_id = user['member_id']
                if user_id >= 0 and self.isAdmin:
                    user_info = self.vk_api.users.get(user_ids=user_id, fields=['domain'])[0]
                    user_name = self.vk_api.users.get(user_ids=user_id)[0]['first_name']  # Имя пользователя
                    user_domain = '@' + user_info['domain'] + "(" + user_name + ")"
                    listUsers.append(user_domain)
                elif not self.isAdmin:
                    error = True
            except:
                self.parent.SendMessage(self.chatId, "УПС! Что-то пошло не так :(")
                error = True
        self.parent.SendMessage(self.chatId, ', '.join(listUsers))

    def CollectionTeamsNames(self, exitUser):  # выход из группы
        arrayParticipants = self.vkApi.messages.getConversationMembers(peer_id=2000000000 + self.chatId)
        for user in arrayParticipants['profiles']:
            userId = user['id']
            print(userId)
            try:
                userName = self.vkApi.users.get(user_ids=userId)[0]['first_name']
                if userName == exitUser:
                    try:
                        self.vkApi.messages.removeChatUser(chat_id=self.chatId, user_id=userId)
                    except:
                        self.CollectionTeamsOutput('БОТ НЕ МОЖЕТ ИСКЛЮЧАТЬ АДМИНИСТРАТОРОВ')
            except:
                pass