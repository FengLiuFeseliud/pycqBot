import json
import logging
import platform
import subprocess
from threading import Thread
import time
import websocket
import asyncio
import aiohttp
import aiofiles
import os


# 默认生成框架 cgo-cqhttp 配置
GO_CQHTTP_CONFIG = """# go-cqhttp 详细配置见 go-cqhttp 文档 https://docs.go-cqhttp.org/guide/config
account:
    encrypt: false
    status: 0
    relogin:
        delay: 3
        interval: 3
        max-times: 0
    use-sso-address: true
    allow-temp-session: true

heartbeat:
    interval: 40

message:
    post-format: string
    ignore-invalid-cqcode: false
    force-fragment: false
    fix-url: false
    proxy-rewrite: ''
    report-self-message: false
    remove-reply-at: false
    extra-reply-data: false
    skip-mime-scan: false

output:
    log-level: trace
    log-aging: 15
    log-force-new: true
    log-colorful: true
    debug: false

default-middlewares: &default
    access-token: ''
    filter: ''
    rate-limit:
        enabled: false 
        frequency: 1
        bucket: 1

database:
    leveldb:
        enable: true

    cache:
        image: data/image.db
        video: data/video.db

servers:
    - http:
        host: 127.0.0.1
        port: 8000
        timeout: 5
        middlewares:
            <<: *default
        post:

    - ws:
        host: 127.0.0.1
        port: 5700
        middlewares:
            <<: *default
"""


class cqSocket:
    """
    cqSocket cqBot 基类开启 websocket 会话
        并为 cqBot 提供事件响应
        无法单独使用
    """

    def __init__(self, host):
        # 以下参数只有在启用时设置有效
        # websocket 会话 地址
        self._host = host
        # websocket 会话 debug
        self._debug = False
        self._websocket_start_in = True

        """
        go-cqhttp 事件
        响应值查看: https://docs.go-cqhttp.org/event
        """
        self.__event = {
            # 好友私聊消息
            "message_private_friend": self.message_private_friend,
            # 群临时会话私聊消息
            "message_private_group": self.message_private_group,
            # 群中自身私聊消息
            "message_private_group_self": self.message_private_group_self,
            # 私聊消息
            "message_private_other": self.message_private_other,
            # 群消息
            "message_group_normal": self.message_group_normal,
            "message_group_anonymous": self.message_group_normal,
            # 群文件上传
            "notice_group_upload": self.notice_group_upload,
            # 群管理员变动
            "notice_group_admin_set": self.notice_group_admin_set,
            "notice_group_admin_unset": self.notice_group_admin_unset,
            # 群成员减少
            "notice_group_decrease_leave": self.notice_group_decrease_leave,
            "notice_group_decrease_kick": self.notice_group_decrease_kick,
            "notice_group_decrease_kickme": self.notice_group_decrease_kickme,
            # 群成员增加
            "notice_group_increase_approve": self.notice_group_increase_approve,
            "notice_group_increase_invite": self.notice_group_increase_invite,
            # 群禁言
            "notice_group_ban_ban": self.notice_group_ban_ban,
            "notice_group_ban_lift_ban": self.notice_group_ban_lift_ban,
            # 群消息撤回
            "notice_group_recall": self.notice_group_recall,
            # 群红包运气王提示
            "notice_notify_lucky_king": self.notice_notify_lucky_king,
            # 群成员荣誉变更提示
            "notice_notify_honor": self.notice_notify_honor,
            # 群成员名片更新
            "notice_group_card": self.notice_group_card,
            # 好友添加
            "notice_friend_add": self.notice_friend_add,
            # 好友消息撤回
            "notice_friend_recall": self.notice_friend_recall,
            # 好友/群内 戳一戳
            "notice_notify_poke": self.notice_notify_poke,
            # 接收到离线文件
            "notice_offline_file": self.notice_offline_file,
            # 其他客户端在线状态变更
            "notice_client_status": self.notice_client_status,
            # 精华消息添加
            "notice_essence_add": self.notice_essence_add,
            # 精华消息移出
            "notice_essence_delete": self.notice_essence_delete,
            # 加好友请求
            "request_friend": self.request_friend,
            # 加群请求
            "request_group_add": self.request_group_add,
            # 加群邀请
            "request_group_invite": self.request_group_invite,
            # 连接响应
            "meta_event_connect": self.meta_event_connect,
            # 心跳
            "meta_event": self.meta_event
        }
    
    def cqhttp_log_print(self, shell_msg):
        shell_msg = shell_msg.split(": ", maxsplit=1)

        if "INFO" in shell_msg[0]:
            logging.info(shell_msg[-1])
            return

        if "WARNING" in shell_msg[0]:
            logging.warning("go-cqhttp %s" % shell_msg[-1])
            return

        if "FATAL" in shell_msg[0]:
            logging.error("go-cqhttp 发生错误 %s" % shell_msg[-1])
            return
        
        print(shell_msg[-1])

    def _set_config(self, go_cqhttp_path):
        config_path = os.path.join(go_cqhttp_path, "./config.yml")
        if not os.path.isfile(config_path):
            with open(config_path, "w", encoding="utf8") as file:
                file.write(GO_CQHTTP_CONFIG)

    def start(self, go_cqhttp_path="./", print_error=True, start_go_cqhttp=True):
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
    
    def _websocket_start(self):
        """
        连接 websocket 会话
        """
        if self._debug:
            websocket.enableTrace(True)
        
        wsapp = websocket.WebSocketApp(self._host,
                on_message=self._on_message, 
                on_error=self.on_error,
                on_open=self.on_open,
            )
        # 打开连接
        wsapp.run_forever()
    
    def _set_event_name(self, message):
        """
        检查事件类型并返回对应事件名
        """
        event_name = message["post_type"]

        if "message_type" in message:
            event_name = "%s_%s" % (event_name, message["message_type"])
        elif "notice_type" in message:
            event_name = "%s_%s" % (event_name, message["notice_type"])
        elif "request_type" in message:
            event_name = "%s_%s" % (event_name, message["request_type"])
        
        if "sub_type" in message:
            event_name = "%s_%s" % (event_name, message["sub_type"])
        
        return event_name


    def _on_message(self, wsapp, message):
        """
        处理数据不建议修改, 错误修改将导致无法运行
        除非已经了解如何工作
        """
        data = json.loads(message)
        
        event_name = self._set_event_name(data)
        if event_name in self.__event:
            self.__event[event_name](data)

            return event_name
        else:
            logging.warning("未知数据协议:%s" % event_name)

    def on_open(self, wsapp):
        """
        准备打开 websocket 会话
        """
        logging.info("正在连接 go-cqhttp websocket 服务")

    def on_error(self, wsapp, error):
        """
        websocket 会话错误
        """
        logging.exception(error)


