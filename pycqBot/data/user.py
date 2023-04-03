from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, TYPE_CHECKING, Optional

from pycqBot.cqCode import poke


if TYPE_CHECKING:
    from pycqBot import cqHttpApi


class User(metaclass=ABCMeta):

    def __init__(self, cqapi: cqHttpApi, user_data:  dict[str, Any]) -> None:
        self._cqapi = cqapi

        self.id: int = user_data["user_id"]
        """QQ 号"""

        self.nickname: str = user_data["nickname"]
        """昵称"""

        self.sex: str = user_data["sex"]
        """
        性别\n

            male 男性, female 女性 或 unknown 未知
        """

        self.age: int = user_data["age"]
        """年龄"""

    def get_stranger_info(self, no_cache: bool = False):
        """
        获取陌生人信息
        """
        return self._cqapi.get_stranger_info(self.id, no_cache)

    def delete(self):
        """
        删除好友
        """
        self._cqapi.delete_friend(self.id)

    def delete_unidirectional(self):
        """
        删除单向好友
        """
        self._cqapi.delete_unidirectional_friend(self.id)

    def waiting_reply(self, sleep: int):
        """
        等待回复 等待超时返回 None 用于进行判断
        """
        return self._cqapi.reply(self.id, sleep)

    @abstractmethod
    def send_message(self, message: str, auto_escape: bool = False):
        """
        发送消息
        """

    @abstractmethod
    def send_forward_msg(self, messages: str):
        """
        发送合并转发
        """


class Private_User(User):
    """私聊用户"""
    
    def __init__(self, cqapi: cqHttpApi, user_data: dict[str, Any]) -> None:
        super().__init__(cqapi, user_data)

        self.group_id: Optional[int] = user_data["group_id"] if "group_id" in user_data else None
        """
        临时群消息来源群号\n

            当私聊类型为群临时会话时的额外字段
        """

    def send_message(self, message: str, auto_escape: bool = False):
        """
        发送私聊消息
        """

        if self.group_id is None:
            self._cqapi.send_private_msg(self.id, message, auto_escape)
            return
         
        self._cqapi.send_private_msg(self.id, message, self.group_id, auto_escape)

    def send_forward_msg(self, messages: str):
        """
        发送私聊合并转发
        """

        self._cqapi.send_private_forward_msg(self.id, messages)

class Group_User(User):
    """群聊用户"""
    
    def __init__(self, cqapi: cqHttpApi, group_id: int, user_data: dict[str, Any]) -> None:
        super().__init__(cqapi, user_data)

        self.group_id: int = group_id
        """来源群"""

        self.card: str = user_data["card"]
        """群名片／备注"""

        self.area: str = user_data["area"]
        """地区"""

        self.level: str = user_data["level"]
        """成员等级"""

        self.role: str = user_data["role"]
        """
        角色\n

            owner 群主, admin 管理员, member 群友
        """

        self.title: str = user_data["title"]
        """专属头衔"""

    def send_message(self, message: str, auto_escape: bool = False):
        """
        发送私聊消息
        """
        self._cqapi.send_private_msg(self.id, message, auto_escape)

    def send_forward_msg(self, messages: str):
        """
        发送私聊合并转发
        """

        self._cqapi.send_private_forward_msg(self.id, messages)

    def poke(self):
        """
        群戳一戳
        """
        self._cqapi.send_group_msg(self.group_id, poke(self.id))

    def ban(self, duration: int = 30):
        """
        群禁言
        """
        self._cqapi.set_group_ban(self.group_id, self.id, duration)

    def kick(self, reject_add_request: bool = False):
        """
        群踢人
        """
        self._cqapi.set_group_kick(self.group_id, self.id, reject_add_request)

    def admin(self, enable: bool):
        """
        设置群管理员
        """
        self._cqapi.set_group_admin(self.group_id, self.id, enable)

    def set_card(self, card: str):
        """
        设置群名片 ( 群备注 )
        """
        self._cqapi.set_group_card(self.group_id, self.id, card)

    def set_special_title(self, title: str, duration: int = -1):
        """
        设置群专属头衔
        """
        self._cqapi.set_group_special_title(self.group_id, self.id, title, duration)
