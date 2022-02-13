from pycqBot.socketApp import cqSocket, cqLog
from pycqBot.cqApi import cqHttpApi, cqBot
from pycqBot.cqCode import at, image, music


# log mod
cqLog()

cq_api = cqHttpApi()
bot_obj = cqBot(cq_api, group_id_list=[
        685735591
    ],
    command={

    }
)

cqc = cqSocket(bot_obj)

input("")