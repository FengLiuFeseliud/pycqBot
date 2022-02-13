import requests


class cqHttpApi:

    def __init__(self, ip="127.0.0.1",port=8000):
        self.http = "http://%s:%s" % (ip, port)

    def link(self, api, data={}):
        with requests.post(self.http + api, data=data) as req:
            return req.json()

    def send_group_msg(self, group_id, message, auto_escape=False):
        """
        发送群消息
        """
        post_data = {
            "group_id":group_id,
            "message":message,
            "auto_escape":auto_escape
        }
        return self.link("/send_group_msg", post_data)
    
    def set_group_ban(self, group_id, user_id, duration=30):
        """
        群组单人禁言
        """
        post_data = {
            "group_id":group_id,
            "user_id":user_id,
            "duration":int(duration) * 60
        }
        return self.link("/set_group_ban", post_data)
    
    def set_group_whole_ban(self, group_id, enable=True):
        """
        群组全员禁言
        """
        post_data = {
            "group_id":group_id,
            "enable": enable
        }
        return self.link("/set_group_whole_ban", post_data)
    
    def set_group_admin(self, group_id, user_id, enable=True):
        """
        群组设置管理员
        """
        post_data = {
            "group_id":group_id,
            "user_id": user_id,
            "enable": enable
        }
        return self.link("/set_group_admin", post_data)
    
    def set_group_card(self, group_id, user_id, card=""):
        """
        设置群名片 ( 群备注 )
        """
        post_data = {
            "group_id":group_id,
            "user_id": user_id,
            "card": card
        }
        return self.link("/set_group_card", post_data)
    
    def set_group_name(self, group_id, group_name):
        """
        设置群名
        """
        post_data = {
            "group_id":group_id,
            "group_name": group_name,
        }
        return self.link("/set_group_name", post_data)

    def set_group_leave(self, group_id, is_dismiss=False):
        """
        退出群组
        """
        post_data = {
            "group_id":group_id,
            "is_dismiss": is_dismiss,
        }
        return self.link("/set_group_leave", post_data)
    
    def set_group_special_title(self, group_id, user_id, special_title="", duration=-1):
        """
        设置群组专属头衔
        """
        post_data = {
            "group_id":group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        }
        return self.link("/set_group_special_title", post_data)

    def set_friend_add_request(self, flag, approve, remark):
        """
        处理加好友请求
        """
        post_data = {
            "flag":flag,
            "approve": approve,
            "remark": remark,
        }
        return self.link("/set_friend_add_request", post_data)
    
    def set_group_add_request(self, flag, sub_type, approve=True, reason=""):
        """
        处理加群请求／邀请
        """
        post_data = {
            "flag":flag,
            "approve": approve,
            "sub_type": sub_type,
            "reason": reason
        }
        return self.link("/set_friend_add_request", post_data)
    
    def get_login_info(self):
        """
        获取登录号信息
        """
        return self.link("/set_friend_add_request")
    
    def qidian_get_account_info(self):
        """
        获取企点账号信息
        """
        return self.link("/qidian_get_account_info")
    
    def get_stranger_info(self, user_id, no_cache=False):
        """
        获取陌生人信息
        """
        post_data = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self.link("/get_stranger_info", post_data)
    
    def get_friend_list(self):
        """
        获取好友列表
        """
        return self.link("/get_friend_list")