class asyncHttp:

    def __init__(self, download_path="./download", chunk_size=1024) -> None:
        self._loop = asyncio.new_event_loop()
        self._session = aiohttp.ClientSession(loop=self._loop)
        self._download_path = download_path
        self.chunk_size = chunk_size

        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        
        self.__asyncHttp_loop()

    async def _download_file(self, file_name, file_url):
        try:
            async with self._session.get(file_url) as req:
                if req.status != 200:
                    self.downloadFileError(file_name, file_url, req.status)
                    return

                async with aiofiles.open("%s/%s" % (self._download_path, file_name), "wb") as file:
                    async for chunk in req.content.iter_chunked(self.chunk_size):
                        await file.write(chunk)
                    
                    self.download_end(file_name, file_url, req.status)
        except Exception as err:
            self.downloadFileRunError(err)
    
    async def _asynclink(self, api, data={}):
        json = await self.link("%s%s" % (self.http, api), mod="post", data=data)
        logging.debug("cqAPI 响应: %s" % json)
        if json == {}:
            return
            
        if json["retcode"] != 0:
            self.apiLinkError(json)
        
        return json

    async def link(self, url, mod="get", data={}, json=True, allow_redirects=False, proxy=None, headers={}, encoding=None):
        if encoding is None:
            encoding = "utf-8"
            
        try:
            if mod == "get":
                async with self._session.get(url, data=data, allow_redirects=allow_redirects, proxy=proxy, headers=headers) as req:
                    if json:
                        data = await req.json(encoding=encoding)
                    else:
                        data = await req.text(encoding=encoding)
            
            if mod == "post":
                async with self._session.post(url, data=data, allow_redirects=allow_redirects, proxy=proxy, headers=headers) as req:
                    if json:
                        data = await req.json(encoding=encoding)
                    else:
                        data = await req.text(encoding=encoding)
            
            return data
        except Exception as err:
            self.apiLinkRunError(err)
    
    def add_task(self, coroutine):
        asyncio.run_coroutine_threadsafe(coroutine, self._loop)
    
    def add(self, api, data={}):
        asyncio.run_coroutine_threadsafe(self._asynclink(api, data), self._loop)

    def download_path(self, download_path):
        if not os.path.isdir(download_path):
            os.makedirs(download_path)

        self._download_path = download_path
    
    def __asyncHttp_loop(self):
        def task_loop_():
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()

        thread = Thread(target=task_loop_, name="asyncHttp_loop")
        thread.setDaemon(True)
        thread.start()

    async def _download_img(self, file):
        post_data = {
            "file": file
        }
        img_file = (await self._asynclink("/get_image", data=post_data))["data"]
        await self._download_file(img_file["filename"], img_file["url"])

    def download_file(self, file_name, file_url):
        asyncio.run_coroutine_threadsafe(self._download_file(file_name, file_url), self._loop)
    
    def download_img(self, file):
        asyncio.run_coroutine_threadsafe(self._download_img(file), self._loop)
    
    def download_end(self, file_name, file_url, code):
        """
        下载完成
        """
        logging.info("%s 下载完成! code: %s" % (file_name, code))

    def downloadFileError(self, file_name, file_url, code):
        """
        下载失败
        """
        logging.error("%s 下载失败... code: %s" % (file_name, code))
    
    def downloadFileRunError(self, err):
        """
        下载时发生错误
        """
        logging.error("下载文件时发生错误 Error: %s" % err)
        logging.exception(err)
    
    def apiLinkError(self, err_json):
        """
        cqapi发生错误
        """
        logging.error("api 发生错误 %s: %s code: %s" % (err_json["msg"], err_json["wording"], err_json["retcode"]))
    
    def apiLinkRunError(self, err):
        """
        cqapi请求时发生错误
        """
        logging.error("api 请求发生错误 Error: %s" % err)
        logging.exception(err)