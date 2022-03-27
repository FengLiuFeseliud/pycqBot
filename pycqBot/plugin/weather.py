import json
import logging
from pycqBot.object import Plugin, Message
from pycqBot.cqApi import cqBot, cqHttpApi

class weather(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)

        self.bot.command(self.weather, "天气", {
            "type": "all"
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
            logging.error("天气 error: %s" % err)
            logging.exception(err)

    def weather(self, commandData, message: Message):
        self.cqapi.add_task(self._weather(commandData[0], message))