class cqBot:

    def __init__(self, cq_api, on_group_msg=None, on_private_msg=None,
            group_id_list=[], user_id_list=[],
            command={}, 
            options={}
        ):

        self.cq_api = cq_api
        # 需处理群
        self.__group_id_list = group_id_list
        # 需处理私信
        self.__user_id_list = user_id_list
        # 群信息勾子
        self.on_group_msg = on_group_msg
        # 群信息勾子
        self.on_private_msg = on_private_msg
        # 指令列表
        self.commandList = command
        # 管理员列表
        self.admin = []
        # 指令标志符
        self.commandSign = "$"
        # 帮助信息模版
        self.help_text = "本bot帮助信息!\n{help_command_text}\npycqbot v0.1.0"

        for key in options.keys():
            exec("self.%s = '%s'" % (key, options[key]))
        
        self.commandList["help"] = {
            "help": [
                "$help - 显示本条帮助信息"
            ]
        }

        self._check_set_command()
        self._set_help_text()

        def print_help(commandData, message, from_id):
            self.cq_api.send_group_msg(from_id, self.help_text)

        self.commandList["help"]["function"] = print_help
    
    def meta_event_connect(self, message):
        """
        连接响应
        """
        print("成功连接 websocket 服务! bot qq:%s" % message["self_id"])
    
    def _set_help_text(self):
        """
        帮助信息模版
        """
        help_command_text = ""
        for command in self.commandList.keys():
            for help_r_text in self.commandList[command]["help"]:
                help_command_text += help_r_text + "\n"
        
        self.help_text = self.help_text.format(help_command_text=help_command_text)
    
    def user_log_srt(self, message):
        user_id = message["user_id"]
        if message["sub_type"] == "normal" or message["sub_type"] == "notice":
            if "card" in message["sender"]:
                user_name = message["sender"]["card"]
            else:
                user_name = message["sender"]["nickname"]
        else:
            user_name = "匿名用户 - %s flag: %s" % (message["anonymous"]["name"],
                message["anonymous"]["flag"])

        if "group_id" in message:
            return "%s (qq=%s,群号=%s)" % (user_name, user_id, message["group_id"])

        return "%s (qq=%s)" % (user_name, user_id)

    def _set_command_key(self, message):
        """
        指令解析
        """

        commandSign = list(message)[0]
        command_str_list = message.split(" ")
        command = command_str_list[0].lstrip(commandSign)
        commandData = command_str_list[1:]

        return commandSign, command, commandData
    
    def _check_set_command(self):
        """
        检查指令设置
        """
        for command in self.commandList.keys():
            if "type" not in self.commandList[command]:
                self.commandList[command]["type"] = "group"
            
            if "admin" not in self.commandList[command]:
                self.commandList[command]["admin"] = False
            
            if "ban" not in self.commandList[command]:
                self.commandList[command]["ban"] = []
            
            if "help" not in self.commandList[command]:
                self.commandList[command]["help"] = ""
    
    def _check_command(self, message, command_type):
        """
        指令检查
        """

        commandSign, command, commandData = self._set_command_key(message["message"])

        if "group_id" in message:
            from_id = message["group_id"]
        else:
            from_id = message["user_id"]

        if commandSign != self.commandSign:
            return False
        
        self.check_command(message, from_id)
        
        if command not in self.commandList:
            self.notCommandError(message, from_id)
            return False
        
        if self.commandList[command]["type"] != command_type:
            return False
        
        if from_id in self.commandList[command]["ban"]:
            self.banCommandError(message, from_id)
            return False
        
        if self.commandList[command]["admin"] and message["user_id"] not in self.admin:
            self.purviewError(message, from_id)
            return False

        return commandSign, command, commandData, from_id
    
    def _run_command(self, message, command_type):
        """
        指令运行
        """

        commandIn = self._check_command(message, command_type)
        if not commandIn:
            return

        commandSign, command, commandData, from_id = commandIn

        try:
            self.commandList[command]["function"](commandData, message, from_id)
        except Exception as err:
            self.runCommandError(message, err, from_id)
    
    def check_command(self, message, from_id):
        """
        指令开始检查勾子
        """
        print("%s 使用指令: %s" % (self.user_log_srt(message), message["message"]))

    def _message_private(self, message):
        """
        通用私聊消息处理
        """
        if message["user_id"] not in self.__user_id_list or self.__user_id_list == []:
            return

        try:
            self.on_private_msg(message) 
        except TypeError:
            pass
        
        self._run_command(message, "private")
    
    def _message_group(self, message):
        """
        通用群消息处理
        """
        if message["group_id"] not in self.__group_id_list or self.__group_id_list == []:
            return

        try:
            self.on_group_msg(message) 
        except TypeError:
            pass
        
        self._run_command(message, "group")
    
    def _bot_message_log(self, log, from_id):
        print(log)
        self.cq_api.send_group_msg(from_id, log)

    def message_private_friend(self, message):
        """
        好友私聊消息
        """
        self._message_private(message)
    
    def message_private_group(self, message):
        """
        群临时会话私聊消息
        """
        self._message_private(message)
    
    def message_private_group_self(self, message):
        """
        群中自身私聊消息
        """
        self._message_private(message)
    
    def message_private_other(self, message):
        """
        私聊消息
        """
        self._message_private(message)

    def message_group_normal(self, message):
        """
        群消息
        """
        self._message_group(message)
    
    def notCommandError(self, message, from_id):
        """
        指令不存在时错误
        """
        self._bot_message_log("指令 %s 不存在..." % message["message"], from_id)
    
    def banCommandError(self, message, from_id):
        """
        指令被禁用时错误
        """
        self._bot_message_log("指令 %s 被禁用!" % message["message"], from_id)
    
    def purviewError(self, message, from_id):
        """
        指令权限不足时错误
        """
        self._bot_message_log("%s 权限不足... 指令 %s" % (self.user_log_srt(message), message["message"]), from_id)
    
    def runCommandError(self, message, err, from_id):
        """
        指令运行时错误
        """
        self._bot_message_log("指令 %s 运行时错误... Error: %s" % (message["message"], err), from_id)
    

    def notice_group_upload(self, message, from_id):
        """
        群文件上传
        """
        pass
    
    def notice_group_admin_set(self, message, from_id):
        """
        群管理员设置
        """
        pass

    def notice_group_admin_unset(self, message, from_id):
        """
        群管理员取消
        """
        pass
    
    def notice_group_decrease_leave(self, message, from_id):
        """
        群成员减少 - 主动退群
        """
        pass
    
    def notice_group_decrease_kick(self, message, from_id):
        """
        群成员减少 - 成员被踢
        """
        pass
    
    def notice_group_decrease_kickme(self, message, from_id):
        """
        群成员减少 - 登录号被踢
        """
        pass
    
    def notice_group_increase_approve(self, message, from_id):
        """
        群成员增加 - 同意入群
        """
        pass

    def notice_group_increase_invite(self, message, from_id):
        """
        群成员增加 - 邀请入群
        """
        pass
    
    def notice_group_ban_ban(self, message, from_id):
        """
        群禁言
        """
        pass

    def notice_group_ban_lift_ban(self, message, from_id):
        """
        群解除禁言
        """
        pass

    def notice_group_recall(self, message, from_id):
        """
        群消息撤回
        """
        pass
    
    def notice_notify_lucky_king(self, message, from_id):
        """
        群红包运气王提示
        """
        pass
    
    def notice_notify_honor(self, message, from_id):
        """
        群成员荣誉变更提示
        honor_type 荣誉类型

        talkative:龙王 
        performer:群聊之火 
        emotion:快乐源泉
        """

        pass
    
    def notice_group_card(self, message, from_id):
        """
        群成员名片更新
        """
        pass
    
    def notice_friend_add(self, message, from_id):
        """
        好友添加
        """
        pass

    def notice_friend_recall(self, message, from_id):
        """
        好友消息撤回
        """
        pass
    
    def notice_notify_poke(self, message, from_id):
        """
        好友/群内 戳一戳
        """
        pass
    
    def notice_offline_file(self, message, from_id):
        """
        接收到离线文件
        """
        pass

    def notice_client_status(self, message, from_id):
        """
        其他客户端在线状态变更
        """
        pass
    
    def notice_essence_add(self, message, from_id):
        """
        精华消息添加
        """
        pass
    
    def notice_essence_delete(self, message, from_id):
        """
        精华消息移出
        """
        pass

    def request_friend(self, message, from_id):
        """
        加好友请求
        """
        pass

    def request_group_add(self, message, from_id):
        """
        加群请求
        """
        pass
    
    def request_group_invite(self, message, from_id):
        """
        加群邀请
        """
        pass