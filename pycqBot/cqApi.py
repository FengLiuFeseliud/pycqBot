import requests
import os
from logging import handlers
import logging
from threading import Thread
import time
import sqlite3
from pycqBot.object import Message, cqEvent
from pycqBot.socketApp import cqSocket, asyncHttp
import importlib
import yaml


class cqHttpApi(asyncHttp):

    def __init__(self, host="http://127.0.0.1:8000", download_path="./download", chunk_size=1024) -> None:
        super().__init__(download_path, chunk_size)
        self.http = host
        self.__reply_list_msg = {}
        self.thread_count = 4
        self.bot_qq = 0

    def create_bot(self, host="ws://127.0.0.1:5700", group_id_list=[], user_id_list=[], options={}):
        """
        直接创建一个 bot 
        """
        return cqBot(
            self, host, group_id_list, user_id_list, options
        )
    
    def _create_sql_link(self, db_path, sleep):
        """
        长效消息存储 初始化
        """
        db_path = os.path.join(db_path, "bot_sql.db")
        self._db_path = db_path

        if os.path.isfile(db_path):
            os.remove(db_path)

        with sqlite3.connect(self._db_path) as sql_link:
            sql_cursor = sql_link.cursor()
            # 初始化 Message 表
            sql_cursor.execute("""CREATE TABLE `Message` (
                    ID               INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId           NOT NULL,
                    stime            NOT NULL,
                    etime            NOT NULL,
                    messageData JSON NOT NULL
                );
            """)

            sql_link.commit()
        
        thread = Thread(target=self._record_message_ck, args=(sleep,),name="_record_message_ck")
        thread.setDaemon(True)
        thread.start()
    
    def _record_message_ck(self, sleep):
        """
        长效消息存储 检查失效消息
        """
        while True:
            try:
                with sqlite3.connect(self._db_path) as sql_link:
                    sql_cursor = sql_link.cursor()
                    data_list = sql_cursor.execute("SELECT * FROM `Message` WHERE etime < '%s'" % int(time.time()))
                    for data in data_list:
                        sql_cursor.execute("DELETE from `Message` where ID = '%s'" % data[0])
                        self.recordMessageInvalid(data, sql_link)

            except Exception as err:
                self.recordMessageCKError(err)

            time.sleep(sleep)

    def record_message(self, message_data, time_end):
        """
        长效消息存储
        """
        time_int = int(time.time())
        time_end = time_int + time_end
        try:
            with sqlite3.connect(self._db_path) as sql_link:
                sql_cursor = sql_link.cursor()
                sql_cursor.execute("""
                    INSERT INTO `Message` VALUES (
                        NULL , "%s", "%s", "%s", "%s" 
                    )
                """ % (message_data.user_id, time_int, time_end, message_data.message_data))
                sql_link.commit()
        except Exception as err:
            self.recordMessageError(message_data, time_int, time_end, err)
    
    def record_message_get(self, user_id):
        """
        长效消息存储 获取
        """
        try:
            with sqlite3.connect(self._db_path) as sql_link:
                sql_cursor = sql_link.cursor()
                data_list = sql_cursor.execute("SELECT * FROM `Message` WHERE userId = '%s'" % user_id)

                data_list = data_list.fetchall()
                return data_list

        except Exception as err:
            self.recordMessageGetError(user_id, err)

    def reply(self, user_id, sleep) -> Message or None:
        """
        等待回复
        """
        in_time =  time.time()
        sleep += in_time
        self.__reply_list_msg[user_id] = None
        while in_time < sleep:
            in_time = time.time()
            if self.__reply_list_msg[user_id] is None:
                continue
            
            break
        
        reply_msg = self.__reply_list_msg[user_id]
        self.__reply_list_msg.pop(user_id)

        return reply_msg
    
    def _reply_ck(self, user_id):
        """
        等待回复 检查
        """
        if user_id in self.__reply_list_msg:
            return True
        
        return False
    
    def _reply_add(self, user_id, msg):
        """
        等待回复 添加回复数据
        """
        self.__reply_list_msg[user_id] = msg

    def _link(self, api, data={}):
        try:
            with requests.post(self.http + api, data=data) as req:
                json =  req.json()
                logging.debug("cqAPI 响应: %s" % json)
                if json["retcode"] != 0:
                    self.apiLinkError(json)
                    
                return json
            
        except Exception as err:
            self.apiLinkRunError(err)
    
    def send_private_msg(self, user_id, message, group_id="", auto_escape=False):
        """
        发送私聊消息
        """
        post_data = {
            "user_id": user_id,
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        }
        self.add("/send_msg", post_data)

    def send_group_msg(self, group_id, message, auto_escape=False):
        """
        发送群消息
        """
        post_data = {
            "group_id":group_id,
            "message":message,
            "auto_escape":auto_escape
        }
        self.add("/send_msg", post_data)
    
    def send_group_forward_msg(self, group_id, message):
        """
        发送合并转发 ( 群 )
        """
        post_data = {
            "group_id":group_id,
            "messages": message,
        }
        self.add("/send_group_forward_msg", post_data)

    def send_reply(self, from_message, message, auto_escape=False):
        """
        发送回复
        """
        if from_message.type == "group":
            self.send_group_msg(from_message.group_id, message, auto_escape)
        
        if from_message.type == "private":
            self.send_private_msg(from_message.user_id, message, auto_escape)
    
    def get_forward(self, forward_id):
        """
        获取合并转发
        """
        post_data = {
            "id":forward_id,
        }
        return self._link("/get_forward_msg", post_data)
    
    def set_group_ban(self, group_id, user_id, duration=30):
        """
        群组单人禁言
        """
        post_data = {
            "group_id":group_id,
            "user_id":user_id,
            "duration":int(duration) * 60
        }
        self.add("/send_msg", post_data)
    
    def set_group_whole_ban(self, group_id, enable=True):
        """
        群组全员禁言
        """
        post_data = {
            "group_id":group_id,
            "enable": enable
        }
        self.add("/send_msg", post_data)
    
    def set_group_admin(self, group_id, user_id, enable=True):
        """
        群组设置管理员
        """
        post_data = {
            "group_id":group_id,
            "user_id": user_id,
            "enable": enable
        }
        self.add("/send_msg", post_data)
    
    def set_group_card(self, group_id, user_id, card=""):
        """
        设置群名片 ( 群备注 )
        """
        post_data = {
            "group_id":group_id,
            "user_id": user_id,
            "card": card
        }
        self.add("/send_msg", post_data)
    
    def set_group_name(self, group_id, group_name):
        """
        设置群名
        """
        post_data = {
            "group_id":group_id,
            "group_name": group_name,
        }
        self.add("/send_msg", post_data)

    def set_group_leave(self, group_id, is_dismiss=False):
        """
        退出群组
        """
        post_data = {
            "group_id":group_id,
            "is_dismiss": is_dismiss,
        }
        self.add("/send_msg", post_data)
    
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
        self.add("/send_msg", post_data)

    def set_friend_add_request(self, flag, approve, remark):
        """
        处理加好友请求
        """
        post_data = {
            "flag":flag,
            "approve": approve,
            "remark": remark,
        }
        self.add("/send_msg", post_data)
    
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
        self.add("/send_msg", post_data)
    
    def get_msg(self, message_id):
        """
        获取消息
        """
        post_data = {
            "message_id": message_id,
        }
        return self._link("/get_msg", post_data)
    
    def get_login_info(self):
        """
        获取登录号信息
        """
        return self._link("/set_friend_add_request")
    
    def qidian_get_account_info(self):
        """
        获取企点账号信息
        """
        return self._link("/qidian_get_account_info")
    
    def get_stranger_info(self, user_id, no_cache=False):
        """
        获取陌生人信息
        """
        post_data = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self._link("/get_stranger_info", post_data)
    
    def get_friend_list(self):
        """
        获取好友列表
        """
        return self._link("/get_friend_list")
    
    def get_image(self, file):
        """
        获取图片信息
        """
        post_data = {
            "file": file
        }
        return self._link("/get_image", post_data)
    
    async def _cqhttp_download_file(self, url, headers):
        """
        go-cqhttp 的内置下载 (异步)
        """
        post_data = {
            "url":url,
            "headers": headers,
            "thread_count": self.thread_count
        }
        return (await self._asynclink("/download_file", post_data))["data"]["file"]
    
    def cqhttp_download_file(self, url, headers):
        """
        go-cqhttp 的内置下载
        """
        post_data = {
            "url":url,
            "headers": headers,
            "thread_count": self.thread_count
        }
        return self._link("/download_file", post_data)["file"]
    
    def get_status(self):
        """
        获取 go-cqhttp 状态
        """
        return self._link("/get_status")
    
    def recordMessageInvalid(self, record_message_data, sql_link):
        """
        长效消息存储 消息失效
        """
        logging.debug("长效消息存储 消息失效 %s" % str(record_message_data))
    
    def recordMessageError(self, message_data, time_int, time_end, err):
        """
        长效消息存储 消息存储失败
        """
        logging.error("长效消息存储 消息存储失败 %s Error: %s" % (message_data, err))
        logging.exception(err)
    
    def recordMessageGetError(self, user_id, err):
        """
        长效消息存储 消息查询失败
        """
        logging.error("长效消息存储 消息查询失败 user_id: %s Error: %s" % (user_id, err))
        logging.exception(err)
    
    def recordMessageCKError(self, err):
        """
        长效消息存储 检查消息失败
        """
        logging.error("长效消息存储 检查消息失败 Error: %s" % err)
        logging.exception(err)


