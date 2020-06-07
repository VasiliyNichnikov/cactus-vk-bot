import calendar
import datetime
from requests import post


class ErrorCreateEvents(Exception):
    pass


class ErrorNameEvent(ErrorCreateEvents):
    pass


class ErrorDescriptionEvent(ErrorCreateEvents):
    pass


class ErrorColorEvent(ErrorCreateEvents):
    pass


class ErrorDayMonthYear(ErrorCreateEvents):
    pass


class ErrorTimeEvent(ErrorCreateEvents):
    pass


# Возвращает день и месяц сегоднейшего дня
def get_day_month(day, month):
    _day = ''
    _month = ''
    if day < 10:
        _day = f'0{day}'
    if month < 10:
        _month = f'0{month}'
    return f'{_day}.{_month}'


class CreateEvent:
    # Словарь с вариантами ответов
    dict_create_events = {
        'name_event': 'Начнем создавать напоминание. Для начала введите название напоминания.',
        'description_event': 'Напишите описание напоминания. '
                             'Это не обязательно. '
                             'Вы можете написать - и тогда бот пропустит описание.',
        'color_event': 'Введите цвет, который хотите видеть у напоминания. (По умолчанию: 0)',
        'day_month_year_event': 'Введите день, в который нужно создать напоминание. день месяц.год. '
                                f'Например: {get_day_month(datetime.datetime.now().day, datetime.datetime.now().month)}'
                                f'.{datetime.datetime.now().year} '
                                '(По умолчанию: сегодня)',
        'time_event': 'Введите время начала и конца напоминания. (Пример: 10:00-11:00)',
        'ready': 'Поздравляю, вы создали напоминание!'
    }

    def __init__(self, user_id, parent):
        self.user_id = user_id
        self.parent = parent

        self.name_event = ''
        self.description_event = '',
        self.color_event = ''
        self.day_month_year_event = ''
        self.time_event = ''

        self.stage = list(self.dict_create_events.keys())[0]

        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['name_event'],
                             attachment=self.parent.load_image('creating_reminder.png'))

        self.dict_phase_functions = {
            'name_event': self.function_name_event,
            'description_event': self.function_description_event,
            'color_event': self.function_color_event,
            'day_month_year_event': self.function_day_month_year_event,
            'time_event': self.function_time_event
        }

    def creating_reminder(self, user_msg):
        try:
            self.dict_phase_functions[self.stage](user_msg)
            self.next_stage()
        except ErrorCreateEvents as error:
            self.parent.send_msg(send_id=self.user_id, message=error)

    def function_name_event(self, user_msg):
        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['description_event'])
        self.name_event = user_msg

    def function_description_event(self, user_msg):
        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['color_event'])
        self.description_event = user_msg
        if self.description_event == '-':
            print('Описания нет.')
            self.description_event = ''

    def function_color_event(self, user_msg):
        self.color_event = user_msg
        if user_msg != '-':
            try:
                if 0 < int(self.color_event) and int(self.color_event) >= 9:
                    raise ErrorColorEvent('Ошибка. Данного id нет в списке.')
            except ValueError as e:
                raise ErrorColorEvent('Ошибка. Вы можете использовать только цифры. От 0 до 9 включительно.')
        else:
            self.color_event = '0'
        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['day_month_year_event'])

    def function_day_month_year_event(self, user_msg):
        self.day_month_year_event = user_msg
        if self.day_month_year_event != '-':
            try:
                day, month, year = self.day_month_year_event.split('.')
                if len(day) > 2 or len(month) > 2 or len(year) > 4:
                    raise ErrorDayMonthYear('Ошибка. Вы ввели неправильный день или месяц или год. (1)')
                elif int(month) > 12:
                    raise ErrorDayMonthYear('Вы ввели месяц больше 12.')
                elif int(day) > calendar.monthrange(int(year), int(month))[1]:
                    raise ErrorDayMonthYear('Вы ввели неверное кол-во дней в месяце.')
            except ValueError as e:
                raise ErrorDayMonthYear('Ошибка. Вы ввели неправильный день или месяц или год. (2)')
        else:
            self.day_month_year_event = f'{datetime.datetime.now().day}.{datetime.datetime.now().month}.' \
                                        f'{datetime.datetime.now().year}'
        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['time_event'])

    def function_time_event(self, user_msg):
        self.time_event = user_msg
        try:
            time_start, time_end = self.time_event.split('-')
            time_start_hours, time_start_minutes = time_start.split(':')
            time_end_hours, time_end_minutes = time_end.split(':')
            if int(time_start_hours) > 24 or int(time_end_hours) > 24 or int(time_start_hours) < 0 \
                    or int(time_end_hours) < 0:
                raise ErrorTimeEvent('Ошибка. Вы ввели неверные часы. Убедитесь, что время от 0 до 24.')
            if int(time_start_minutes) > 60 or int(time_end_minutes) > 60 or int(time_start_minutes) < 0 \
                    or int(time_end_minutes) < 0:
                raise ErrorTimeEvent('Ошибка. Вы ввели неверные минуты. Убедитесь, что время от 0 до 60.')
            if int(time_start_hours) == int(time_end_hours) and int(time_start_minutes) == int(time_end_minutes):
                raise ErrorTimeEvent('Ошибка. Время начала и конца не может быть одинакова.')
        except ValueError as e:
            raise ErrorTimeEvent('Ошибка. Вы ввели неверное время.')
        self.parent.send_msg(send_id=self.user_id, message=self.dict_create_events['ready'],
                             attachment=self.parent.load_image('created_reminder.png'))
        self.create_event_google_api()

    def next_stage(self):
        list_keys_dict = list(self.dict_create_events.keys())
        for stage_number in range(len(list_keys_dict)):
            if list_keys_dict[stage_number] == self.stage and stage_number + 1 < \
                    len(self.dict_create_events.keys()):
                self.stage = list_keys_dict[stage_number + 1]
                break
            elif stage_number + 1 >= len(list_keys_dict):
                self.stage = list_keys_dict[0]

    def check_stage_end(self):
        if self.stage == list(self.dict_create_events.keys())[-1]:
            return True
        return False

    def create_event_google_api(self):
        result = post('https://web-site-google-calendar.herokuapp.com/create_event',
                      json={'user_id': self.user_id,
                            'name_event': self.name_event,
                            'description_event': self.description_event,
                            'color_event': self.color_event,
                            'day_month_year_event': self.day_month_year_event,
                            'time_event': self.time_event})
        print(result.text)


