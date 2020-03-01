import datetime
import time


class Reminder:
    dictMonths = {
        "январь": 1,
        "февраль": 2,
        "март": 3,
        "апрель": 4,
        "май": 5,
        "июнь": 6,
        "июль": 7,
        "август": 8,
        "сентябрь": 9,
        "октябрь": 10,
        "ноябрь": 11,
        "декабрь": 12
    }

    def __init__(self, vk_api, chatId, parent=None):
        self.parent = parent
        self.vk_api = vk_api
        self.chatId = chatId

    def Command(self):
        #self.parent.SendMessage(self.chatId, "Все действия происходят в консоли) (ТЕСТИРОВАНИЕ)")
        print('Создание напоминания. Напишите, когда хотите, чтобы бот вам напомнил в таком формате (время день). '
              'Например: 2:30 25 ноября. Бот к вам прикреплен!')
        dateTime = input().split()  # Время и дата напоминия
        hours = dateTime[0].split(':')[0]
        minutes = dateTime[0].split(':')[-1]
        day = dateTime[1]
        month = self.dictMonths[dateTime[-1].lower()]

        print('Hours:', hours, 'Minutes:', minutes, 'Day:', day, 'Month:', month)
        deadLine = datetime.datetime(datetime.datetime.now().year, month, int(day), int(hours), int(minutes), 0)
        print(deadLine)
        print('Хорошо, теперь введите напоминание')
        reminder = input()

        print('Все данные введены. Бот напомнит вам', reminder, "в", dateTime)
        print("ADD REMINDER")

        while True:
            nowDate = datetime.datetime.now()
            if nowDate >= deadLine:
                self.parent.SendMessage(self.chatId, f"Напоминание: {reminder}")
                break
