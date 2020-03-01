

class EditMessage:
    def __init__(self, vk_api, chat_id, message, parent=None):
        self.parent = parent
        self.vk_api = vk_api
        self.chat_id = chat_id
        self.message = message

    # Основная функция
    def Command(self):
        print(self.vk_api.messages.getHistory(peer_id=self.message['peer_id'], count=1))
        #self.vk_api.messages.getHistory(offset=0, count=1, user_id=self.user_id, peer_id=self.chat_id)
        #print(self.message)
        #infoMessage = self.vk_api.messages.getById(message_ids=self.message['conversation_message_id'])
        #print(infoMessage)
        #print(self.chat_id)
        #print(self.message)
        #self.vk_api.messages.edit(peer_id=self.message['peer_id'], message='test',
        #                          message_id=self.message['id'])
