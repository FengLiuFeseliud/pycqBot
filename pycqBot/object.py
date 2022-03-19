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