from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pycqBot.data.message import Group_Message, Private_Message, Message
    from pycqBot.data.event import Message_Event, Meta_Event, Notice_Event, Request_Event


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

class Event:
    """
    go-cqhttp v1.0.0 事件
    
    https://docs.go-cqhttp.org/event
    """

    def message_private_friend(self, message: Private_Message):
        """
        私聊好友消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        pass
    
    def message_private_group(self, message: Private_Message):
        """
        私聊群临时会话消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        pass

    def message_sent_private_friend(self, message: Private_Message):
        """
        私聊好友消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        pass

    def message_private_group_self(self, message: Private_Message):
        """
        私聊群中自身消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        pass


    def message_private_other(self, message: Private_Message):
        """
        私聊消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        pass

    def message_group_normal(self, message: Group_Message):
        """
        群消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        """
        pass

    def message_group_anonymous(self, message: Group_Message):
        """
        群匿名消息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        """
        pass
    
    def message_sent_group_normal(self, message: Group_Message):
        """
        群中自身消息上报

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        """
        pass

    def notice_friend_recall(self, event: Notice_Event):
        """
        私聊消息撤回

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF%E6%92%A4%E5%9B%9E
        """
        pass

    def notice_group_recall(self, event: Notice_Event):
        """
        群消息撤回

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF%E6%92%A4%E5%9B%9E
        """
        pass

    def notice_group_increase_approve(self, event: Notice_Event):
        """
        群成员增加 - 同意入群

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0
        """
        pass

    def notice_group_increase_invite(self, event: Notice_Event):
        """
        群成员增加 - 邀请入群

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0
        """
        pass
    
    def notice_group_decrease_leave(self, event: Notice_Event):
        """
        群成员减少 - 主动退群

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91
        """
        pass
    
    def notice_group_decrease_kick(self, event: Notice_Event):
        """
        群成员减少 - 成员被踢

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91
        """
        pass
    
    def notice_group_decrease_kick_me(self, event: Notice_Event):
        """
        群成员减少 - 登录号被踢

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91
        """
        pass

    def notice_group_admin_set(self, event: Notice_Event):
        """
        群管理员变动 - 设置

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%AE%A1%E7%90%86%E5%91%98%E5%8F%98%E5%8A%A8
        """
        pass

    def notice_group_admin_unset(self, event: Notice_Event):
        """
        群管理员变动 - 取消

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%AE%A1%E7%90%86%E5%91%98%E5%8F%98%E5%8A%A8
        """
        pass

    def notice_group_upload(self, event: Notice_Event):
        """
        群文件上传

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0
        """
        pass
    
    def notice_group_ban_ban(self, event: Notice_Event):
        """
        群禁言 - 禁言

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%A6%81%E8%A8%80
        """
        pass

    def notice_group_ban_lift_ban(self, event: Notice_Event):
        """
        群禁言 - 解除

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%A6%81%E8%A8%80
        """
        pass

    def notice_friend_add(self, event: Notice_Event):
        """
        好友添加

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%A5%BD%E5%8F%8B%E6%B7%BB%E5%8A%A0
        """
        pass
    
    def notice_notify_poke(self, event: Notice_Event):
        """
        好友/群内 戳一戳

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%A5%BD%E5%8F%8B%E6%88%B3%E4%B8%80%E6%88%B3-%E5%8F%8C%E5%87%BB%E5%A4%B4%E5%83%8F
        """
        pass
    
    def notice_notify_lucky_king(self, event: Notice_Event):
        """
        群红包运气王提示

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%BA%A2%E5%8C%85%E8%BF%90%E6%B0%94%E7%8E%8B%E6%8F%90%E7%A4%BA
        """
        pass
    
    def notice_notify_honor(self, event: Notice_Event):
        """
        群成员荣誉变更提示
        
        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA
        """
        pass

    def notice_notify_title(self, event: Notice_Event):
        """
        群成员头衔变更

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A4%B4%E8%A1%94%E5%8F%98%E6%9B%B4
        """
        pass
    
    def notice_group_card(self, event: Notice_Event):
        """
        群成员名片更新

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%90%8D%E7%89%87%E6%9B%B4%E6%96%B0
        """
        pass
    
    def notice_offline_file(self, event: Notice_Event):
        """
        接收到离线文件

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E6%8E%A5%E6%94%B6%E5%88%B0%E7%A6%BB%E7%BA%BF%E6%96%87%E4%BB%B6
        """
        pass

    def notice_client_status(self, event: Notice_Event):
        """
        其他客户端在线状态变更

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%85%B6%E4%BB%96%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%9C%A8%E7%BA%BF%E7%8A%B6%E6%80%81%E5%8F%98%E6%9B%B4
        """
        pass
    
    def notice_essence_add(self, event: Notice_Event):
        """
        精华消息变更 - 添加

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%8F%98%E6%9B%B4
        """
        pass
    
    def notice_essence_delete(self, event: Notice_Event):
        """
        精华消息变更 - 移出

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%8F%98%E6%9B%B4
        """
        pass

    def request_friend(self, event: Request_Event):
        """
        加好友请求

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82
        """
        pass

    def request_group_add(self, event: Request_Event):
        """
        加群请求

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        """
        pass
    
    def request_group_invite(self, event: Request_Event):
        """
        加群邀请

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        """
        pass

    def meta_event_lifecycle_connect(self, event: Meta_Event):
        """
        连接响应

        go-cqhttp 文档:
        null
        """
        pass
    
    def meta_event_heartbeat(self, event: Meta_Event):
        """
        心跳

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E5%BF%83%E8%B7%B3%E5%8C%85
        """
        pass

    def meta_event(self, event: Meta_Event):
        """
        生命周期

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/event/#%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F
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