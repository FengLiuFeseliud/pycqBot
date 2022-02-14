import json
import os
import sys
from threading import Lock, Thread
import time
import websocket

class cqSocket:

    def __init__(self, bot, ip="127.0.0.1", port=5700, debug=False):
        self.__port = port
        self.__ip = ip
        self.debug = debug
        """
        go-cqhttp 事件
        响应值查看: https://docs.go-cqhttp.org/event
        """
        self.__event = {
            # 好友私聊消息
            "message_private_friend": bot.message_private_friend,
            # 群临时会话私聊消息
            "message_private_group": bot.message_private_group,
            # 群中自身私聊消息
            "message_private_group_self": bot.message_private_group_self,
            # 私聊消息
            "message_private_other": bot.message_private_other,
            # 群消息
            "message_group_normal": bot.message_group_normal,
            "message_group_anonymous": bot.message_group_normal,
            # 群文件上传
            "notice_group_upload": bot.notice_group_upload,
            # 群管理员变动
            "notice_group_admin_set": bot.notice_group_admin_set,
            "notice_group_admin_unset": bot.notice_group_admin_unset,
            # 群成员减少
            "notice_group_decrease_leave": bot.notice_group_decrease_leave,
            "notice_group_decrease_kick": bot.notice_group_decrease_kick,
            "notice_group_decrease_kickme": bot.notice_group_decrease_kickme,
            # 群成员增加
            "notice_group_increase_approve": bot.notice_group_increase_approve,
            "notice_group_increase_invite": bot.notice_group_increase_invite,
            # 群禁言
            "notice_group_ban_ban": bot.notice_group_ban_ban,
            "notice_group_ban_lift_ban": bot.notice_group_ban_lift_ban,
            # 群消息撤回
            "notice_group_recall": bot.notice_group_recall,
            # 群红包运气王提示
            "notice_notify_lucky_king": bot.notice_notify_lucky_king,
            # 群成员荣誉变更提示
            "notice_notify_honor": bot.notice_notify_honor,
            # 群成员名片更新
            "notice_group_card": bot.notice_group_card,
            # 好友添加
            "notice_friend_add": bot.notice_friend_add,
            # 好友消息撤回
            "notice_friend_recall": bot.notice_friend_recall,
            # 好友/群内 戳一戳
            "notice_notify_poke": bot.notice_notify_poke,
            # 接收到离线文件
            "notice_offline_file": bot.notice_offline_file,
            # 其他客户端在线状态变更
            "notice_client_status": bot.notice_client_status,
            # 精华消息添加
            "notice_essence_add": bot.notice_essence_add,
            # 精华消息移出
            "notice_essence_delete": bot.notice_essence_delete,
            # 加好友请求
            "request_friend": bot.request_friend,
            # 加群请求
            "request_group_add": bot.request_group_add,
            # 加群邀请
            "request_group_invite": bot.request_group_invite,
            # 连接响应
            "meta_event_connect": bot.meta_event_connect,
        }

        self.link()
    
    def link(self):
        def websocketThread():
            if self.debug:
                websocket.enableTrace(True)
            
            wsapp = websocket.WebSocketApp("ws://%s:%s" % (self.__ip, self.__port),
                    on_message=self.on_message, 
                    on_error=self.on_error,
                    on_open=self.on_open,
                )
            # 打开连接
            wsapp.run_forever()
        
        thread = Thread(target=websocketThread, name="websocketThread")
        thread.setDaemon(True)
        thread.start()
    
    def set_event_name(self, message):
        event_name = message["post_type"]

        if "message_type" in message:
            event_name += "_" + message["message_type"]
        elif "notice_type" in message:
            event_name += "_" + message["notice_type"]
        elif "request_type" in message:
            event_name += "_" + message["request_type"]
        
        if "sub_type" in message:
            event_name += "_" + message["sub_type"]
        
        return event_name


    def on_message(self, wsapp, message):
        data = json.loads(message)
        
        event_name = self.set_event_name(data)
        if event_name in self.__event:
            self.__event[event_name](data)
        else:
            print("未知数据协议:%s" % event_name)

    def on_open(self, wsapp):
        print("正在连接 go-cqhttp websocket 服务")

    def on_error(self, wsapp, error):
        print(error)