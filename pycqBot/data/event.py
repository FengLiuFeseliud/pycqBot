from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Union, TYPE_CHECKING
import json

from pycqBot.data.message import Group_Message, Private_Message

if TYPE_CHECKING:
    from pycqBot.cqApi import cqHttpApi


class Message:

    MESSAGE_POST_TYPE: str = "message"
    """消息事件类型"""

    PRIVATE_MESSAGE_TYPE: str = "private"
    """私聊消息类型"""

    GROUP_MESSAGE_TYPE: str = "group"
    """群消息类型"""


class Notice:

    NOTICE_POST_TYPE: str = "notice"
    """通知事件类型"""


class Request:

    REQUEST_POST_TYPE: str = "request"
    """请求事件类型"""


class Meta:

    META_POST_TYPE: str = "meta_event"
    """元事件类型"""


class Event(metaclass=ABCMeta):

    def __init__(self, event_data: dict[str, Any]) -> None:
        self.data = event_data
        """事件数据"""
        
        self.post_type: str = event_data["post_type"]
        """事件上报的类型"""

        self.sub_type: str = event_data["sub_type"] if "sub_type" in event_data else None
        """事件子类型"""
    
    @abstractmethod
    def get_event_sub_type(self) -> str:
        """
        获取事件副类型
        """

    def get_event_name(self) -> str:
        """
        获取完整事件名

        将 `post_type` `sub_type` 事件副类型 拼接为 cqEvent 事件函数名的格式
        """
        if self.sub_type is None:
            return "%s_%s" % (self.post_type, self.get_event_sub_type())
        else:
            return "%s_%s_%s" % (self.post_type, self.get_event_sub_type(), self.sub_type)


class Message_Event(Event):
    """消息事件"""

    def __init__(self, event_data: dict[str, Any]) -> None:
        super().__init__(event_data)

        self.message_type: str = event_data["message_type"] if "message_type" in event_data else None
        """消息类型"""

    def get_event_sub_type(self) -> str:
        return self.message_type
    
    def get_message(self, cqapi: cqHttpApi) -> Union[Group_Message, Private_Message]:
        return Private_Message(cqapi, self, self.data) if self.is_private() else Group_Message(cqapi, self, self.data)
    
    def is_private(self) -> bool:
        """是否为私聊消息类型"""
        return self.message_type == Message.PRIVATE_MESSAGE_TYPE
    
    def is_group(self) -> bool:
        """是否为群消息类型"""
        return self.message_type == Message.GROUP_MESSAGE_TYPE


class Notice_Event(Event):
    """通知事件"""

    def __init__(self, event_data: dict[str, Any]) -> None:
        super().__init__(event_data)

        self.notice_type: str = event_data["notice_type"] if "notice_type" in event_data else None
        """通知类型"""

    def get_event_sub_type(self) -> str:
        return self.notice_type
    

class Request_Event(Event):
    """请求事件"""

    def __init__(self, event_data: dict[str, Any]) -> None:
        super().__init__(event_data)

        self.request_type: str = event_data["request_type"] if "request_type" in event_data else None
        """请求类型"""

    def get_event_sub_type(self) -> str:
        return self.request_type
    

class Meta_Event(Event):
    """元事件"""

    def __init__(self, event_data: dict[str, Any]) -> None:
        super().__init__(event_data)

        self.meta_event_type: str = event_data["meta_event_type"] if "meta_event_type" in event_data else None
        """元类型"""

    def get_event_sub_type(self) -> str:
        return self.meta_event_type
    

def _get_event(message: str) -> Event:
    message_data = json.loads(message)
    if message_data["post_type"] == Message.MESSAGE_POST_TYPE:
        return Message_Event(message_data)
    
    if message_data["post_type"] == Meta.META_POST_TYPE:
        return Meta_Event(message_data)
    
    if message_data["post_type"] == Notice.NOTICE_POST_TYPE:
        return Notice_Event(message_data)
    
    if message_data["post_type"] == Request.REQUEST_POST_TYPE:
        return Request_Event(message_data)
    
    raise TypeError("未知事件协议: %s" % message_data)
