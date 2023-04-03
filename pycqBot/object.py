from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pycqBot import cqBot, cqHttpApi
    from pycqBot.data.message import Group_Message, Private_Message, Message
    from pycqBot.data.event import Message_Event, Meta_Event, Notice_Event, Request_Event

class cqEvent:
    """
    go-cqhttp 事件
    响应值查看: https://docs.go-cqhttp.org/event
    """
    
    EVENT = [
            # 好友私聊消息
            "message_private_friend",
            # 群临时会话私聊消息
            "message_private_group",
            # 群中自身私聊消息
            "message_private_group_self",
            # 私聊消息
            "message_private_other",
            # 群消息
            "message_group_normal",
            "message_group_anonymous",
            # 自身群消息上报
            "message_sent_group_normal",
            # 自身消息私聊上报
            "message_sent_private_friend",
            # 群文件上传
            "notice_group_upload",
            # 群管理员变动
            "notice_group_admin_set",
            "notice_group_admin_unset",
            # 群成员减少
            "notice_group_decrease_leave",
            "notice_group_decrease_kick",
            "notice_group_decrease_kick_me",
            # 群成员增加
            "notice_group_increase_approve",
            "notice_group_increase_invite",
            # 群禁言
            "notice_group_ban_ban",
            "notice_group_ban_lift_ban",
            # 群消息撤回
            "notice_group_recall",
            # 群红包运气王提示
            "notice_notify_lucky_king",
            # 群成员荣誉变更提示
            "notice_notify_honor",
            # 群成员名片更新
            "notice_group_card",
            # 群成员头衔变更
            "notice_notify_title",
            # 好友添加
            "notice_friend_add",
            # 好友消息撤回
            "notice_friend_recall",
            # 好友/群内 戳一戳
            "notice_notify_poke",
            # 接收到离线文件
            "notice_offline_file",
            # 其他客户端在线状态变更
            "notice_client_status",
            # 精华消息添加
            "notice_essence_add",
            # 精华消息移出
            "notice_essence_delete",
            # 加好友请求
            "request_friend",
            # 加群请求
            "request_group_add",
            # 加群邀请
            "request_group_invite",
            # 连接响应
            "meta_event_lifecycle_connect",
            # 心跳
            "meta_event_heartbeat",
            # 生命周期
            "meta_event",
        ]


    def meta_event_lifecycle_connect(self, event: Meta_Event):
        """
        连接响应
        """
        pass
    
    def meta_event_heartbeat(self, event: Meta_Event):
        """
        心跳
        """
        pass

    def meta_event(self, event: Meta_Event):
        """
        生命周期
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

    def on_group_msg(self, message: Group_Message):
        pass
    
    def on_private_msg(self, message: Private_Message):
        pass

    def at_bot(self, message: Group_Message, cqCode_list, cqCode):
        """
        接收到 at bot
        """
        pass
    
    def at(self, message: Group_Message, cqCode_list, cqCode):
        """
        接收到 at
        """
        pass

    def message_private_friend(self, message: Private_Message):
        """
        好友私聊消息
        """
        pass
    
    def message_private_group(self, message: Private_Message):
        """
        群临时会话私聊消息
        """
        pass

    def message_sent_private_friend(self, message: Private_Message):
        """
        自身消息私聊上报
        """
        pass

    def message_group_anonymous(self, message: Group_Message):
        """
        群匿名消息
        """
        pass
    
    def message_sent_group_normal(self, message: Group_Message):
        """
        群中自身消息上报
        """
        pass
    
    def message_private_group_self(self, message: Group_Message):
        """
        群中自身消息
        """
        pass
    
    def message_private_other(self, message: Private_Message):
        """
        私聊消息
        """
        pass

    def message_group_normal(self, message: Group_Message):
        """
        群消息
        """
        pass

    def notice_group_upload(self, event: Notice_Event):
        """
        群文件上传
        """
        pass
    
    def notice_group_admin_set(self, event: Notice_Event):
        """
        群管理员设置
        """
        pass

    def notice_group_admin_unset(self, event: Notice_Event):
        """
        群管理员取消
        """
        pass
    
    def notice_group_decrease_leave(self, event: Notice_Event):
        """
        群成员减少 - 主动退群
        """
        pass
    
    def notice_group_decrease_kick(self, event: Notice_Event):
        """
        群成员减少 - 成员被踢
        """
        pass
    
    def notice_group_decrease_kick_me(self, event: Notice_Event):
        """
        群成员减少 - 登录号被踢
        """
        pass
    
    def notice_group_increase_approve(self, event: Notice_Event):
        """
        群成员增加 - 同意入群
        """
        pass

    def notice_group_increase_invite(self, event: Notice_Event):
        """
        群成员增加 - 邀请入群
        """
        pass
    
    def notice_group_ban_ban(self, event: Notice_Event):
        """
        群禁言
        """
        pass

    def notice_group_ban_lift_ban(self, event: Notice_Event):
        """
        群解除禁言
        """
        pass

    def notice_group_recall(self, event: Notice_Event):
        """
        群消息撤回
        """
        pass
    
    def notice_notify_lucky_king(self, event: Notice_Event):
        """
        群红包运气王提示
        """
        pass
    
    def notice_notify_honor(self, event: Notice_Event):
        """
        群成员荣誉变更提示
        honor_type 荣誉类型

        talkative:龙王 
        performer:群聊之火 
        emotion:快乐源泉
        """

        pass

    def notice_notify_title(self, event: Notice_Event):
        """
        群成员头衔变更
        """
        pass
    
    def notice_group_card(self, event: Notice_Event):
        """
        群成员名片更新
        """
        pass
    
    def notice_friend_add(self, event: Notice_Event):
        """
        好友添加
        """
        pass

    def notice_friend_recall(self, event: Notice_Event):
        """
        好友消息撤回
        """
        pass
    
    def notice_notify_poke(self, event: Notice_Event):
        """
        好友/群内 戳一戳
        """
        pass
    
    def notice_offline_file(self, event: Notice_Event):
        """
        接收到离线文件
        """
        pass

    def notice_client_status(self, event: Notice_Event):
        """
        其他客户端在线状态变更
        """
        pass
    
    def notice_essence_add(self, event: Notice_Event):
        """
        精华消息添加
        """
        pass
    
    def notice_essence_delete(self, event: Notice_Event):
        """
        精华消息移出
        """
        pass

    def request_friend(self, event: Request_Event):
        """
        加好友请求
        """
        pass

    def request_group_add(self, event: Request_Event):
        """
        加群请求
        """
        pass
    
    def request_group_invite(self, event: Request_Event):
        """
        加群邀请
        """
        pass


class Plugin(cqEvent):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config: dict[str, Any]) -> None:
        self.bot = bot
        self.cqapi = cqapi
        self.plugin_config = plugin_config