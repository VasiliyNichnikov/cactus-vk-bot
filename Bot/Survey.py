from vk_api.utils import get_random_id
import json


class Survey:
    questions = {'question_survey': 'Введите вопрос опроса.',
                 'answer_choice': 'Введите варианты ответов через запятую.'}

    description = 'Вы выбрали создание опроса. Бот прикреплен к вам, чтобы открепить бота, напишите !выход. ' \
                  'Сейчас бот будет просить данные, чтобы создать опрос.'
    course_events = 'question_survey'

    # переменные для опроса
    question = ''
    answers = []

    def __init__(self, userId, vkUser, vkApi, chatId, group_id):
        self.group_id = group_id
        self.vkUser = vkUser
        self.userId = userId
        self.vkApi = vkApi
        self.chatId = chatId

        self.SendMessage(self.description)
        self.SendMessage(self.questions[self.course_events])

    def SendMessage(self, message, file=None):
        self.vkApi.messages.send(chat_id=self.chatId, random_id=get_random_id(), message=message, attachment=file)

    def AcceptMessage(self, message):
        if self.course_events == 'answer_choice':
            self.AddAnswersList(message)
        elif self.course_events == 'question_survey':
            self.AddQuestions(message)

    # Добавляет вопросы к опросу
    def AddAnswersList(self, answers):
        print('Add Answer')
        self.answers = answers.split(',')
        self.course_events = 'exit'
        self.SendMessage('Все данные введены')
        self.CreatePoll()

    # Добавляет вопрос
    def AddQuestions(self, question):
        print('Add Question')
        self.question = question
        self.course_events = 'answer_choice'
        self.SendMessage(self.questions[self.course_events])

    def CreatePoll(self):
        jsonAnswers = {}  # Собираем все данные, которые ввел пользователь
        polls = []  # Опрос
        for i in range(len(self.answers)):
            jsonAnswers['{}'.format(i)] = self.answers[i]
        poll = self.vkUser.polls.create(question=self.question, owner_id=str('-' + str(self.group_id)),
                                        add_answers=json.dumps(jsonAnswers))
        polls.append('poll{}_{}'.format(poll['owner_id'], poll['id']))
        self.SendMessage('Опрос готов, пользователь откреплен', polls)

    def CheckPoll(self):
        if self.course_events == 'exit':
            self.course_events = 'question_survey'
            return True
        return False
