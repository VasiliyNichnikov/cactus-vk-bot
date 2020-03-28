#  from Bot.BotCactus import Server
#  from CactusDel.MainScript import Server
from KateBot.data import db_session
from KateBot.Main import Server

# токен вк api
vk_api_token = "5d657387b5ddbb3c3f735546ae27d2aac9ddfa50b20a6619c197c803e0fcdefc8608c5c1a6d25ead07a60"
# Токен пользователя
user_token = '73c46d213cebd5794a7dfc5471a792bc670b0be4c7452191f25bfdd094b70a78b620994d19e001d883688'
# Токен приложения
app_token = '3cd9d1bedb7358529b317062d172112e43c81afa025349c82b33382310535f38c79ca58499718324f7ce2'


if __name__ == '__main__':
    db_session.global_init("KateBot/db/users.sqlite")
    server_kate_bot = Server(vk_api_token, app_token, 187407860,  db_session, 'Kate Bot')
    server_kate_bot.start()
    #  serverBotTeacher = Server(vk_api_token, app_token, 187407860, 'Bot Teacher')
    #  serverCactusDel = Server(vk_api_token, app_token, 187407860, 'Cactus Bot')
    #  serverMISSiS.ObtainingInformation()