class cqBot(cqSocket, cqEvent):
    """
    cqBot 机器人
    """

    def __init__(self, cqapi, host, group_id_list=[], user_id_list=[], options={}):
        super().__init__(host)

        self.cqapi = cqapi
        self.__plugin_list = []
        # bot qq
        self.__bot_qq = 0
        # 需处理群
        self.__group_id_list = group_id_list
        # 需处理私信
        self.__user_id_list = user_id_list
        # 指令列表
        self._commandList = {}
        # 定时任务
        self._timingList = {}
        # 管理员列表
        self.admin = []
        # 指令标志符
        self.commandSign = "#"
        # 帮助信息模版
        self.help_text_format = "本bot帮助信息!\n{help_command_text}\npycqbot v0.1.0"
        self.help_command_text = ""
        # 长效消息存储
        self.messageSql = False
        # 长效消息存储 数据库目录
        self.messageSqlPath = "./"
        # 长效消息存储 清理间隔
        self.messageSqlClearTime = 60
        # go_cqhttp 状态 通过心跳更新
        self._go_cqhttp_status = {}

        for key in options.keys():
            if type(options[key]) is str:
                exec("self.%s = '%s'" % (key, options[key]))
            else:
                exec("self.%s = %s" % (key, options[key]))

        """
        内置指令 help
            显示帮助信息
        """

        def print_help(_, message):
            message.reply(self.help_text)

        self.command(print_help, "help", {
            "type": "all",
            "help": [
                self.commandSign + "help - 显示本条帮助信息",
            ]
        })

        """
        内置指令 status
            查看 go-cqhttp 状态
        """
        
        def status(_, message):
            if self._go_cqhttp_status == {}:
                self.cqapi.send_reply(message, "go-cqhttp 心跳未被正常配置，请检查")
                logging.warning("go-cqhttp 心跳未被正常配置")
                return

            status_msg = "bot (qq=%s) 是否在线：%s\n收到数据包：%s\n发送数据包：%s\n丢失数据包：%s\n接受信息：%s\n发送信息：%s\nTCP 链接断开：%s\n账号掉线次数：%s\n最后消息时间：%s" % (
                self.__bot_qq,
                self._go_cqhttp_status["online"],
                self._go_cqhttp_status["stat"]["PacketReceived"],
                self._go_cqhttp_status["stat"]["PacketSent"],
                self._go_cqhttp_status["stat"]["PacketLost"],
                self._go_cqhttp_status["stat"]["MessageReceived"],
                self._go_cqhttp_status["stat"]["MessageSent"],
                self._go_cqhttp_status["stat"]["DisconnectTimes"],
                self._go_cqhttp_status["stat"]["LostTimes"],
                self._go_cqhttp_status["stat"]["LastMessageTime"],
            )

            message.reply(status_msg)
        
        self.command(status, "status", {
            "type": "all",
            "admin": True,
            "help": [
                self.commandSign + "status - 获取 go-cqhttp 状态",
            ]
        })

    def _on_message(self, wsapp, message):
        event_name = super()._on_message(wsapp, message)
        if event_name is None:
            return

        self._plugin_event_run(event_name, message)
    
    @staticmethod
    def _import_plugin_config() -> dict:
        if os.path.isfile("./plugin_config.yml"):
            with open("./plugin_config.yml", "r") as file:
                return yaml.safe_load(file.read())
        else:
            with open("./plugin_config.yml", "w") as file:
                file.write(r"{}")

        return {}
    
    def _import_plugin(self, plugin: str, plugin_config: dict):
        try:
            if plugin.rsplit(".", maxsplit=1)[0] == "pycqBot.plugin":
                plugin_obj = importlib.import_module(plugin)
                plugin = plugin.rsplit(".", maxsplit=1)[-1]
            else:
                plugin_obj = importlib.import_module("plugin.%s" % plugin)

            if eval("plugin_obj.%s.__base__.__name__ != 'Plugin'" % plugin):
                logging.warning("%s 插件未继承 pycqBot.Plugin 不进行加载" % plugin)
                del plugin_obj
                return
            
            if plugin not in plugin_config:
                plugin_config[plugin] = {}

            plugin_obj = eval("plugin_obj.%s(self, self.cqapi, plugin_config[plugin])" % plugin)
            self.__plugin_list.append(plugin_obj)

            logging.debug("%s 插件加载完成" % plugin)
        except ModuleNotFoundError:
            self.pluginNotFoundError(plugin)
        except Exception as err:
            self.pluginImportError(plugin, err)
    
    def _plugin_event_run(self, event_name, *args):
        for plugin_obj in self.__plugin_list:
            eval('plugin_obj.%s' % event_name)(*args)

    def plugin_load(self, plugin):
        """
        加载插件
        """
        plugin_config = self._import_plugin_config()
        if type(plugin) == str:
            self._import_plugin(plugin, plugin_config)
        
        if type(plugin) == list:
            for plugin_ in plugin:
                self._import_plugin(plugin_, plugin_config)
            
            logging.info("插件列表加载完成: %s" % plugin)
    
    def pluginNotFoundError(self, plugin):
        """
        插件不存在
        """
        logging.error("plugin 目录下不存在插件 %s " % plugin)
    
    def pluginImportError(self, plugin, err):
        """
        加载插件时发生错误
        """
        logging.error("加载插件 %s 时发生错误: %s" % (plugin, err))
        logging.exception(err)
        
    def _check_command_options(self, options):
        """
        检查指令设置
        """
        if "type" not in options:
            options["type"] = "group"
        
        if "admin" not in options:
            options["admin"] = False
        
        if "user" not in options:
            options["user"] = ["all"]
        else:
            options["user"] = options["user"].split(",")
        
        if "ban" not in options:
            options["ban"] = []

        if "help" in options:
            for help_r_text in options["help"]:
                self.help_command_text = "%s%s\n" % (self.help_command_text, help_r_text)
            
            self.help_text = "%s\n" % self.help_text_format.format(help_command_text=self.help_command_text)
        
        return options
    
    def _check_timing_options(self, options, timing_name):
        options["name"] = timing_name

        if "timeSleep" not in options:
            logging.warning("定时任务 %s 没有指定 timeSleep 间隔, 中止创建" % timing_name)
            return False

        if "ban" not in options:
            options["ban"] = []

        return options
        
    def command(self, function, command_name, options=None):
        if options is None:
            options = {}
            
        options = self._check_command_options(options)

        if type(command_name) == str:
            command_name = [command_name]

        for name in command_name:
            self._commandList[name] = options
            self._commandList[name]["function"] = function

    def _timing_job(self, job):
        run_count = 0
        while True:
            self.timing_jobs_start(job, run_count)
            self._plugin_event_run("timing_jobs_start", job, run_count)
            for group_id in self.__group_id_list:
                if group_id in job["ban"]:
                    return
                
                run_count += 1
                try:
                    job["function"](group_id)
                    self.timing_job_end(job, run_count, group_id)
                    self._plugin_event_run("timing_job_end", job, run_count, group_id)

                except Exception as err:
                    self.runTimingError(job, run_count, err, group_id)
                    self._plugin_event_run("runTimingError", job, run_count, err, group_id)

            self.timing_jobs_end(job, run_count)
            self._plugin_event_run("timing_jobs_end", job, run_count)
            time.sleep(job["timeSleep"])
    
    def timing(self, function, timing_name, options=None):
        if options is None:
            options = {}

        options = self._check_timing_options(options, timing_name)
        if not options:
            return

        options["function"] = function
        self._timingList[timing_name] = options

        thread = Thread(target=self._timing_job, args=(self._timingList[timing_name],), name=timing_name)
        thread.setDaemon(True)
        thread.start()

        logging.info("创建定时任务 %s " % timing_name)
    
    def set_bot_status(self, message):
        self.__bot_qq = message["self_id"]
        self.cqapi.bot_qq = message["self_id"]
    
    def _meta_event_connect(self, message):
        """
        连接响应
        """
        self.set_bot_status(message)
        if self.messageSql is True:
            self.cqapi._create_sql_link(self.messageSqlPath, self.messageSqlClearTime)
    
    def meta_event_connect(self, message):
        """
        连接响应
        """
        self._meta_event_connect(message)
        logging.info("成功连接 websocket 服务! bot qq:%s" % self.__bot_qq)
    
    def meta_event(self, message):
        """
        心跳
        """
        self.set_bot_status(message)
        self._go_cqhttp_status = message["status"]
    
    def timing_start(self):
        """
        启动定时任务
        """
        self._timing_start()
        logging.info("定时任务启动完成!")

    def timing_jobs_end(self, job, run_count):
        """
        群列表定时任务执行完成
        """
        logging.debug("定时任务 %s 执行完成! 共执行 %s 次" % (job["name"], run_count))
        pass
    
    def runTimingError(self, job, run_count, err, group_id):
        """
        定时任务执行错误
        """
        logging.error("定时任务 %s 在群 %s 执行错误... 共执行 %s 次 Error: %s" % (job["name"], group_id, run_count, err))
        logging.exception(err)

    def user_log_srt(self, message):
        user_id = message.user_id
        if message.type == "private":
            user_name = message.sender["nickname"]
        elif message.type == "group":
            if message.anonymous == None:
                if message.sender["card"].strip() != '':
                    user_name = message.sender["card"]
                else:
                    user_name = message.sender["nickname"]
            else:
                user_name = "匿名用户 - %s flag: %s" % (message.anonymous["name"],
                    message.anonymous["flag"])

        if message.type == "group":
            return "%s (qq=%s,群号=%s)" % (user_name, user_id, message.group_id)

        return "%s (qq=%s)" % (user_name, user_id)

    def _set_command_key(self, message):
        """
        指令解析
        """

        if self.commandSign != "":
            commandSign = list(message)[0]
        else:
            commandSign = ""

        command_str_list = message.split(" ")
        command = command_str_list[0].lstrip(commandSign)
        commandData = command_str_list[1:]

        return commandSign, command, commandData
    
    def _check_command(self, message, command_type):
        """
        指令检查
        """

        commandSign, command, commandData = self._set_command_key(message.text)

        if commandSign != self.commandSign:
            return False

        if message.type == "group":
            from_id = message.group_id
        else:
            from_id = message.user_id
        
        if command not in self._commandList:
            self.notCommandError(message, from_id)
            return False

        if self._commandList[command]["type"] != command_type and self._commandList[command]["type"] != "all":
            return False
        
        self.check_command(message, from_id)
        
        if from_id in self._commandList[command]["ban"]:
            self.banCommandError(message, from_id)
            return False
        
        user_list = self._commandList[command]["user"]
        if user_list[0] != "all" and message.type == "group":
            if "role" not in message.sender and "anonymous" not in user_list:
                self.userPurviewError(message, from_id)
                return False
            elif "role" in message.sender:
                if message.sender["role"] not in user_list and user_list[0] != "nall":
                    self.userPurviewError(message, from_id)
                    return False
        
        if self._commandList[command]["admin"] and message.user_id not in self.admin:
            self.purviewError(message, from_id)
            return False

        return commandSign, command, commandData
    
    def _run_command(self, message, command_type):
        """
        指令运行
        """
        def run_command(message, command_type):
            try:
                commandIn = self._check_command(message, command_type)
                if not commandIn:
                    return

                commandSign, command, commandData = commandIn
                self._commandList[command]["function"](commandData, message)

            except Exception as err:
                self.runCommandError(message, err)
        
        thread = Thread(target=run_command, args=(message, command_type, ), name="command")
        thread.setDaemon(True)
        thread.start()

    def check_command(self, message, from_id):
        """
        指令开始检查勾子
        """
        logging.info("%s 使用指令: %s" % (self.user_log_srt(message), message.text))
    
    def _message(self, message) -> Message:
        """
        通用消息处理
        """

        message = Message(message, self.cqapi)
        # 检查等待回复
        if self.cqapi._reply_ck(message.user_id):
            self.cqapi._reply_add(message.user_id, message)
        
        return message

    def _message_private(self, message) -> Message:
        """
        通用私聊消息处理
        """
        if (message["user_id"] not in self.__user_id_list) and self.__user_id_list != []:
            return

        message = self._message(message)
        self.on_private_msg(message)
        self._plugin_event_run("on_private_msg", message)
        self._run_command(message, "private")

        return message
    
    def _message_group(self, message) -> Message:
        """
        通用群消息处理
        """
        if message["group_id"] not in self.__group_id_list and self.__group_id_list != []:
            return

        message = self._message(message)
        self.on_group_msg(message)
        self._plugin_event_run("on_group_msg", message)

        for cqCode in message.code:
            if cqCode["type"] == "at":
                if cqCode["data"]["qq"] == str(self.__bot_qq):
                    self.at_bot(message, message.code, cqCode)
                    self._plugin_event_run("at_bot", message, message.code, cqCode)
                    continue
                
                self.at(message, message.code, cqCode)
                self._plugin_event_run("at", message, message.code, cqCode)
        
        self._run_command(message, "group")

        return message
    
    def _bot_message_log(self, log, message):
        logging.info(log)
        self.cqapi.send_reply(message, log)
    
    def at_bot(self, message, cqCode_list, cqCode):
        """
        接收到 at bot
        """
        logging.info("接收到 at bot %s " % self.user_log_srt(message))

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
        # commandSign 为空时不处理 不然每一条消息都会调用 notCommandError ...
        if self.commandSign == "":
            return

        self._bot_message_log("指令 %s 不存在..." % message.text, message)
    
    def banCommandError(self, message, from_id):
        """
        指令被禁用时错误
        """
        self._bot_message_log("指令 %s 被禁用!" % message.text, message)
    
    def userPurviewError(self, message, from_id):
        """
        指令用户组权限不足时错误
        """
        self._bot_message_log("%s 用户组权限不足... 指令 %s" % (self.user_log_srt(message), message.text), message)
    
    def purviewError(self, message, from_id):
        """
        指令权限不足时错误 (bot admin)
        """
        self._bot_message_log("%s 权限不足... 指令 %s" % (self.user_log_srt(message), message.text), message)
    
    def runCommandError(self, message, err):
        """
        指令运行时错误
        """
        self._bot_message_log("指令 %s 运行时错误... Error: %s" % (message.text, err), message)
        logging.exception(err)


class cqLog:

    def __init__(self, level=logging.DEBUG, 
            logPath="./cqLogs", 
            when="d", 
            interval=1,
            backupCount=7
        ):

        logger = logging.getLogger()
        logger.setLevel(level)

        if not os.path.isdir(logPath):
            os.makedirs(logPath)

        sh = logging.StreamHandler()
        rh = handlers.TimedRotatingFileHandler(
            os.path.join(logPath, "cq.log"), 
            when,
            interval,
            backupCount
        )
        
        logger.addHandler(sh)
        logger.addHandler(rh)

        formatter = logging.Formatter(
            self.setFormat()
        )
        sh.setFormatter(formatter)
        rh.setFormatter(formatter)
        
    def setFormat(self):
        return "\033[0m[%(asctime)s][%(threadName)s/%(levelname)s] PyCqBot: %(message)s\033[0m"