#  from Bot.BotCactus import Server
#  from CactusDel.MainScript import Server
from BotTeacher.Main import Server

# токен вк api
vk_api_token = "4f22434cd699dd0209b3c5e60f9d5aac529c9364f88da3a3c4d4b7b6c2251f7cecc4f0836a5b59788317e"
# Токен пользователя
user_token = '73c46d213cebd5794a7dfc5471a792bc670b0be4c7452191f25bfdd094b70a78b620994d19e001d883688'
# Токен приложения
app_token = '3cd9d1bedb7358529b317062d172112e43c81afa025349c82b33382310535f38c79ca58499718324f7ce2'

if __name__ == '__main__':
    serverBotTeacher = Server(vk_api_token, app_token, 187407860, 'Bot Teacher')
    #  serverCactusDel = Server(vk_api_token, app_token, 187407860, 'Cactus Bot')
    #  serverMISSiS.ObtainingInformation()
