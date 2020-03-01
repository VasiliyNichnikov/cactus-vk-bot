class EGE:
    greeting = "Выбери предмет, к которому ты хочешь готовиться."

    def __init__(self, parent):
        self.parent = parent
        #parent.ChangeKeyboard("C:/Users/vnich/YandexDisk/Bot_VK/keyboards/keyboardEGE.json")


    def GreetingText(self):
        return self.greeting

    def Mathematics(self):
        return "Хорошо, какой номер?"
