import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from BotCalendar.database import WorkingDataBase
from vk_api.utils import get_random_id
from BotCalendar.create_event import CreateEvent

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
    def __init__(self, api_token, group_id, server_name):
        super().__init__()
        #  self.reset_selected_function()
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        # self.class_google_api = WorkingGoogleCalendarAPI()
        # Все команды, которые имеет бот
        self.dict_teams = {'/start': {'function': self.start_bot},
                           '/create_event': {'function': self.create_event}
                           }
        print('Бот Живой!')

    # Отправка сообщений
    def send_msg(self, send_id, message, attachment=None):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(), attachment=attachment)

    #  Загрузка изображения
    def load_image(self, name_image):
        upload = vk_api.VkUpload(self.vk)
        photo = upload.photo_messages(f'BotCalendar/images/{name_image}')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        print("Изображение создано")
        return attachment

    # Приветствие
    def start_bot(self, *args):
        send_id = int(args[0]['user_id'])
        self.send_msg(send_id, 'Приветствую! '
                      'Я умею создавать напоминания в google календарь. '
                      'Но перед тем как начать, нужно авторизоваться, для этого перейдтите на этот сайт - '
                      f'https://web-site-google-calendar.herokuapp.com/{send_id} \n'
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
        if self.check_create_event(send_id):
            self.update_selected_function(send_id, 'create_event')
            new_event = CreateEvent(send_id, self)
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

    # Функция, которая принимает сообщения пользователя
    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id = event.object.message['from_id']
                user_message = str(event.object.message['text']).lower()
                info_user = self.get_user(peer_id)
                # Проверяем, есть ли пользователь в БД
                if not info_user:
                    self.add_user(peer_id)
                if self.get_command_user(user_message) is not None:
                    self.get_command_user(user_message)['function'](info_user, user_message)
                elif info_user is not None and info_user['selected_function'] == 'create_event':
                    self.create_event(info_user, user_message)
                else:
                    self.send_msg(peer_id, 'Простите, я вас не понимаю. Введите /create_event, '
                                           'чтобы начать создавать напоминания в google календаре.')


