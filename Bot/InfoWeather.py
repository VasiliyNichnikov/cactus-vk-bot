import bs4
import requests


class InfoWeather:
    def __init__(self, vk_api, chatId, parent=None):
        self.parent = parent
        self.vk_api = vk_api
        self.chatId = chatId

    # Смотрим температуру на сайте и отправляем сообщением
    def Command(self, city="москва"):
        # Берем информацию из Яндекс Погода (Пока только для москвы)
        request = requests.get("https://yandex.ru/pogoda/moscow")
        receivedInfo = bs4.BeautifulSoup(request.text, "html.parser")

        weatherOnTenDays = receivedInfo.find_all('div', class_='card_size_big')
        #  print(weatherOnTenDays)
        time = weatherOnTenDays[0].find('time', class_='fact__time').text
        temperature = weatherOnTenDays[0].find('span', class_='temp__value').text
        resLine = '{} \nТемпература: {}°.\nИнформация взята с сервиса Яндекс (Яндекс Погода).' \
                  '\nДанная функция пока определяет погоду только в Москве :('.format(time, temperature)
        self.parent.SendMessage(self.chatId, resLine)



