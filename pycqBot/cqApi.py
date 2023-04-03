import asyncio
import importlib
import platform
import subprocess
from typing import Union, Optional, Any, Callable
import requests
import os
from logging import handlers
import logging
from threading import Thread
import time
import sqlite3
from websockets.exceptions import ConnectionClosedError
import websockets

import pycqBot
from pycqBot.data import *
from pycqBot.data.event import _get_event
from pycqBot.object import cqEvent
from pycqBot.asyncHttp import asyncHttp
import yaml


class cqHttpApi(asyncHttp):

    def __init__(self, host: str="http://127.0.0.1:5700", download_path: str="./download", chunk_size: int=1024) -> None:
        super().__init__(download_path, chunk_size)
        self.http = host
        self.__reply_list_msg: dict[int, Optional[Message]] = {}
        self.thread_count = 4
        self.bot_qq = 0

    def create_bot(self, host: str="ws://127.0.0.1:8080", group_id_list: list[int]=[], user_id_list: list[int]=[], options: dict[str, Any]={}) -> "cqBot":
        """
        直接创建一个 bot 
        """
        return cqBot(
            self, host, group_id_list, user_id_list, options
        )
    
    def _create_sql_link(self, db_path: str, sleep: int) -> None:
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
    
    def _record_message_ck(self, sleep: int) -> None:
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

    def record_message(self, message: Message, time_end: int) -> None:
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
                """ % (message.sender.id, time_int, time_end, message._message_data))
                sql_link.commit()
        except Exception as err:
            self.recordMessageError(message, time_int, time_end, err)
    
    def record_message_get(self, user_id: int) -> Optional[list[dict[str, Any]]]:
        """
        长效消息存储 获取
        """
        try:
            with sqlite3.connect(self._db_path) as sql_link:
                sql_cursor = sql_link.cursor()
                data_cursor = sql_cursor.execute("SELECT * FROM `Message` WHERE userId = '%s'" % user_id)

                data_list = data_cursor.fetchall()
                return data_list

        except Exception as err:
            self.recordMessageGetError(user_id, err)
        
        return None

    def reply(self, user_id, sleep) -> Optional[Message]:
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
    
    def _reply_ck(self, user_id: int) -> bool:
        """
        等待回复 检查
        """
        if user_id in self.__reply_list_msg:
            return True
        
        return False
    
    def _reply_add(self, user_id: int, msg: Message) -> None:
        """
        等待回复 添加回复数据
        """
        self.__reply_list_msg[user_id] = msg

    def _link(self, api: str, data: dict[str, Any]={}) -> Optional[dict[Any, Any]]:
        try:
            with requests.post(f"{self.http}{api}", data=data) as req:
                json =  req.json()
                logging.debug("cqAPI 响应: %s" % json)
                if json["retcode"] != 0:
                    self.apiLinkError(json)
                    
                return json
            
        except Exception as err:
            self.apiLinkRunError(err)
        
        return None
    
    def send_private_msg(self, user_id: int, message: str, group_id: Optional[int] = None, auto_escape: bool=False) -> None:
        """
        发送私聊消息
        """
        post_data = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape
        }

        if group_id is not None:
            post_data["group_id"] = group_id
        
        self.add("/send_msg", post_data)

    def send_group_msg(self, group_id: int, message: str, auto_escape: bool=False) -> None:
        """
        发送群消息
        """
        self.add("/send_msg", {
            "group_id":group_id,
            "message":message,
            "auto_escape":auto_escape
        })
    
    def send_group_forward_msg(self, group_id: int, message: str) -> None:
        """
        发送合并转发 ( 群 )
        """
        self.add("/send_group_forward_msg", {
            "group_id":group_id,
            "messages": message,
        })
    
    def send_private_forward_msg(self, user_id: int, message: str) -> None:
        """
        发送合并转发 ( 私聊 )
        """
        self.add("/send_private_forward_msg", {
            "user_id":user_id,
            "messages": message,
        })

    def send_reply(self, from_message: Union[Private_Message, Group_Message], message: str, auto_escape: bool=False) -> None: 
        """
        发送回复
        """
        if type(from_message) is Group_Message:
            self.send_group_msg(from_message.group_id, message, auto_escape)
        
        if type(from_message) is Private_Message:
            self.send_private_msg(from_message.sender.id, message, auto_escape)

    def send_forward_msg(self, from_message: Union[Private_Message, Group_Message], message: str) -> None: 
        """
        发送合并转发
        """
        if type(from_message) is Group_Message:
            self.send_group_forward_msg(from_message.group_id, message)
        
        if type(from_message) is Private_Message:
            self.send_private_forward_msg(from_message.sender.id, message)
    
    def get_forward(self, forward_id: int) -> Optional[dict[Any, Any]]:
        """
        获取合并转发
        """
        return self._link("/get_forward_msg", {
            "id":forward_id,
        })
    
    def set_group_ban(self, group_id: int, user_id: int, duration: int=30) -> None:
        """
        群组单人禁言
        """
        self.add("/set_group_ban", {
            "group_id":group_id,
            "user_id":user_id,
            "duration":int(duration) * 60
        })

    def set_group_anonymous_ban(self, group_id: int, anonymous, anonymous_flag: str, duration: int = 1800) -> None:
        """
        群匿名用户禁言
        """
        self.add("/set_group_anonymous_ban", {
            "group_id":group_id,
            "anonymous": anonymous,
            "anonymous_flag": anonymous_flag,
            "duration": duration
        })
    
    def set_group_whole_ban(self, group_id: int, enable: bool=True) -> None:
        """
        群组全员禁言
        """
        self.add("/set_group_whole_ban", {
            "group_id":group_id,
            "enable": enable
        })
    
    def set_group_admin(self, group_id: int, user_id: int, enable: bool=True) -> None:
        """
        群组设置管理员
        """
        self.add("/set_group_admin", {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        })

    def set_essence_msg(self, message_id: int):
        """
        设置精华消息
        """
        self.add("/set_essence_msg", {
            "message_id": message_id
        })

    def delete_essence_msg(self, message_id: int):
        """
        移出精华消息
        """
        self.add("/delete_essence_msg", {
            "message_id": message_id
        })

    def send_group_sign(self, group_id: int):
        """
        群打卡
        """
        self.add("/send_group_sign", {
            "group_id": group_id
        })

    def set_group_anonymous(self, group_id: int, enable: bool = True):
        """
        群设置匿名 (该 API 暂未被 go-cqhttp 支持)
        """
        self.add("/set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        })

    def _send_group_notice(self, group_id: int, content: str, image: Optional[str] = None):
        """
        发送群公告
        """
        post_data = {
            "group_id": group_id,
            "enable": content   
        }

        if image != None:
            post_data["image"] = image
        
        self.add("/set_group_anonymous", post_data)

    def _get_group_notice(self, group_id: int):
        """
        获取群公告
        """
        return self._link("/_get_group_notice", {
            "group_id": group_id
        })

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False):
        """
        群组踢人
        """
        self.add("/set_group_kick", {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        })
    
    def set_group_card(self, group_id: int, user_id: int, card: str="") -> None:
        """
        设置群名片 ( 群备注 )
        """
        self.add("/set_group_card", {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        })
    
    def set_group_name(self, group_id: int, group_name: str) -> None:
        """
        设置群名
        """
        self.add("/set_group_name", {
            "group_id":group_id,
            "group_name": group_name,
        })

    def set_group_portrait(self, group_id: int, file: str, cache: int = 1):
        """
        设置群头像
        """
        self.add("/set_group_portrait", {
            "group_id":group_id,
            "file": file,
            "cache": cache
        })

    def set_group_leave(self, group_id: int, is_dismiss: bool=False) -> None:
        """
        退出群组
        """
        self.add("/set_group_leave", {
            "group_id":group_id,
            "is_dismiss": is_dismiss,
        })
    
    def set_group_special_title(self, group_id, user_id, special_title="", duration=-1):
        """
        设置群组专属头衔
        """
        self.add("/set_group_special_title", {
            "group_id":group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        })

    def set_friend_add_request(self, flag, approve, remark):
        """
        处理加好友请求
        """
        self.add("/set_friend_add_request", {
            "flag":flag,
            "approve": approve,
            "remark": remark,
        })
    
    def set_group_add_request(self, flag, sub_type, approve=True, reason=""):
        """
        处理加群请求／邀请
        """
        self.add("/set_group_add_request", {
            "flag":flag,
            "approve": approve,
            "sub_type": sub_type,
            "reason": reason
        })
    
    def get_msg(self, message_id):
        """
        获取消息
        """
        return self._link("/get_msg", {
            "message_id": message_id,
        })

    def get_group_info(self, group_id: int, no_cache: bool = False):
        """
        获取群信息
        """
        return self._link("/get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        })
    
    def get_group_msg_history(self, message_seq: int, group_id: int):
        """
        获取群消息历史记录
        """
        return self._link("/get_group_msg_history", data={
            "message_seq": message_seq,
            "group_id": group_id
        })
    
    def get_group_list(self, no_cache: bool = False):
        """
        获取群列表
        """
        return self._link("/get_group_list", {
            "no_cache": no_cache,
        })

    def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False):
        """
        获取群成员信息
        """
        return self._link("/get_group_member_info", {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache,
        })

    def get_group_member_list(self, group_id: int, no_cache: bool = False):
        """
        获取群成员列表
        """
        return self._link("/get_group_member_list", {
            "group_id": group_id,
            "no_cache": no_cache,
        })
    
    def get_group_honor_info(self, group_id: int, type: str):
        """
        获取群荣誉信息
        """
        return self._link("/get_group_honor_info", {
            "group_id": group_id,
            "type": type,
        })
    
    def get_group_system_msg(self):
        """
        获取群系统消息
        """
        return self._link("/get_group_system_msg")

    def get_essence_msg_list(self, group_id: int):
        """
        获取精华消息列表
        """
        return self._link("/get_essence_msg_list", {
            "group_id": group_id,
        })

    def get_group_at_all_remain(self, group_id: int):
        """
        获取群 @全体成员 剩余次数
        """
        return self._link("/get_group_at_all_remain", {
            "group_id": group_id,
        })
    
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
        return self._link("/get_stranger_info", {
            "user_id": user_id,
            "no_cache": no_cache
        })
    
    def get_friend_list(self):
        """
        获取好友列表
        """
        return self._link("/get_friend_list")

    def get_unidirectional_friend_list(self):
        """
        获取单向好友列表
        """
        return self._link("/get_unidirectional_friend_list")
    
    def get_image(self, file):
        """
        获取图片信息
        """
        return self._link("/get_image", {
            "file": file
        })

    def can_send_image(self):
        """
        检查是否可以发送图片
        """
        return self._link("/can_send_image")

    def ocr_image(self, image: str):
        """
        图片 OCR
        """
        return self._link("/ocr_image", {
            "image": image
        })

    def get_record(self, file: str, out_format: str):
        """
        获取语音 (该 API 暂未被 go-cqhttp 支持)
        """
        return self._link("/get_record", {
            "file": file,
            "out_format": out_format
        })
    
    def can_send_record(self):
        """
        检查是否可以发送语音
        """
        return self._link("/can_send_record")
    
    def delete_msg(self, message_id):
        """
        撤回消息
        """
        self.add("/delete_msg", {
            "message_id": message_id
        })

    def delete_friend(self, user_id: int):
        """
        删除好友
        """
        self.add("/delete_msg", {
            "user_id": user_id
        })

    def delete_unidirectional_friend(self, user_id: int):
        """
        删除单向好友
        """
        self.add("/delete_unidirectional_friend", {
            "user_id": user_id
        })

    def mark_msg_as_read(self, message_id: int):
        """
        标记消息已读
        """
        self.add("/mark_msg_as_read", {
            "message_id": message_id
        })

    async def _cqhttp_download_file(self, url, headers):
        """
        go-cqhttp 的内置下载 (异步)
        """
        return (await self._asynclink("/download_file", {
            "url":url,
            "headers": headers,
            "thread_count": self.thread_count
        }))["data"]["file"]
    
    def cqhttp_download_file(self, url, headers):
        """
        go-cqhttp 的内置下载
        """
        return self._link("/download_file", {
            "url":url,
            "headers": headers,
            "thread_count": self.thread_count
        })["file"]
    
    def get_status(self):
        """
        获取 go-cqhttp 状态
        """
        return self._link("/get_status")
    
    def upload_group_file(self, group_id, file, name, folder=None):
        """
        上传群文件
        """
        post_data = {
            "group_id": group_id,
            "file": "file://%s" % file,
            "name": name
        }

        if folder is not None:
            post_data["folder"] = folder

        self.add("/upload_group_file", post_data)
    
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


class cqBot(cqEvent):
    """
    cqBot 机器人
    """
    def __init__(self, cqapi: cqHttpApi, host: str="ws://127.0.0.1:8080", group_id_list: list[int]=[], user_id_list: list[int]=[], options: dict[str, Union[list, str, int]]={}):

        self.cqapi = cqapi
        self.__plugin_list: list[object] = []
        # 指令列表
        self.__commandList: dict[str, dict] = {}
        # 定时任务
        self.__timingList: dict[str, dict] = {}
        # bot qq
        self.__bot_qq: int= 0
        # 需处理群
        self.group_id_list: list[int] = group_id_list
        # 需处理私信
        self.user_id_list: list[int] = user_id_list
        # 管理员列表
        self.admin: list[int] = []
        # 指令标志符
        self.commandSign: str = "#"
        # 帮助信息模版
        self.help_text_format: str = "本bot帮助信息!\n{help_command_text}\npycqbot {__VERSIONS__}"
        self.help_command_text: str = ""
        # 长效消息存储
        self.messageSql: bool = False
        # 长效消息存储 数据库目录
        self.messageSqlPath: str = "./"
        # 长效消息存储 清理间隔
        self.messageSqlClearTime: int = 60
        # go_cqhttp 状态 通过心跳更新
        self._go_cqhttp_status: dict = {}

        # 以下参数只有在启用时设置有效
        # websocket 会话 地址
        self.__host = host
        self._websocket_start_in = True

        self.reconnection_sleep = 10
        self.reconnection = 3

        for key in options.keys():
            if type(options[key]) is str:
                exec("self.%s = '%s'" % (key, options[key]))
            else:
                exec("self.%s = %s" % (key, options[key]))

        """
        内置指令 help
            显示帮助信息
        """

        def print_help(_, message: Message):
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
        
        def status(_, message: Message):
            if self._go_cqhttp_status == {}:
                self.cqapi.send_reply(message, "go-cqhttp 心跳未被正常配置，请检查")
                logging.warning("go-cqhttp 心跳未被正常配置")
                return

            status_msg = "bot (qq=%s) 是否在线：%s\n收到数据包：%s\n发送数据包：%s\n丢失数据包：%s\n接受信息：%s\n发送信息：%s\nTCP 链接断开：%s\n账号掉线次数：%s\n最后消息时间：%s" % (
                self.__bot_qq,
                self._go_cqhttp_status["online"],
                self._go_cqhttp_status["stat"]["packet_received"],
                self._go_cqhttp_status["stat"]["packet_sent"],
                self._go_cqhttp_status["stat"]["packet_lost"],
                self._go_cqhttp_status["stat"]["message_received"],
                self._go_cqhttp_status["stat"]["message_sent"],
                self._go_cqhttp_status["stat"]["disconnect_times"],
                self._go_cqhttp_status["stat"]["lost_times"],
                self._go_cqhttp_status["stat"]["last_message_time"],
            )

            message.reply(status_msg)
        
        self.command(status, "status", {
            "type": "all",
            "admin": True,
            "help": [
                self.commandSign + "status - 获取 go-cqhttp 状态",
            ]
        })

    def cqhttp_log_print(self, shell_msg: str) -> None:
        try:
            shell_msg_data = shell_msg.split(": ", maxsplit=1)[1]
        except IndexError:
            print(shell_msg)
            return

        if "INFO" in shell_msg:
            logging.info(shell_msg_data)
            return

        if "WARNING" in shell_msg:
            logging.warning("go-cqhttp 警告 %s" % shell_msg_data)
            return
        
        if "DEBUG" in shell_msg:
            logging.debug(shell_msg_data)
            return
        
        if "ERROR" in shell_msg:
            logging.error("go-cqhttp 发生错误 %s" % shell_msg_data)
            return

        if "FATAL" in shell_msg:
            logging.error("go-cqhttp 发生致命错误 %s" % shell_msg_data)
            return
        
        print(shell_msg[-1])

    def _set_config(self, go_cqhttp_path) -> None:
        config_path = os.path.join(go_cqhttp_path, "./config.yml")
        if not os.path.isfile(config_path):
            with open(config_path, "w", encoding="utf8") as file:
                file.write(pycqBot.GO_CQHTTP_CONFIG)

    def start(self, go_cqhttp_path: str="./", print_error: bool=True, start_go_cqhttp: bool=True)  -> None:
        print(pycqBot.TIT)
        """
        运行 go-cqhttp 并连接 websocket 会话
        """
        def cqhttp_start():
            self._set_config(go_cqhttp_path)
            plat = platform.system().lower()
            if plat == 'windows':
                subp = subprocess.Popen("cd %s && .\go-cqhttp.exe -faststart" % go_cqhttp_path, shell=True, stdout=subprocess.PIPE)
            elif plat == 'linux':
                subp = subprocess.Popen("cd %s && ./go-cqhttp -faststart" % go_cqhttp_path, shell=True, stdout=subprocess.PIPE)

            while True:
                shell_msg = subp.stdout.readline().decode("utf-8").strip()
                if shell_msg.strip() == "":
                    continue

                if "CQ WebSocket 服务器已启动" in shell_msg:
                    self._websocket_start_in = False
                
                if print_error and "INFO" not in shell_msg:
                    self.cqhttp_log_print(shell_msg)
                elif not print_error:
                    self.cqhttp_log_print(shell_msg)
        
        try:
            if not start_go_cqhttp:
                self._websocket_start()
                return

            thread = Thread(target=cqhttp_start, name="cqhttp_shell")
            thread.setDaemon(True)
            thread.start()

            while self._websocket_start_in:
                time.sleep(0.5)
                pass

            self._websocket_start()
        except KeyboardInterrupt:
            print("\n")
    
    def _websocket_start(self) -> None:
        """
        连接 websocket 会话
        """
        old_reconnection = self.reconnection
        async def main_logic():
            while self.reconnection != -1:
                try:
                    logging.info("正在连接 go-cqhttp websocket 服务")
                    # 只接收 event
                    async with websockets.connect(self.__host) as websocket:
                        self.reconnection = old_reconnection
                        while 1:
                            try:
                                self._on_message(await websocket.recv())
                            except ConnectionClosedError as crerr:
                                logging.warning(crerr)
                                break

                            except Exception as err:
                                self.on_error(err)

                except ConnectionRefusedError as crerr:
                    logging.warning(crerr)

                self.reconnection -= 1
                logging.warning(f"{self.reconnection_sleep}秒后 重新连接 websocket 服务 ({old_reconnection - self.reconnection}/{old_reconnection})")
                time.sleep(self.reconnection_sleep)
            
            logging.fatal(f"无法连接 websocket 服务 host: {self._host}")
        
        try:
            asyncio.run(main_logic())
        except KeyboardInterrupt:
            print("\n")

    @staticmethod
    def _import_plugin_config() -> dict:
        if os.path.isfile("./plugin_config.yml"):
            with open("./plugin_config.yml", "r", encoding="utf8") as file:
                return yaml.safe_load(file.read())
        else:
            with open("./plugin_config.yml", "w", encoding="utf8") as file:
                file.write("# 插件配置")

        return {}
    
    def _import_plugin(self, plugin: str, plugin_config: dict) -> None:
        try:
            if plugin.rsplit(".", maxsplit=1)[0] == "pycqBot.plugin":
                plugin = plugin.rsplit(".", maxsplit=1)[-1]
                plugin_obj = importlib.import_module(f"pycqBot.plugin.{plugin}.{plugin}")
            else:
                plugin_obj = importlib.import_module(f"plugin.{plugin}.{plugin}")

            if eval(f"plugin_obj.{plugin}.__base__.__name__ != 'Plugin'"):
                logging.warning("%s 插件未继承 pycqBot.Plugin 不进行加载" % plugin)
                del plugin_obj
                return
            
            if plugin not in plugin_config:
                plugin_config[plugin] = {}

            plugin_obj = eval(f"plugin_obj.{plugin}(self, self.cqapi, plugin_config[plugin])")
            self.__plugin_list.append(plugin_obj)

            logging.debug(f"{plugin} 插件加载完成")
        except ModuleNotFoundError:
            self.pluginNotFoundError(plugin)
        except Exception as err:
            self.pluginImportError(plugin, err)
    
    def _plugin_event_run(self, event_name: str, *args) -> None:
        for plugin_obj in self.__plugin_list:
            exec(f'plugin_obj.{event_name}(*args)')

    def plugin_load(self, plugin: Union[str, list[str]]) -> "cqBot":
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
        
        return self
    
    def pluginNotFoundError(self, plugin: str) -> None:
        """
        插件不存在
        """
        logging.error("plugin 目录下不存在插件 %s " % plugin)
    
    def pluginImportError(self, plugin: str, err: Exception) -> None:
        """
        加载插件时发生错误
        """
        logging.error("加载插件 %s 时发生错误: %s" % (plugin, err))
        logging.exception(err)

    
    def _on_message(self, message_data: str) -> tuple[str, Optional[Event]]:
        """
        处理数据不建议修改, 错误修改将导致无法运行
        除非已经了解如何工作
        """
        try:
            event = _get_event(message_data)
        except TypeError as err:
            logging.warning(err)
            return "", None
        
        event_name = event.get_event_name()
        logging.debug("go-cqhttp 上报 %s 事件: %s" % (event_name, event.data))

        if event_name in cqEvent.EVENT:
            if type(event) is Message_Event:
                message = event.get_message(self.cqapi)

                exec("self.%s(message)" % event_name)
                self._plugin_event_run(event_name, message)
            else:
                exec("self.%s(event)" % event_name)
                self._plugin_event_run(event_name, event)

            return event_name, event
        else:
            logging.warning("未知数据协议:%s" % event_name)
        
        return "", None

    def on_error(self, error: Exception) -> None:
        """
        websocket 会话错误
        """
        logging.exception(error)
        
    def _check_command_options(self, options: dict[str, Any]) -> dict[str, Any]:
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
            
            self.help_text = "%s\n" % self.help_text_format.format(help_command_text=self.help_command_text, __VERSIONS__=pycqBot.__VERSIONS__)
        
        return options
    
    def _check_timing_options(self, options: dict[str, Any], timing_name: str) -> Optional[dict[str, Any]]:
        options["name"] = timing_name

        if "timeSleep" not in options:
            logging.warning("定时任务 %s 没有指定 timeSleep 间隔, 中止创建" % timing_name)
            return None

        if "ban" not in options:
            options["ban"] = []

        return options
        
    def command(self, function: Callable[[list[str], Message], None], command_name: Union[str, list[str]], options: dict[str, Any]=None) -> "cqBot":
        if options is None:
            options = {}
            
        options = self._check_command_options(options)

        if type(command_name) == str:
            command_name = [command_name]

        for name in command_name:
            self.__commandList[name] = options
            self.__commandList[name]["function"] = function

        return self

    def _timing_job(self, job: dict[str, Any]) -> None:
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
    
    def timing(self, function: Callable[[int], None], timing_name: str, options: dict[str, Any]=None) -> "cqBot":
        if options is None:
            options = {}

        ck_options = self._check_timing_options(options, timing_name)
        if ck_options is None:
            return self

        options = ck_options
        if not options:
            return self

        options["function"] = function
        self.__timingList[timing_name] = options

        thread = Thread(target=self._timing_job, args=(self.__timingList[timing_name],), name=timing_name)
        thread.setDaemon(True)
        thread.start()

        logging.info("创建定时任务 %s " % timing_name)

        return self
    
    def set_bot_status(self, event: Meta_Event) -> None:
        self.__bot_qq = event.data["self_id"]
        self.cqapi.bot_qq = event.data["self_id"]
    
    def meta_event_lifecycle_connect(self, event: Meta_Event):
        """
        连接响应
        """
        self.set_bot_status(event)
        if self.messageSql is True:
            self.cqapi._create_sql_link(self.messageSqlPath, self.messageSqlClearTime)

        logging.info("成功连接 websocket 服务! bot qq:%s" % self.__bot_qq)
    
    def meta_event_heartbeat(self, event: Meta_Event):
        """
        心跳
        """
        self.set_bot_status(event)
        self._go_cqhttp_status = event.data["status"]
        logging.debug("websocket 心跳: %s" % event.data)

    def meta_event(self, event: Meta_Event):
        """
        生命周期
        """
        logging.debug("生命周期: %s" % event.data)
    
    
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

    def user_log_srt(self, message: Union[Private_Message, Group_Message]):
        user_id = message.sender.id

        if type(message) is Private_Message:
            user_name = message.sender.nickname
        elif type(message) is Group_Message:
            if message.anonymous == None:
                if message.sender.card.strip() != '':
                    user_name = message.sender.card
                else:
                    user_name = message.sender.nickname
            else:
                user_name = "匿名用户 - %s flag: %s" % (message.anonymous["name"],
                    message.anonymous["flag"])

        if type(message) is Group_Message:
            return "%s (qq=%s,群号=%s)" % (user_name, user_id, message.group_id)

        return "%s (qq=%s)" % (user_name, user_id)

    def _set_command_key(self, message: str):
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
    
    def _check_command(self, message: Union[Private_Message, Group_Message]):
        """
        指令检查
        """

        commandSign, command, commandData = self._set_command_key(message.message)

        if commandSign != self.commandSign:
            return False
        
        if command not in self.__commandList:
            self.notCommandError(message)
            return False

        if self.__commandList[command]["type"] != message.event.message_type and self.__commandList[command]["type"] != "all":
            return False
        
        self.check_command(message)
        
        if message.event is Group_Message:

            if message.group_id in self.__commandList[command]["ban"]:
                self.banCommandError(message)
                return False
            
            user_list = self.__commandList[command]["user"]
            if user_list[0] != "all":

                if message.anonymous is not None and "anonymous" not in user_list:
                    self.userPurviewError(message)
                    return False
                
                if message.sender.role not in user_list or user_list[0] != "nall":
                    self.userPurviewError(message)
                    return False

        if self.__commandList[command]["admin"] and message.sender.id not in self.admin:
            self.purviewError(message)
            return False

        return commandSign, command, commandData
    
    def _run_command(self, message: Message):
        """
        指令运行
        """
        def run_command(message):
            try:
                commandIn = self._check_command(message)
                if not commandIn:
                    return

                commandSign, command, commandData = commandIn
                self.__commandList[command]["function"](commandData, message)

            except Exception as err:
                self.runCommandError(message, err)
        
        thread = Thread(target=run_command, args=(message, ), name="command")
        thread.setDaemon(True)
        thread.start()

    def check_command(self, message: Message):
        """
        指令开始检查勾子
        """
        logging.info("%s 使用指令: %s" % (self.user_log_srt(message), message.message))
    
    def _message(self, message: Message) -> Message:
        """
        通用消息处理
        """
        # 检查等待回复
        if self.cqapi._reply_ck(message.sender.id):
            self.cqapi._reply_add(message.sender.id, message)
        
        return message
    
    def _message_run(self, message: Message) -> Message:
        message = self._message(message)
        self._plugin_event_run(f"on_{message.event.message_type}_msg", message)
        self._run_command(message)

        return message


    def _message_private(self, message: Private_Message) -> Optional[Private_Message]:
        """
        通用私聊消息处理
        """
        if (message.sender.id not in self.user_id_list) and self.user_id_list != []:
            return None

        message = self._message_run(message)
        self.on_private_msg(message)

        return message
    
    def _message_group(self, message: Group_Message) -> Optional[Group_Message]:
        """
        通用群消息处理
        """
        if message.group_id not in self.group_id_list and self.group_id_list != []:
            return None

        message = self._message_run(message)
        self.on_group_msg(message)

        for cqCode in message.code:
            if cqCode["type"] == "at":
                if cqCode["data"]["qq"] == str(self.__bot_qq):
                    self.at_bot(message, message.code, cqCode)
                    self._plugin_event_run("at_bot", message, message.code, cqCode)
                    continue
                
                self.at(message, message.code, cqCode)
                self._plugin_event_run("at", message, message.code, cqCode)

        return message
    
    def _bot_message_log(self, log, message):
        logging.info(log)
        self.cqapi.send_reply(message, log)
    
    def at_bot(self, message: Group_Message, cqCode_list, cqCode):
        """
        接收到 at bot
        """
        logging.info("接收到 at bot %s " % self.user_log_srt(message))

    def message_private_friend(self, message: Private_Message):
        """
        好友私聊消息
        """
        self._message_private(message)
    
    def message_private_group(self, message: Private_Message):
        """
        群临时会话私聊消息
        """
        self._message_private(message)

    def message_sent_private_friend(self, message: Private_Message):
        """
        自身消息私聊上报
        """
        self._message_private(message)

    def message_group_anonymous(self, message: Group_Message):
        """
        群匿名消息
        """
        self._message_group(message)

    def message_sent_group_normal(self, message: Group_Message):
        self._message_group(message)
    
    def message_private_group_self(self, message: Group_Message):
        """
        群中自身私聊消息
        """
        self._message_private(message)
    
    def message_private_other(self, message: Private_Message):
        """
        私聊消息
        """
        self._message_private(message)

    def message_group_normal(self, message: Group_Message):
        """
        群消息
        """
        self._message_group(message)
    
    def notCommandError(self, message: Message):
        """
        指令不存在时错误
        """
        # commandSign 为空时不处理 不然每一条消息都会调用 notCommandError ...
        if self.commandSign == "":
            return

        self._bot_message_log("指令 %s 不存在..." % message.message, message)
    
    def banCommandError(self, message: Message):
        """
        指令被禁用时错误
        """
        self._bot_message_log("指令 %s 被禁用!" % message.message, message)
    
    def userPurviewError(self, message: Message):
        """
        指令用户组权限不足时错误
        """
        self._bot_message_log("%s 用户组权限不足... 指令 %s" % (self.user_log_srt(message), message.message), message)
    
    def purviewError(self, message: Message):
        """
        指令权限不足时错误 (bot admin)
        """
        self._bot_message_log("%s 权限不足... 指令 %s" % (self.user_log_srt(message), message.message), message)
    
    def runCommandError(self, message: Message, err: Exception):
        """
        指令运行时错误
        """
        self._bot_message_log("指令 %s 运行时错误... Error: %s" % (message.message, err), message)
        logging.exception(err)
    
    def notice_group_decrease_kick_me(self, event: Notice_Event):
        """
        群成员减少 - 登录号被踢
        """
        if event.data["group_id"] in self.group_id_list:
            self.group_id_list.remove(event.data["group_id"])

        async def _notice_group_decrease_kick_me(message):
            user_data = await self.cqapi._asynclink("/get_stranger_info", {
                "user_id": event.data["operator_id"]
            })

            if user_data is None:
                return
            
            logging.info("bot 被 %s (qq=%s) T出群 %s" % (user_data["data"]["nickname"], user_data["data"]["user_id"], event.data["group_id"]))

        self.cqapi.add_task(_notice_group_decrease_kick_me(event))


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