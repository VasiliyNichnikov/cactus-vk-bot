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

        weatherMainInfo = receivedInfo.find('div', class_='card_size_big')
        #  print(weatherOnTenDays)

        print(weatherMainInfo.prettify())
        # Температура сейчас
        condition = weatherMainInfo.find('div', class_='link__condition day-anchor i-bem').text  # Состояние погоды
        temperature = weatherMainInfo.find('div', class_='temp fact__temp fact__temp_size_s').text
        feels = weatherMainInfo.find('div', class_='term term_orient_h fact__feels-like').text  # Как ощущается
        windSpeed = weatherMainInfo.find('span', 'wind-speed').text  # Скорость ветра
        humidity = weatherMainInfo.find('div', 'term term_orient_v fact__humidity').text  # Влажность
        pressure = weatherMainInfo.find('div', 'term term_orient_v fact__pressure').text  # Давление

        resLine = 'Температура: {}°.\n' \
                  '{} \n ' \
                  'Состояние погоды: {} \n' \
                  'Ветер: {}м/с.\n' \
                  'Влажность: {}.\n' \
                  'Давление: {}\n' \
                  'Информация взята с сервиса Яндекс (Яндекс Погода). \n' \
                  'Данная функция пока определяет погоду только в Москве :('.format(temperature, feels, condition,
                                                                                    windSpeed, humidity, pressure)
        self.parent.SendMessage(self.chatId, resLine)
