#  from Bot.BotCactus import Server
#  from CactusDel.MainScript import Server
from KateBot.main import Server

# токен вк api
vk_api_token = "5d657387b5ddbb3c3f735546ae27d2aac9ddfa50b20a6619c197c803e0fcdefc8608c5c1a6d25ead07a60"
# Токен пользователя
user_token = '73c46d213cebd5794a7dfc5471a792bc670b0be4c7452191f25bfdd094b70a78b620994d19e001d883688'
# Токен приложения
app_token = "d20982366e78b639274c82289794f835b5ac469e8001e2c7e5667e5ed673d1262d6582a983f1fd99b49e5"


if __name__ == '__main__':
    server_kate_bot = Server(vk_api_token, app_token, 187407860, 'Kate Bot')
    server_kate_bot.start()
    #  serverBotTeacher = Server(vk_api_token, app_token, 187407860, 'Bot Teacher')
    #  serverCactusDel = Server(vk_api_token, app_token, 187407860, 'Cactus Bot')
    #  serverMISSiS.ObtainingInformation()
