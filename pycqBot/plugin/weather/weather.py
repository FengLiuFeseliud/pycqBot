import json
from pycqBot.cqLogger import cqlogger
from pycqBot.object import Plugin
from pycqBot.cqHttpApi import cqBot, cqHttpApi
from pycqBot.data import *


class weather(Plugin):
    """
    天气查询
    """

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)

        self.bot.command(self.weather, "天气", {
            "help": [
                "#天气 - 查询指定城市天气",
                "   格式: 天气 [城市]"
            ]
        })

    async def _weather(self, city, message: Message):
        try:
            api = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % city
            data = json.loads(await self.cqapi.link(api, json=False))
            if data["status"] != 1000:
                message_data = "天气 api error: %s" % data
            else:
                ganmao = data["data"]["ganmao"]
                data = data["data"]["forecast"][0]
                fengli = data["fengli"].lstrip("<![CDATA[").rstrip("]]>")
                message_data = "%s%s %s %s %s %s%s\n%s" % (city, data["date"],
                                                           data["high"],
                                                           data["low"],
                                                           data["type"],
                                                           data["fengxiang"],
                                                           fengli,
                                                           ganmao
                                                           )

            print(message_data)
            message.reply(message_data)
        except Exception as err:
            cqlogger.error("天气 error: %s" % err)
            cqlogger.exception(err)

    def weather(self, commandData, message: Message):
        self.cqapi.add_task(self._weather(commandData[0], message))
