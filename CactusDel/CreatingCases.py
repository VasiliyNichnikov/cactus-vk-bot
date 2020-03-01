import datetime


# Данный класс создает дела
class CreateCaseOnDay:
    allCase = {}  # Словарь со всеми делами
    condition = "day"  # На каком этапе находится пользователь по созданию дела
    allStates = ["day", "name", "description", "timeStart", "timeEnd"]  # Список со всеми состояниями

    allStatesText = {"day": "Введите день:",
                     "name": "Введите название дела:",
                     "description": "Введите описание дела:",
                     "timeStart": "Введите время с которого начнете делать:",
                     "timeEnd": "Введите время, когда закончите делать:"
                     }  # Словарь, для вывода текста при опросе пользователя
    allStatesTextEnd = {
        "day": "День:",
        "name": "Название:",
        "description": "Описание:",
        "timeStart": "Начало:",
        "timeEnd": "Завершение:"
    }  # Словарь, для вывода текста при выводе информации пользователю

    caseWork = None  # Дело, которое сейчас создается

    def __init__(self, parent):
        self.parent = parent

    # Запускается функция создания создания дела
    def Start_func(self):
        self.parent.classSendMessage.SendMessage("Создание дела началось!")
        self.parent.classSendMessage.SendMessage(self.allStatesText[self.condition])

    # Вся информация передается сюда
    def Work(self, messageUser):
        if self.caseWork is None:
            self.caseWork = NewCase()
        if self.condition == "day" and messageUser != "пропустить":
            self.caseWork.dictInfo[self.condition] = messageUser
        elif self.condition == "description" and messageUser != "пропустить":
            self.caseWork.dictInfo[self.condition] = messageUser
        elif self.condition != "day" and self.condition != "description":
            self.caseWork.dictInfo[self.condition] = messageUser
        self.NextStep()

    def CaseEnd(self):
        listRes = []  # Список, который потом отправим пользователю
        for info in self.caseWork.dictInfo:
            line = self.allStatesTextEnd[info] + " " + self.caseWork.dictInfo[info]
            listRes.append(line)
        self.parent.classSendMessage.SendMessage("\n".join(listRes))

    def NextStep(self):
        step = 0
        for i in range(len(self.allStates)):
            if self.allStates[i] == self.condition:
                step = i
                break
        if step + 1 < len(self.allStates):
            step += 1
            self.condition = self.allStates[step]
            # Вывод текста для пользователя
            self.parent.classSendMessage.SendMessage(self.allStatesText[self.condition])
        elif step + 1 >= len(self.allStates):
            self.parent.classSendMessage.SendMessage("Вы создали дело!")
            self.CaseEnd()


class NewCase:
    def __init__(self):
        # Инициализация переменных
        self.dateNow = datetime.datetime.now()  # День, сегодня (По умолчанию)
        self.name = ""  # Название дела (Обязательное поле)
        self.description = ""  # Описание дела (Не обязательное поле)
        self.timeStart = "00-00-00"  # Вреям начала дела
        self.timeEnd = "00-00-00"  # Время конца дела
        self.dictInfo = {"day": self.dateNow.strftime("%d.%m.%Y"),
                         "name": self.name,
                         "description": self.description,
                         "timeStart": self.timeStart,
                         "timeEnd": self.timeEnd}  # Словарь, где находится вся информация о блоке
        print(self.dateNow.strftime("%d"))

    # Возвращает словарь с информацией блока
    def ReturnDictInfo(self):
        return self.dictInfo
