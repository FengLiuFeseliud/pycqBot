import logging
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class manage(Plugin):
    """
    群管理插件

    插件配置
    ---------------------------
    
    banText: 屏蔽词列表
    banTextReply: 触发屏蔽词回复 {name} 用户名占位 默认 "{name} 不可以乱说话哦"
    groupRequestAll: 群邀请机制 False 保存群邀请手动同意 True 全部自动同意 默认 False
    groupRequestDeleteReply: 群邀请拒绝回复 默认 "拒绝群邀请"
    replyTime: 等待选择群邀请同意时长 单位秒 默认 60
    """

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)
        self._request_group_message_list = []
        self._ban_text = plugin_config["banText"] if "banText" in plugin_config else []
        self._ban_text_reply = plugin_config["banTextReply"] if "banTextReply" in plugin_config else "{name} 不可以乱说话哦"
        self._group_request_all = plugin_config["groupRequestAll"] if "groupRequestAll" in plugin_config else False
        self._group_request_delete_reply = plugin_config["groupRequestDeleteReply"] if "groupRequestDeleteReply" in plugin_config else "拒绝群邀请"
        self._reply_time = plugin_config["replyTime"] if "replyTime" in plugin_config else 60

        self.command_load()
        
    def command_load(self):
        self.bot.command(self.get_request_group_invite, "群邀请", {
            "type": "all",
            "admin": True
        })

        self.bot.command(self.delete_request_group_invite, "群邀请清空", {
            "type": "all",
            "admin": True
        })
    
    def on_group_msg(self, message: Message):
        for text in self._ban_text:
            if text not in message.text:
                continue
            
            self.cqapi.delete_msg(message.id)
            message.reply_not_code(self._ban_text_reply.format(name=message.sender["nickname"]))
    
    def get_request_group_invite(self, commandData, message: Message):
        if self._request_group_message_list == []:
            message.reply("没有群邀请...")
            return

        send_message, request_group_message_list = "等待 %s 选择邀请，发送序号同意邀请\n" % message.sender["nickname"], self._request_group_message_list
        for index, request_group_message in enumerate(request_group_message_list):
            send_message = "%s%s\n" % (
                send_message, "%s.来自 qq=%s 的 group_id=%s 群邀请 (type=%s)" % (index,
                    request_group_message["group_id"],
                    request_group_message["user_id"],
                    request_group_message["sub_type"],
                )
            )
        message.reply(send_message)
        message_data = self.cqapi.reply(message.user_id, self._reply_time)
        if message_data is None:
            message.reply("等待 %s 选择邀请超时..." % message.sender["nickname"])
            return
        
        request_index = int(message_data.text)
        request_group_message = request_group_message_list[request_index]
        self.cqapi.set_group_add_request(request_group_message["flag"], request_group_message["sub_type"], True)
        del self._request_group_message_list[request_index]
    
    def delete_request_group_invite(self, commandData, message: Message):
        for request_group_message in self._request_group_message_list:
            self.cqapi.set_group_add_request(
                request_group_message["flag"],
                request_group_message["sub_type"], 
                False,
                self._group_request_delete_reply
            )
        
        message.reply("清空 %s 条群邀请" % len(self._request_group_message_list))
        self._request_group_message_list = []
    
    def request_group_invite(self, message):
        if self._group_request_all:
            self.cqapi.set_group_add_request(message["flag"], message["sub_type"], True)
            logging.info("接受来自 qq=%s 的 group_id=%s 群邀请" % (message["user_id"],message["group_id"] ))
            return
        
        logging.info("保存来自 qq=%s 的 group_id=%s 群邀请" % (message["user_id"],message["group_id"] ))
        self._request_group_message_list.append(message)