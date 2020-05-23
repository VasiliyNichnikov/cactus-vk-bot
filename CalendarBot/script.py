import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from CalendarBot.database import WorkingDataBase
from vk_api.utils import get_random_id
from CalendarBot.create_event import CreateEvent
from CalendarBot.working_google_calendar import WorkingGoogleCalendarAPI

'''
/start - включение бота, бот активируется и приветствует пользователя.  
/create_event - создает напоминание в календаре. Для этого нужно указать название напоминания, 
цвет напоминания и время проведения напоминания.
'''


class Server(WorkingDataBase):
    list_all_events = []

    dict_errors = {
        'error_teams_not_found': 'Ошибка! Такой команды нет! Убедитесь, что вы ввели все правильно!'
    }

    # CalendarBot/Users.sqlite
    def __init__(self, api_token, group_id, server_name, path_database):
        super().__init__(path_database)
        self.reset_selected_function()
        self.path_database = path_database
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.class_google_api = WorkingGoogleCalendarAPI()
        # Все команды, которые имеет бот
        self.dict_teams = {'/start': {'function': self.start_bot},
                           '/create_event': {'function': self.create_event}
                           }
        print('Бот Живой!')

    # Отправка сообщений
    def send_msg(self, send_id, message, attachment=None):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(), attachment=attachment)

    # Приветсие
    def start_bot(self, *args):
        send_id = int(args[0]['user_id'])
        self.send_msg(send_id, 'Приветствую! '
                      'Я умею создавать напоминания в google календарь. '
                      'Чтобы создать напоминание, введите /create_event. ')

    # Получает класс, который сейчас используется для создания напоминания
    def get_class(self, send_id):
        for event in self.list_all_events:
            if event.user_id == send_id:
                if event.check_stage_end():
                    self.delete_event(event)
                    return None
                return event
        return None

    # Удаление класса из списка, когда напоминание создано
    def delete_event(self, event):
        for i in range(len(self.list_all_events)):
            if self.list_all_events[i] == event:
                self.update_selected_function(event.user_id, 'null')
                print("change")
                del self.list_all_events[i]
                break

    def check_delete(self, send_id):
        for event in self.list_all_events:
            if event.user_id == send_id:
                if event.check_stage_end():
                    self.delete_event(event)

    # Проверка, есть ли созданное напоминание в списке
    def check_create_event(self, send_id):
        for event in self.list_all_events:
            if event.user_id == send_id:
                if event.check_stage_end():
                    self.delete_event(event)
                    return True
                return False
        return True

    # Начинает создавать напоминание
    def create_event(self, *args):
        send_id = int(args[0]['user_id'])
        user_msg = args[1]
        self.class_google_api.manual_init_user(send_id)
        if self.check_create_event(send_id):
            self.update_selected_function(send_id, 'create_event')
            new_event = CreateEvent(send_id, self.vk_api, self.class_google_api)
            self.list_all_events.append(new_event)
        else:
            class_create_event = self.get_class(send_id)
            if class_create_event is not None:
                class_create_event.creating_reminder(user_msg)
                self.check_delete(send_id)

    # Возвращает команду, которая выполняется у пользователя
    def get_command_user(self, user_msg):
        for word in user_msg.split():
            if word in self.dict_teams.keys():
                try:
                    return self.dict_teams[word]
                except TypeError as e:
                    return None
        return None

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id = event.object.message['from_id']
                user_message = str(event.object.message['text']).lower()
                # Проверяем, есть ли пользователь в БД
                if not self.get_user(peer_id):
                    self.add_user(peer_id)

                info_user = self.get_user(peer_id)
                if self.get_command_user(user_message) is not None:
                    self.get_command_user(user_message)['function'](info_user, user_message)
                elif info_user is not None and info_user['selected_function'] == 'create_event':
                    self.create_event(info_user, user_message)
                else:
                    self.send_msg(peer_id, 'Простите, я вас не понимаю. Введите /create_event, '
                                           'чтобы начать создавать напоминания в google календаре.')

