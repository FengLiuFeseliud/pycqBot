from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class test(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)

        self.command_load()

    def command_load(self):
        self.bot.command(self.echo, "echo", {
            "type": "all"
        })

        self.bot.command(self.codestr, "codestr", {
            "type": "all"
        })

        self.bot.command(self.code, "code", {
            "type": "all"
        })
    
    def echo(self, commandData, message: Message):
        message.reply(" ".join(commandData))
    
    def codestr(self, commandData, message: Message):
        message.reply(message.code_str)

    def code(self, commandData, message: Message):
        message.reply("code len: %s code: %s" % (len(message.code), message.code))
