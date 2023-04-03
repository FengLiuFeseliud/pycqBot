from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Union, TYPE_CHECKING, Optional
from pycqBot.cqCode import reply, strToCqCode, get_cq_code
from pycqBot.data.user import Private_User, Group_User, User


if TYPE_CHECKING:
    from pycqBot import cqBot, cqHttpApi
    from pycqBot.data.event import Message_Event


class Message(metaclass=ABCMeta):

    def __init__(self, cqapi: cqHttpApi, event: Message_Event, message_data: dict[str, Any]) -> None:
        self._cqapi = cqapi
        self._message_data: dict[str, Any] = message_data

        self.event = event
        """消息事件"""

        self.id: int = message_data["message_id"]
        """消息 id"""

        self.sub_type: str = message_data["sub_type"]
        """
        消息子类型\n
        
        群消息
            正常消息 normal, 匿名消息 anonymous, 系统提 notice\n
        
        私聊消息
            好友 friend, 群临时会话 group, 群中自身发送 group_self
        """

        self.raw_message: str = message_data["raw_message"]
        """原始消息内容"""

        self.font: int = message_data["font"]
        """字体"""

        self.sender: User = None
        """发送人"""

        self.message: str = message_data["message"]
        """消息"""

        self.code_str: list[str] = strToCqCode(self.message)
        """消息 cqCode 字符串"""

        self.code: list[dict[str, Union[str, dict[str, Any]]]] = [get_cq_code(code_str) for code_str in self.code_str]
        """消息 cqCode 字典"""

    @abstractmethod
    def reply(self, message: str, auto_escape: bool=False) -> None:
        """
        回复该消息
        """

    @abstractmethod
    def reply_not_code(self, message: str, auto_escape: bool=False) -> None:
        """
        回复该消息 不带 cqcode
        """

    def delete(self):
        """
        撤回消息
        """
        self._cqapi.delete_msg(self.id)
    
    def record(self, time_end: int) -> None:
        """
        存储该消息
        """
        self._cqapi.record_message(self, time_end)


class Private_Message(Message):
    """私聊消息"""

    def __init__(self, cqapi: cqHttpApi, event: Message_Event, message_data: dict[str, Any]) -> None:
        super().__init__(cqapi, event, message_data)

        self.sender: Private_User = Private_User(self._cqapi, message_data["sender"])
        """发送人"""

        self.target_id: int = message_data["target_id"]
        """接收者 QQ 号"""

        self.temp_source: Optional[int] = message_data["temp_source"] if "temp_source" in message_data else None
        """临时会话来源"""

    def reply(self, message: str, auto_escape: bool = False) -> None:
        self._cqapi.send_private_msg(self.sender.id, "%s%s" % (reply(msg_id=self.id), message), self.temp_source, auto_escape)

    def reply_not_code(self, message: str, auto_escape: bool=False) -> None:
        self._cqapi.send_private_msg(self.sender.id, message, self.temp_source, auto_escape)

class Group_Message(Message):
    """群消息"""

    def __init__(self, cqapi: cqHttpApi, event: Message_Event, message_data: dict[str, Any]) -> None:
        super().__init__(cqapi, event, message_data)

        self.group_id: int = message_data["group_id"]
        """群号"""

        self.sender: Group_User = Group_User(self._cqapi, self.group_id, message_data["sender"])
        """发送人"""

        self.anonymous: dict[str, Any] = message_data["anonymous"]
        """
        匿名信息\n

            如果不是匿名消息则为 null
        """

    def reply(self, message: str, auto_escape: bool = False) -> None:
        self._cqapi.send_group_msg(self.group_id, "%s%s" % (reply(msg_id=self.id), message), auto_escape)

    def reply_not_code(self, message: str, auto_escape: bool=False) -> None:
        self._cqapi.send_group_msg(self.group_id, message, auto_escape)

    def set_essence(self):
        """
        设置精华消息
        """
        self._cqapi.set_essence_msg(self.id)

    def delete_essence(self):
        """
        移出精华消息
        """
        self._cqapi.delete_essence_msg(self.id)