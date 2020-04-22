import vk_api.vk_api
import json
import time
import concurrent.futures
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
import threading
import requests
from requests import post, get


class Server:
    dict_phrase_bot = {
        '/start': 'Я рад, что ты решил воспользоваться моим сервисом.' 
                  'Прежде чем начать, активируй меня. Для этого перейди на сайт "(ссылка на сайт)".' 
                  'На сайте зайди в параметры -> информация и скопируй ключ. Этот ключ нужно указать в команде /key <ваш ключ>.' 
                  'Если что-то не понятно, вот видео - "(ссылка на видео)"',
        'error_command_not_found': 'Я вас не понимаю, убедитесь, что вы ввели все правильно.'
                                   'Если хотите узнать, какие команды, я знаю наберить "/all_commands".',
        'error_not_found_key': 'Упс! Что-то пошло не так.'
                               'Проверьте правильность введенной команды и ключа. (Подсказка команды: /key <ваш ключ>)',
        'error_key_activated': 'Ключ уже активирован! Введите команду "/all_commands", чтобы узнать все доступные команды.',
        'success_key_active': 'Ура! Ключ активирован! Кол-во команд обновлено! Чтобы узнать все доступные команды введите "/all_commands".',
        'error_access': 'Отказано в доступе! Активируйте ключ. Для этого используйте команду "/key <ваш ключ>".',
        'all_commands': 'Команды, которые доступны для использования:\n'
                        '/start_program <имя программы>\n'
                        '/start_scenario <имя сценария>\n'
                        '/exit - отключение бота от сервера\n'
                        '/all_programs - узнать все программу, которые есть на сайте'
                        '/all_scenarios - узнать все сценарии, которые есть на сайте'
                        '/function <один из параметров>\n'
                        '------------------------------\n'
                        'Параметры для /function:\n'
                        'shutdown - выключение компьютера\n'
                        'reboot - перезагрузка компьютера\n'
                        'sleep_mode - спящий режим\n',
        'user_not_found': 'Ошибка! Пользователь не найден! Проверьте правильность команды.',
        'program_not_found': 'Ошибка! Программа не найдена!'
                             ' Убедитесь, что вы ввели правильное имя программы!' 
                             ' Чтобы посмотреть все программы, наберите команду "/all_programs".',
        'path_program_change_success': 'Запрос выполнен успешно!',
        'name_scenario_change_success': 'Запрос выполнен успешно!',
        'name_function_change_success': 'Запрос выполнен успешно!',
        'programs_not_found': 'Ошибка! Программы не найдены.'
                              'Убедитесь, что вы создали программу на сайте.' 
                              'Посмотрите видео, если есть проблемы с созданием программ ("ссылка на видео")',
        'function_not_found': 'Данная функция не найдена! Убедитесь, что вы ввели команду верно.',
        'function_lock': 'Данная функция заблокирована! Перейдите на сайт, чтобы разрешить использовать ее.',
        'scenario_not_found': 'Сценарий не найден! Убедитесь, что такой сценарий есть. Чтобы посмотреть все сценарии, введите команду "/all_scenarios"',
        'scenarios_not_found': 'Ошибка! Сценарии не найдены.Убедитесь, что вы создали сценарий на сайте.Посмотрите видео, если есть проблемы с созданием сценария("ссылка на видео")',
        'exit_bot_success': 'Бот успешно отключен от сервера.'
    }

    def __init__(self, api_token, app_token, group_id, server_name="None"):
        # Имя сервера
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Активация ключа приложения
        self.app = vk_api.VkApi(token=app_token)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()
        # Получение api приложения
        self.app_api = self.app.get_api()
        # id группы
        self.group_id = group_id

        # Команды, которые поддерживает бот
        self.list_commands = ['/start',
                              '/key',
                              '/all_commands',
                              '/start_program',
                              '/all_programs',
                              '/start_scenario',
                              '/all_scenarios',
                              '/exit',
                              '/function']

        print("Бот живой!")

    # Отправка сообщений
    def send_msg(self, send_id, message, attachment=None):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(), attachment=attachment)

    # Запуск сервера
    def start(self):
        for event in self.long_poll.listen():
            # Новое сообщение от пользователя
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_message = str(event.object.message['text'])
                peer_id = int(event.object.message['from_id'])
                # Проверка, если команда, которую написал пользователь среди всех команд
                if self.get_command(user_message) is not None:
                    command, information = self.get_command(user_message)
                    start_command = {
                        '/start': self.start_command,
                        '/key': self.activating_bot,
                        '/all_commands': self.get_all_commands,
                        '/start_program': self.start_select_program,
                        '/start_scenario': self.change_select_name_scenario,
                        '/all_programs': self.get_user_programs,
                        '/all_scenarios': self.get_user_scenarios,
                        '/exit': self.exit_user_bd,
                        '/function': self.change_function_pc
                    }.get(command)(information, peer_id)
                elif self.get_command(user_message) is None:
                    self.conclusion_error_user_command('error_command_not_found', peer_id)

    # Получение команды, которую ввел пользователь
    def get_command(self, user_message):
        for i in self.list_commands:
            if i in user_message:
                list_user_message = user_message.split()
                command = list_user_message[0]
                information = list_user_message[-1]
                return command, information
        return None

    # Команда старта, которая запускает бота
    def start_command(self, informaion, peer_id):
        self.send_msg(peer_id, self.dict_phrase_bot['/start'])

    # Функция, который выводит ошибку и говорит, что не понимает пользователя
    def conclusion_error_user_command(self, name_error, peer_id):
        self.send_msg(peer_id, self.dict_phrase_bot[name_error])

    # Функция, отправляет все команды, которые может использовать пользователь
    def get_all_commands(self, informaion, peer_id):
        if self.check_user_key(peer_id):
            self.send_msg(peer_id, self.dict_phrase_bot['all_commands'])
        else:
            self.conclusion_error_user_command('error_access', peer_id)

    # Функция, которая активирует бота и открывает возможность управлять ботом 
    def activating_bot(self, key, peer_id):
        information_json = {'key_user': key, 'id_user_vk': peer_id}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            request_server = executor.submit(self.request_server, 'add_key_bot', information_json)
            value = request_server.result()
            
            result = json.loads(value.text)
            if 'error' in result:
                self.conclusion_error_user_command(result['error'], peer_id)
            elif 'success' in result:
                self.send_msg(peer_id, self.dict_phrase_bot['success_key_active'])
    
    # Функция, которая проверяет, есть ли ключ у игрока или нет
    def check_user_key(self, peer_id):
        information_json = {'id_user_vk': peer_id}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            request_server = executor.submit(self.request_server, 'check_key_user', information_json)
            value = request_server.result()

            if "Error" in value:
                return False

            result = json.loads(value.text)
            if 'error' in result:
                return False
            elif 'key_user' in result:
                return result['key_user']

    # Функция, которая меняет путь к программе у пользователя
    def start_select_program(self, program, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'key_user': key, 'name_program': program}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'change_path_program', information_json)
                value = request_server.result()

                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    self.send_msg(peer_id, self.dict_phrase_bot['path_program_change_success'])
        else:
            self.conclusion_error_user_command('error_access', peer_id)
    
    # Передает параметр в функцию ПК
    def change_function_pc(self, function, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'key_user': key, 'function': function}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'change_pc_function', information_json)
                value = request_server.result()

                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    self.send_msg(peer_id, self.dict_phrase_bot['path_program_change_success'])
        else:
            self.conclusion_error_user_command('error_access', peer_id)

    # Функция, которая меняет сценарий у пользователя
    def change_select_name_scenario(self, name_scenario, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'key_user': key, 'name_scenario': name_scenario}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'change_name_scenario', information_json)
                value = request_server.result()

                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    self.send_msg(peer_id, self.dict_phrase_bot['name_scenario_change_success'])
        else:
            self.conclusion_error_user_command('error_access', peer_id)
        
    # Функция отправляет пользователю все программы, которые он имеет
    def get_user_programs(self, program, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'id_user_vk': peer_id}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'get_all_programs_user', information_json)
                value = request_server.result()

                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    message = f'Программы, которые у вас есть на сайте: {" ".join(result["success"])}'
                    self.send_msg(peer_id, message)
        else:
            self.conclusion_error_user_command('error_access', peer_id)
    
    # Функция, отключает бота от БД
    def exit_user_bd(self, informaion, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'key_user': key}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'exit_key_bot', information_json)
                value = request_server.result()
                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    self.send_msg(peer_id, self.dict_phrase_bot[result['success']])
        else:
            self.conclusion_error_user_command('error_access', peer_id)

    # Функция, которая возвращает все сценарии
    def get_user_scenarios(self, scenario, peer_id):
        key = self.check_user_key(peer_id)
        if key is not False:
            information_json = {'id_user_vk': peer_id}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                request_server = executor.submit(self.request_server, 'get_all_scenarios_user', information_json)
                value = request_server.result()
                print(value)
                result = json.loads(value.text)
                if 'error' in result:
                    self.conclusion_error_user_command(result['error'], peer_id)
                else:
                    message = f'Сценарии, которые у вас есть на сайте: {" ".join(result["success"])}'
                    self.send_msg(peer_id, message)
        else:
            self.conclusion_error_user_command('error_access', peer_id)

    # Отправляет запрос на сервер и возвращает ответ
    def request_server(self, place, information_json):
        while True:
            try:
                request = post(f'https://website-computer-manager.herokuapp.com/{place}', json=information_json)
                if request.status_code != 200:
                    print("Ошибка. Код ответа: %s", request.status)
                    time.sleep(1)
                    continue
                return request
            except requests.RequestException:
                print("Ошибка. Не удается подключиться к серверу.")
                return "Error"
            except requests.ConnectionError:
                print("Ошибка. Не удается подключиться к серверу.")
                return "Error"
