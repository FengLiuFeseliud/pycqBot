from pycqBot.cqCode import reply, strToCqCode, get_cq_code


class Message:


    def __init__(self, message_data, cqapi):
        self._cqapi = cqapi
        self.id = message_data["message_id"]
        self.sub_type = message_data["sub_type"]
        self.type = message_data["message_type"]
        self.text = message_data["message"]
        self.user_id = message_data["user_id"]
        self.time = message_data["time"]
        self.sender = message_data["sender"]
        self.group_id = None
        self.temp_source = None
        self.anonymous = None
        self.message_data = message_data
        self.code_str = strToCqCode(self.text)
        self.code = [get_cq_code(code_str) for code_str in self.code_str]

        self._ck_message(message_data)

    
    def _ck_message(self, message_data):
        if "group_id" in message_data:
            self.group_id = message_data["group_id"]
        
        if self.sub_type == "anonymous":
            self.anonymous = message_data["anonymous"]
            return
        
        if self.sub_type == "group":
            self.temp_source = message_data["temp_source"]
            return
    
    def reply(self, message, auto_escape=False):
        """
        回复该消息
        """
        self._cqapi.send_reply(self, "%s%s" % (reply(msg_id=self.id), message), auto_escape)
    
    def reply_not_code(self, message, auto_escape=False):
        """
        回复该消息 不带 cqcode
        """
        self._cqapi.send_reply(self, message, auto_escape)
    
    def record(self, time_end):
        """
        存储该消息
        """
        self._cqapi.record_message(self, time_end)


class cqEvent:

    def meta_event_connect(self, message):
        """
        连接响应
        """
        pass
    
    def meta_event(self, message):
        """
        心跳
        """
        pass
    
    def timing_start(self):
        """
        启动定时任务
        """
        pass
    
    def timing_jobs_start(self, job, run_count):
        """
        群列表定时任准备执行
        """
        pass
    
    def timing_job_end(self, job, run_count, group_id):
        """
        定时任务被执行
        """
        pass

    def timing_jobs_end(self, job, run_count):
        """
        群列表定时任务执行完成
        """
        pass
    
    def runTimingError(self, job, run_count, err, group_id):
        """
        定时任务执行错误
        """
        pass

    def on_group_msg(self, message):
        pass
    
    def on_private_msg(self, message):
        pass

    def at_bot(self, message, cqCode_list, cqCode):
        """
        接收到 at bot
        """
        pass
    
    def at(self, message, cqCode_list, cqCode):
        """
        接收到 at
        """
        pass

    def message_private_friend(self, message):
        """
        好友私聊消息
        """
        pass
    
    def message_private_group(self, message):
        """
        群临时会话私聊消息
        """
        pass
    
    def message_private_group_self(self, message):
        """
        群中自身私聊消息
        """
        pass
    
    def message_private_other(self, message):
        """
        私聊消息
        """
        pass

    def message_group_normal(self, message):
        """
        群消息
        """
        pass

    def notice_group_upload(self, message):
        """
        群文件上传
        """
        pass
    
    def notice_group_admin_set(self, message):
        """
        群管理员设置
        """
        pass

    def notice_group_admin_unset(self, message):
        """
        群管理员取消
        """
        pass
    
    def notice_group_decrease_leave(self, message):
        """
        群成员减少 - 主动退群
        """
        pass
    
    def notice_group_decrease_kick(self, message):
        """
        群成员减少 - 成员被踢
        """
        pass
    
    def notice_group_decrease_kickme(self, message):
        """
        群成员减少 - 登录号被踢
        """
        pass
    
    def notice_group_increase_approve(self, message):
        """
        群成员增加 - 同意入群
        """
        pass

    def notice_group_increase_invite(self, message):
        """
        群成员增加 - 邀请入群
        """
        pass
    
    def notice_group_ban_ban(self, message):
        """
        群禁言
        """
        pass

    def notice_group_ban_lift_ban(self, message):
        """
        群解除禁言
        """
        pass

    def notice_group_recall(self, message):
        """
        群消息撤回
        """
        pass
    
    def notice_notify_lucky_king(self, message):
        """
        群红包运气王提示
        """
        pass
    
    def notice_notify_honor(self, message):
        """
        群成员荣誉变更提示
        honor_type 荣誉类型

        talkative:龙王 
        performer:群聊之火 
        emotion:快乐源泉
        """

        pass
    
    def notice_group_card(self, message):
        """
        群成员名片更新
        """
        pass
    
    def notice_friend_add(self, message):
        """
        好友添加
        """
        pass

    def notice_friend_recall(self, message):
        """
        好友消息撤回
        """
        pass
    
    def notice_notify_poke(self, message):
        """
        好友/群内 戳一戳
        """
        pass
    
    def notice_offline_file(self, message):
        """
        接收到离线文件
        """
        pass

    def notice_client_status(self, message):
        """
        其他客户端在线状态变更
        """
        pass
    
    def notice_essence_add(self, message):
        """
        精华消息添加
        """
        pass
    
    def notice_essence_delete(self, message):
        """
        精华消息移出
        """
        pass

    def request_friend(self, message):
        """
        加好友请求
        """
        pass

    def request_group_add(self, message):
        """
        加群请求
        """
        pass
    
    def request_group_invite(self, message):
        """
        加群邀请
        """
        pass


class Plugin(cqEvent):

    def __init__(self, bot, cqapi, plugin_config) -> None:
        self.bot = bot
        self.cqapi = cqapi
        self.plugin_config = plugin_config