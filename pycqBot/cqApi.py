from typing import Optional, Union
from pycqBot.asyncHttp import asyncHttp
from pycqBot.data.message import *


class Api(asyncHttp):
    """
    go-cqhttp v1.0.0 Api

    https://docs.go-cqhttp.org/api/
    """

    def get_login_info(
        self
    ):
        """
        获取登录号信息

        Returns:
            `user_id`: int QQ 号
            `nickname`: str QQ 昵称

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%99%BB%E5%BD%95%E5%8F%B7%E4%BF%A1%E6%81%AF
        """
        return self._link("/set_friend_add_request")

    def set_qq_profile(
        self,
        nickname: str,
        company: str,
        email: str,
        college: str,
        personal_note: str
    ) -> None:
        """
        设置登录号资料

        Args:
            `nickname`: 名称
            `company`: 公司
            `email`: 邮箱
            `college`: 学校
            `personal_note`: 个人说明

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%99%BB%E5%BD%95%E5%8F%B7%E8%B5%84%E6%96%99
        """
        self.add("/set_qq_profile", {
            "nickname": nickname,
            "company": company,
            "email": email,
            "college": college,
            "personal_note": personal_note
        })

    def qidian_get_account_info(
        self
    ):
        """
        获取企点账号信息

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E4%BC%81%E7%82%B9%E8%B4%A6%E5%8F%B7%E4%BF%A1%E6%81%AF
        """
        return self._link("/qidian_get_account_info")

    def _get_model_show(
        self,
        model: str
    ) -> None:
        """
        获取在线机型

        Args:
            `model`: 机型名称

        Returns:
            `variants`: -
                `model_show`: str -
                `need_pay`: bool -

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%9C%A8%E7%BA%BF%E6%9C%BA%E5%9E%8B
        """
        return self._link("/_get_model_show", {
            "model": model
        })

    def _set_model_show(
        self,
        model: str,
        model_show: str
    ) -> None:
        """
        设置在线机型

        Args:
            `model`: 机型名称
            `model_show`: -

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E5%9C%A8%E7%BA%BF%E6%9C%BA%E5%9E%8B
        """
        self.add("_set_model_show", {
            "model": model,
            "model_show": model_show
        })

    def get_online_clients(
        self,
        no_cache: bool = False
    ):
        """
        获取当前账号在线客户端列表

        Args:
            `no_cache`: 是否无视缓存

        Returns:
            `clients`: Device[] 在线客户端列表

            `Device[]`:
                `app_id`: int 客户端ID
                `device_name`: str 设备名称
                `device_kind`: str 设备类型

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E8%B4%A6%E5%8F%B7%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%88%97%E8%A1%A8
        """
        return self._link("/get_online_clients", {
            "no_cache": no_cache
        })

    def get_stranger_info(
        self,
        user_id: int,
        no_cache: bool = False
    ):
        """
        获取陌生人信息

        Args:
            `user_id`: 对方 QQ 号
            `no_cache`: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E9%99%8C%E7%94%9F%E4%BA%BA%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_stranger_info", {
            "user_id": user_id,
            "no_cache": no_cache
        })

    def get_friend_list(
        self
    ):
        """
        获取好友列表

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8
        """
        return self._link("/get_friend_list")

    def get_unidirectional_friend_list(
        self
    ):
        """
        获取单向好友列表

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%8D%95%E5%90%91%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8
        """
        return self._link("/get_unidirectional_friend_list")

    def delete_friend(
        self,
        user_id: int
    ) -> None:
        """
        删除好友

        Args:
            `user_id`: 好友 QQ 号

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E5%A5%BD%E5%8F%8B
        """
        self.add("/delete_msg", {
            "user_id": user_id
        })

    def delete_unidirectional_friend(
        self,
        user_id: int
    ) -> None:
        """
        删除单向好友

        Args:
            `user_id`: 单向好友QQ号

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E5%8D%95%E5%90%91%E5%A5%BD%E5%8F%8B
        """
        self.add("/delete_unidirectional_friend", {
            "user_id": user_id
        })

    def send_private_msg(
        self,
        user_id: int,
        message: str,
        group_id: Optional[int] = None,
        auto_escape: bool = False
    ) -> None:
        """
        发送私聊消息

        Args:
            `user_id`: 对方 QQ 号
            `group_id`: 主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)
            `message`: 要发送的内容
            `auto_escape`: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 )

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        """
        post_data = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape
        }

        if group_id is not None:
            post_data["group_id"] = group_id

        self.add("/send_msg", post_data)

    def send_group_msg(
        self,
        group_id: int,
        message: str,
        auto_escape: bool = False
    ) -> None:
        """
        发送群消息

        Args:
            `group_id`: 群号
            `message`: 要发送的内容
            `auto_escape`: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 )

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E8%81%8A%E6%B6%88%E6%81%AF
        """
        self.add("/send_msg", {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })

    def get_msg(
        self,
        message_id: int
    ):
        """
        获取消息

        Args:
            `message_id`: 消息id

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E6%B6%88%E6%81%AF
        """
        return self._link("/get_msg", {
            "message_id": message_id,
        })

    def delete_msg(
        self,
        message_id: int
    ) -> None:
        """
        撤回消息

        Args:
            `message_id`: 消息id

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%92%A4%E5%9B%9E%E6%B6%88%E6%81%AF
        """
        self.add("/delete_msg", {
            "message_id": message_id
        })

    def mark_msg_as_read(
        self,
        message_id: int
    ) -> None:
        """
        标记消息已读

        Args:
            `message_id`: 消息id

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%A0%87%E8%AE%B0%E6%B6%88%E6%81%AF%E5%B7%B2%E8%AF%BB
        """
        self.add("/mark_msg_as_read", {
            "message_id": message_id
        })

    def get_forward_msg(
        self,
        message_id: int
    ) -> None:
        """
        获取合并转发内容

        Args:
            `message_id`: 消息id

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E5%86%85%E5%AE%B9
        """
        return self._link("/get_forward_msg", {
            "message_id": message_id
        })

    def send_group_forward_msg(
        self,
        group_id: int,
        message: str
    ) -> None:
        """
        发送合并转发 ( 群 )

        Args:
            `group_id`: 群号
            `messages`: 自定义转发消息, 具体看 CQcode

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91-%E7%BE%A4%E8%81%8A
        """
        self.add("/send_group_forward_msg", {
            "group_id": group_id,
            "messages": message,
        })

    def send_private_forward_msg(
        self,
        user_id: int,
        message: str
    ) -> None:
        """
        发送合并转发 ( 私聊 )

        Args:
            `user_id`: 群号
            `messages`: 自定义转发消息, 具体看 CQcode

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91-%E5%A5%BD%E5%8F%8B
        """
        self.add("/send_private_forward_msg", {
            "user_id": user_id,
            "messages": message,
        })

    def get_group_msg_history(
        self,
        message_seq: int,
        group_id: int
    ):
        """
        获取群消息历史记录

        Args:
            `message_seq`: 起始消息序号, 可通过 `get_msg` 获得
            `group_id`: 群号

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%B6%88%E6%81%AF%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95
        """
        return self._link("/get_group_msg_history", data={
            "message_seq": message_seq,
            "group_id": group_id
        })

    def send_reply(
        self,
        from_message: Union[Private_Message, Group_Message, Message],
        message: str,
        auto_escape: bool = False
    ) -> None:
        """
        发送回复

        Args:
            `from_message`: 发送至该消息所在外
            `messages`: 要发送的内容
            `auto_escape`: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 )
        """
        if type(from_message) is Group_Message:
            self.send_group_msg(from_message.group_id, message, auto_escape)

        if type(from_message) is Private_Message:
            self.send_private_msg(from_message.sender.id, message, auto_escape)

    def send_forward_msg(
        self,
        from_message: Union[Private_Message, Group_Message],
        message: str
    ) -> None:
        """
        发送合并转发

        Args:
            `from_message`: 发送至该消息所在外
            `messages`: 自定义转发消息, 具体看 CQcode
        """
        if type(from_message) is Group_Message:
            self.send_group_forward_msg(from_message.group_id, message)

        if type(from_message) is Private_Message:
            self.send_private_forward_msg(from_message.sender.id, message)

    def get_image(
        self,
        file: str
    ):
        """
        获取图片信息

        Args:
            `file`: 图片缓存文件名

        Returns:
            `size`: int 图片源文件大小
            `filename`: str 图片文件原名
            `url`: str 图片下载地址

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%9B%BE%E7%89%87%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_image", {
            "file": file
        })

    def can_send_image(
        self
    ):
        """
        检查是否可以发送图片

        Returns:
            `yes`: bool 是或否

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87
        """
        return self._link("/can_send_image")

    def ocr_image(
        self,
        image: str
    ):
        """
        图片 OCR

        Args:
            `image`: 图片ID

        Returns:
            `texts`: TextDetection OCR结果
                `text`: str 文本
                `confidence`: int 置信度
                `coordinates`: 坐标

            `language`: str 语言

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%9B%BE%E7%89%87-ocr
        """
        return self._link("/ocr_image", {
            "image": image
        })

    def get_record(
        self,
        file: str,
        out_format: str
    ):
        """
        获取语音 (该 API 暂未被 go-cqhttp 支持)

        Args:
            `file`: 收到的语音文件名（消息段的 file 参数）, 如 0B38145AA44505000B38145AA4450500.silk
            `out_format`: 要转换到的格式, 目前支持 mp3、amr、wma、m4a、spx、ogg、wav、flac

        Returns:
            `file`: str 转换后的语音文件路径, 如 /home/somebody/cqhttp/data/record/0B38145AA44505000B38145AA4450500.mp3

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E8%AF%AD%E9%9F%B3
        """
        return self._link("/get_record", {
            "file": file,
            "out_format": out_format
        })

    def can_send_record(
        self
    ):
        """
        检查是否可以发送语音

        Returns:
            `yes`: bool 是或否

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E8%AF%AD%E9%9F%B3
        """
        return self._link("/can_send_record")

    def set_friend_add_request(
        self,
        flag: str,
        approve: bool = True,
        remark: str = ""
    ) -> None:
        """
        处理加好友请求

        Args:
            `flag`: 加好友请求的 flag（需从上报的数据中获得）
            `approve`: 是否同意请求
            `remark`: 添加后的好友备注（仅在同意时有效）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82
        """
        self.add("/set_friend_add_request", {
            "flag": flag,
            "approve": approve,
            "remark": remark,
        })

    def set_group_add_request(
        self,
        flag: str,
        sub_type: str,
        approve: bool = True,
        reason: str = ""
    ) -> None:
        """
        处理加群请求／邀请

        Args:
            `flag`: 加好友请求的 flag（需从上报的数据中获得）
            `sub_type`: add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）
            `approve`: 是否同意请求
            `remark`: 添加后的好友备注（仅在同意时有效）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        """
        self.add("/set_group_add_request", {
            "flag": flag,
            "approve": approve,
            "sub_type": sub_type,
            "reason": reason
        })

    def get_group_info(
        self, group_id: int,
        no_cache: bool = False
    ):
        """
        获取群信息

        Args:
            `group_id`: 群号
            `no_cache`: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

        如果机器人尚未加入群, group_create_time, group_level, max_member_count 和 member_count 将会为0

        Returns:
            `group_id`: int 群号
            `group_name`: str 群名称
            `group_memo`: str 群备注
            `group_create_time`: int 群创建时间
            `group_level`: int 群等级
            `member_count`: int 成员数
            `max_member_count`: int 最大成员数（群容量）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        })

    def get_group_list(
        self,
        no_cache: bool = False
    ):
        """
        获取群列表

        Args:
            `no_cache`: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

        Returns:
            响应内容为 json 数组, 每个元素和上面的 `get_group_info` 接口相同

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%88%97%E8%A1%A8
        """
        return self._link("/get_group_list", {
            "no_cache": no_cache,
        })

    def get_group_member_info(
        self,
        group_id: int,
        user_id: int,
        no_cache: bool = False
    ):
        """
        获取群成员信息

        Args:
            `group_id`: 群号
            `user_id`: QQ 号
            `no_cache`: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

        Returns:
            `group_id`: int 群号
            `user_id`: int QQ 号
            `nickname`: str 昵称
            `card`: str 群名片／备注
            `sex`: str 性别, male 或 female 或 unknown
            `age`: int 年龄
            `area`: str 地区
            `join_time`: int 加群时间戳
            `last_sent_time`: int 最后发言时间戳
            `level`: str 成员等级
            `role`: str 角色, owner 或 admin 或 member
            `unfriendly`: bool 是否不良记录成员
            `title`: str 专属头衔
            `title_expire_time`: int 专属头衔过期时间戳
            `card_changeable`: bool 是否允许修改群名片
            `shut_up_timestamp`: int 禁言到期时间

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_group_member_info", {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache,
        })

    def get_group_member_list(
        self,
        group_id: int,
        no_cache: bool = False
    ):
        """
        获取群成员列表

        Args:
            `group_id`: 群号
            `no_cache`: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

        Returns:
            响应内容为 json 数组, 每个元素的内容和上面的 `get_group_member_info` 接口相同
            但对于同一个群组的同一个成员, 获取列表时和获取单独的成员信息时
            某些字段可能有所不同, 例如 `area、title` 等字段在获取列表时无法获得, 具体应以单独的成员信息为准。

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E5%88%97%E8%A1%A8
        """
        return self._link("/get_group_member_list", {
            "group_id": group_id,
            "no_cache": no_cache,
        })

    def get_group_honor_info(
        self,
        group_id: int,
        type: str
    ):
        """
        获取群荣誉信息

        Args:
            `group_id`: 群号
            `type`: 要获取的群荣誉类型, 可传入 `talkative` `performer` `legend` `strong_newbie` `emotion`
            以分别获取单个类型的群荣誉数据, 或传入 `all` 获取所有数据

        Returns:
            `group_id`: int 群号

            `current_talkative`: 当前龙王, 仅 `type` 为 `talkative` 或 `all` 时有数据
                `user_id`: int QQ 号
                `nickname`: str 昵称
                `avatar`: str 头像 URL
                `day_count`: int 持续天数

            `talkative_list`: 历史龙王, 仅 type 为 talkative 或 all 时有数据
            `performer_list`: 群聊之火, 仅 type 为 performer 或 all 时有数据
            `legend_list`: 群聊炽焰, 仅 type 为 legend 或 all 时有数据
            `strong_newbie_list`: 冒尖小春笋, 仅 type 为 strong_newbie 或 all 时有数据
            `emotion_list`: 快乐之源, 仅 type 为 emotion 或 all 时有数据

                `*_list`: 其它各 *_list 的每个元素是一个 json 对象
                    `user_id`: int QQ 号
                    `nickname`: str 昵称
                    `avatar`: str 头像 URL
                    `description`: str 荣誉描述

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E8%8D%A3%E8%AA%89%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_group_honor_info", {
            "group_id": group_id,
            "type": type,
        })

    def get_group_system_msg(
        self
    ):
        """
        获取群系统消息

        Returns:
            `invited_requests`: 邀请消息列表
                `request_id`: int 请求ID
                `invitor_uin`: int 邀请者
                `invitor_nick`: str 邀请者昵称
                `group_id`: int 群号
                `group_name`: str 群名
                `checked`: bool 是否已被处理
                `actor`: int 处理者, 未处理为0

            `join_requests`: 进群消息列表
                `request_id`: int 请求 ID
                `requester_uin`: int 请求者 ID
                `requester_nick`: str 请求者昵称
                `message`: str 验证消息
                `group_id`: int 群号
                `group_name`: str 群名
                `checked`: bool 是否已被处理
                `actor`: int 处理者, 未处理为0

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E7%B3%BB%E7%BB%9F%E6%B6%88%E6%81%AF
        """
        return self._link("/get_group_system_msg")

    def get_essence_msg_list(
        self,
        group_id: int
    ):
        """
        获取精华消息列表

        Args:
            `group_id`: int 群号

        Returns:
            `sender_id`: int 发送者 QQ 号
            `sender_nick`: str 发送者昵称
            `sender_time`: int 消息发送时间
            `operator_id`: int 操作者 QQ 号
            `operator_nick`: str 操作者昵称
            `operator_time`: int 精华设置时间
            `message_id`: int 消息ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%88%97%E8%A1%A8
        """
        return self._link("/get_essence_msg_list", {
            "group_id": group_id,
        })

    def get_group_at_all_remain(
        self,
        group_id: int
    ):
        """
        获取群 @全体成员 剩余次数

        Args:
            `group_id`: int 群号

        Returns:
            `can_at_all`: bool 是否可以 @全体成员
            `remain_at_all_count_for_group`: int 群内所有管理当天剩余 @全体成员 次数
            `remain_at_all_count_for_uin`: int Bot 当天剩余 @全体成员 次数

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4-%E5%85%A8%E4%BD%93%E6%88%90%E5%91%98-%E5%89%A9%E4%BD%99%E6%AC%A1%E6%95%B0
        """
        return self._link("/get_group_at_all_remain", {
            "group_id": group_id,
        })

    def set_group_name(
        self,
        group_id: int,
        group_name: str
    ) -> None:
        """
        设置群名

        Args:
            `group_id`: 群号
            `group_name`: 新群名

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D
        """
        self.add("/set_group_name", {
            "group_id": group_id,
            "group_name": group_name,
        })

    def set_group_portrait(
        self,
        group_id: int,
        file: str,
        cache: int = 1
    ):
        r"""
        设置群头像, 目前这个 API 在登录一段时间后因 cookie 失效而失效, 请考虑后使用

        图片支持以下几种格式:
            绝对路径, 例如 file:///C:\Users\Richard\Pictures1.png, 格式使用 file URI
            网络 URL, 例如 http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg
            Base64 编码, 例如 base64://iVBORw0KGgoAAAANSUhEUgAAABQAAAAVCAIAAADJ...

        Args:
            `group_id`: 群号
            `file`: 图片文件名
            `cache`: 表示是否使用已缓存的文件, 通过网络 URL 发送时有效, `1` 表示使用缓存, `0` 关闭关闭缓存, 默认为 `1`

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%A4%B4%E5%83%8F
        """
        self.add("/set_group_portrait", {
            "group_id": group_id,
            "file": file,
            "cache": cache
        })

    def set_group_admin(
        self,
        group_id: int,
        user_id: int,
        enable: bool = True
    ) -> None:
        """
        设置群组管理员

        Args:
            `group_id`: 群号
            `user_id`: 要设置管理员的 QQ 号
            `enable`: true 为设置, false 为取消

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E7%AE%A1%E7%90%86%E5%91%98
        """
        self.add("/set_group_admin", {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        })

    def set_group_card(
        self,
        group_id: int,
        user_id: int,
        card: str = ""
    ) -> None:
        """
        设置群名片 ( 群备注 )

        Args:
            `group_id`: 群号
            `user_id`: 要设置管理员的 QQ 号
            `card`: 群名片内容, 不填或空字符串表示删除群名片

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D%E7%89%87-%E7%BE%A4%E5%A4%87%E6%B3%A8
        """
        self.add("/set_group_card", {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        })

    def set_group_special_title(
        self,
        group_id: int,
        user_id: int,
        special_title: str = "",
        duration: int = -1
    ) -> None:
        """
        设置群组专属头衔

        Args:
            `group_id`: 群号
            `user_id`: 要设置管理员的 QQ 号
            `special_title`: 专属头衔, 不填或空字符串表示删除专属头衔
            `duration`: 专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果, 可能是只有某些特殊的时间长度有效, 有待测试

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E7%BB%84%E4%B8%93%E5%B1%9E%E5%A4%B4%E8%A1%94
        """
        self.add("/set_group_special_title", {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        })

    def set_group_ban(
        self,
        group_id: int,
        user_id: int,
        duration: int = 30*60
    ) -> None:
        """
        群组单人禁言

        Args:
            `group_id`: 群号
            `user_id`: 要设置管理员的 QQ 号
            `duration`: 禁言时长, 单位秒, 0 表示取消禁言

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E5%8D%95%E4%BA%BA%E7%A6%81%E8%A8%80
        """
        self.add("/set_group_ban", {
            "group_id": group_id,
            "user_id": user_id,
            "duration": int(duration) * 60
        })

    def set_group_whole_ban(
        self,
        group_id: int,
        enable: bool = True
    ) -> None:
        """
        群组全员禁言

        Args:
            `group_id`: 群号
            `enable`: 是否禁言

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E5%85%A8%E5%91%98%E7%A6%81%E8%A8%80
        """
        self.add("/set_group_whole_ban", {
            "group_id": group_id,
            "enable": enable
        })

    def set_group_anonymous_ban(self,
        group_id: int,
        duration: int = 1800,
        anonymous: Optional[object] = None,
        anonymous_flag: Optional[str] = None,
    ) -> None:
        """
        群匿名用户禁言

        Args:
            `group_id`: 群号
            `duration`: 禁言时长, 单位秒, 无法取消匿名用户禁言
            `anonymous`: 可选, 要禁言的匿名用户对象（群消息上报的 anonymous 字段）
            `anonymous_flag`: 可选, 要禁言的匿名用户的 flag（需从群消息上报的数据中获得）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E5%8C%BF%E5%90%8D%E7%94%A8%E6%88%B7%E7%A6%81%E8%A8%80
        """

        self.add("/set_group_anonymous_ban", {
            "group_id": group_id,
            "anonymous": anonymous,
            "anonymous_flag": anonymous_flag,
            "duration": duration
        })

    def set_essence_msg(
        self,
        message_id: int
    ) -> None:
        """
        设置精华消息

        Args:
            `message_id`: 消息 ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF
        """
        self.add("/set_essence_msg", {
            "message_id": message_id
        })

    def delete_essence_msg(
        self,
        message_id: int
    ) -> None:
        """
        移出精华消息

        Args:
            `message_id`: 消息 ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%A7%BB%E5%87%BA%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF
        """
        self.add("/delete_essence_msg", {
            "message_id": message_id
        })

    def send_group_sign(
        self,
        group_id: int
    ) -> None:
        """
        群打卡

        Args:
            `group_id`: 群号 ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E6%89%93%E5%8D%A1
        """
        self.add("/send_group_sign", {
            "group_id": group_id
        })

    def set_group_anonymous(
        self,
        group_id: int,
        enable: bool = True
    ) -> None:
        """
        群设置匿名 (该 API 暂未被 go-cqhttp 支持)

        Args:
            `group_id`: 群号 ID
            `enable`: 是否允许匿名聊天

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E8%AE%BE%E7%BD%AE%E5%8C%BF%E5%90%8D
        """
        self.add("/set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        })

    def _send_group_notice(
        self,
        group_id: int,
        content: str,
        image: Optional[str] = None
    ) -> None:
        """
        发送群公告

        Args:
            `group_id`: 群号 ID
            `content`: 公告内容
            `image`: 图片路径（可选）

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E5%85%AC%E5%91%8A
        """
        post_data = {
            "group_id": group_id,
            "enable": content
        }

        if image != None:
            post_data["image"] = image

        self.add("/set_group_anonymous", post_data)

    def _get_group_notice(
        self,
        group_id: int
    ):
        """
        获取群公告

        Args:
            `group_id`: 群号 ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%85%AC%E5%91%8A
        """
        return self._link("/_get_group_notice", {
            "group_id": group_id
        })

    def set_group_kick(
        self,
        group_id: int,
        user_id: int,
        reject_add_request: bool = False
    ) -> None:
        """
        群组踢人

        Args:
            `group_id`: 群号 ID
            `user_id`: 要踢的 QQ 号
            `reject_add_request`: 拒绝此人的加群请求

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E8%B8%A2%E4%BA%BA
        """
        self.add("/set_group_kick", {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        })

    def set_group_leave(
        self,
        group_id: int,
        is_dismiss: bool = False
    ) -> None:
        """
        退出群组

        Args:
            `group_id`: 群号 ID
            `is_dismiss`: 是否解散, 如果登录号是群主, 则仅在此项为 `true` 时能够解散

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E9%80%80%E5%87%BA%E7%BE%A4%E7%BB%84
        """
        self.add("/set_group_leave", {
            "group_id": group_id,
            "is_dismiss": is_dismiss,
        })

    def upload_group_file(
        self,
        group_id: str,
        file: str,
        name: str,
        folder: str
    ) -> None:
        """
        上传群文件

        在不提供 `folder` 参数的情况下默认上传到根目录

        只能上传本地文件, 需要上传 `http` 文件的话请先调用 `download_file` API 下载

        Args:
            `group_id`: 群号
            `file`: 本地文件路径
            `name`: 储存名称
            `folder`: 	父目录ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E4%B8%8A%E4%BC%A0%E7%BE%A4%E6%96%87%E4%BB%B6
        """
        self.add("/upload_group_file", {
            "group_id": group_id,
            "file": file,
            "name": name,
            "folder": folder
        })

    def delete_group_file(
        self,
        group_id: int,
        file_id: str,
        busid: int
    ) -> None:
        """
        删除群文件

        Args:
            `group_id`: 群号
            `file_id`: 文件 ID
            `busid`: 文件类型 

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E7%BE%A4%E6%96%87%E4%BB%B6
        """
        self.add("/delete_group_file", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        })

    def create_group_file_folder(
        self,
        group_id: int,
        name: str
    ) -> None:
        """
        创建群文件文件夹

        仅能在根目录创建文件夹

        Args:
            `group_id`: 群号
            `name`: 文件夹名称

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%88%9B%E5%BB%BA%E7%BE%A4%E6%96%87%E4%BB%B6%E6%96%87%E4%BB%B6%E5%A4%B9
        """
        self.add("/create_group_file_folder", {
            "group_id": group_id,
            "name": name,
            "parent_id": "/"
        })

    def delete_group_folder(
        self,
        group_id: int,
        folder_id: str
    ) -> None:
        """
        删除群文件文件夹

        Args:
            `group_id`: 群号
            `folder_id`: 文件夹ID

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E7%BE%A4%E6%96%87%E4%BB%B6%E6%96%87%E4%BB%B6%E5%A4%B9
        """
        self.add("/delete_group_folder", {
            "group_id": group_id,
            "folder_id": folder_id
        })

    def get_group_file_system_info(
        self,
        group_id: int
    ):
        """
        获取群文件系统信息

        Args:
            `group_id`: 群号

        Returns:
            `file_count`: int 文件总数
            `limit_count`: int 文件上限
            `used_space`: int 已使用空间
            `total_space`: int 空间上限

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_group_file_system_info", {
            "group_id": group_id
        })
    
    def get_group_root_files(
        self,
        group_id: int
    ):
        """
        获取群根目录文件列表

        Args:
            `group_id`: 群号

        Returns:
            `files`: 文件列表
            `folders`: 文件夹列表
        
        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%A0%B9%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8
        """
        return self._link("/get_group_root_files", {
            "group_id": group_id
        })

    def get_group_files_by_folder(
        self,
        group_id: int,
        folder_id: str
    ):
        """
        获取群子目录文件列表

        Args:
            `group_id`: 群号
            `folder_id`: 文件夹 ID

        Returns:
            `files`: 文件列表
            `folders`: 文件夹列表
        
        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%AD%90%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8
        """
        return self._link("/get_group_files_by_folder", {
            "group_id": group_id,
            "folder_id": folder_id
        })
    
    def get_group_file_url(
        self,
        group_id: int,
        file_id: str,
        busid: int
    ):
        """
        获取群文件资源链接

        Args:
            `group_id`: 群号
            `file_id`: 文件 ID
            `busid`: 文件类型

        Returns:
            `url`: str 文件下载链接
        
        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E8%B5%84%E6%BA%90%E9%93%BE%E6%8E%A5
        """
        return self._link("/get_group_file_url", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        })
    
    def upload_private_file(
        self,
        user_id: int,
        file: str,
        name: str
    ) -> None:
        """
        上传私聊文件

        Args:
            `user_id`: 对方 QQ 号
            `file`: 本地文件路径
            `name`: 文件名称

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E4%B8%8A%E4%BC%A0%E7%A7%81%E8%81%8A%E6%96%87%E4%BB%B6
        """
        self.add("upload_private_file", {
            "user_id": user_id,
            "file": file,
            "name": name
        })

    def get_cookies(
        self,
        domain: str
    ):
        """
        获取 Cookies (该 API 暂未被 go-cqhttp 支持)

        Args: 
            `domain`: 需要获取 cookies 的域名

        Returns:
            `cookies`: str Cookies

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96-cookies
        """
        return self._link("/get_cookies", {
            "domain": domain
        })

    def get_csrf_token(
        self
    ):
        """
        获取 CSRF Token (该 API 暂未被 go-cqhttp 支持)

        Returns:
            `token`: int CSRF Token

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96-csrf-token
        """
        return self._link("/get_csrf_token")

    def get_credentials(
        self,
        domain: str
    ):
        """
        获取 QQ 相关接口凭证, 即上面两个接口的合并 (该 API 暂未被 go-cqhttp 支持)

        Args: 
            `domain`: 需要获取 cookies 的域名

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96-qq-%E7%9B%B8%E5%85%B3%E6%8E%A5%E5%8F%A3%E5%87%AD%E8%AF%81
        """
        return self._link("/get_credentials", {
            "domain": domain
        })

    def get_version_info(
        self
    ):
        """
        获取 go-cqhttp 版本信息

        Returns:
            `app_name`: str 应用标识, 如 `go-cqhttp` 固定值
            `app_version`: str 应用版本, 如` v0.9.40-fix4`
            `app_full_name`: str 应用完整名称
            `protocol_version`: str OneBot 标准版本 固定值
            `coolq_edition`: str 原Coolq版本 固定值
            `coolq_directory`: str 
            `go-cqhttp`: bool 是否为go-cqhttp 固定值
            `plugin_version`: str 固定值
            `plugin_build_number`: int 固定值
            `plugin_build_configuration`: str 固定值
            `runtime_version`: str 
            `runtime_os`: str 
            `version`: 应用版本, 如 `v0.9.40-fix4`
            `protocol`: int 当前登陆使用协议类型

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%89%88%E6%9C%AC%E4%BF%A1%E6%81%AF
        """
        return self._link("/get_version_info")

    def get_status(
        self
    ):
        """
        获取 go-cqhttp 状态

        Returns:
            `app_initialized`: bool 原 CQHTTP 字段, 恒定为 true
            `app_enabled`: bool 原 CQHTTP 字段, 恒定为 true
            `plugins_good`: bool 原 CQHTTP 字段, 恒定为 true
            `app_good`: bool 原 CQHTTP 字段, 恒定为 true
            `online`: bool 表示BOT是否在线
            `good`: bool 同 online
            `stat`: 运行统计
                `PacketReceived`: int 收到的数据包总数
                `PacketSent`: int 发送的数据包总数
                `PacketLost`: int 数据包丢失总数
                `MessageReceived`: int 接受信息总数
                `MessageSent`: int 发送信息总数
                `DisconnectTimes`: int TCP 链接断开次数
                `LostTimes`: int 账号掉线次数
                `LastMessageTime`: int 最后一条消息时间

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%8A%B6%E6%80%81
        """
        return self._link("/get_status")

    def set_restart(
        self,
        delay: int = 0
    ) -> None:
        """
        重启 Go-CqHttp (自 go-cqhttp v1.0.0 版本已被移除，目前暂时没有再加入的计划)

        Args:
            `delay`: 要延迟的毫秒数, 如果默认情况下无法重启, 可以尝试设置延迟为 2000 左右

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E9%87%8D%E5%90%AF-go-cqhttp
        """

        self.add("/set_restart", {
            "delay": delay
        })

    def clean_cache(
        self
    ) -> None:
        """
        清理缓存 (该 API 暂未被 go-cqhttp 支持)

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%B8%85%E7%90%86%E7%BC%93%E5%AD%98
        """
        self.add("/clean_cache")

    def reload_event_filter(
        self
    ) -> None:
        """
        重载 go-cqhttp 事件过滤器

        Args:
            `file`: str 事件过滤器文件

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E9%87%8D%E8%BD%BD%E4%BA%8B%E4%BB%B6%E8%BF%87%E6%BB%A4%E5%99%A8
        """
        self.add("/reload_event_filter")

    def cqhttp_download_file(
        self,
        url: str,
        headers,
        thread_count: int
    ):
        """
        go-cqhttp 的内置下载

        Args:
            `url`: str 链接地址
            `headers`: 自定义请求头
            `thread_count`: int 下载线程数

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6%E5%88%B0%E7%BC%93%E5%AD%98%E7%9B%AE%E5%BD%95
        """
        return self._link("/download_file", {
            "url": url,
            "headers": headers,
            "thread_count": thread_count
        })["file"]

    async def _cqhttp_download_file(
        self,
        url: str,
        headers,
        thread_count: int
    ):
        """
        go-cqhttp 的内置下载 (异步)

        Args:
            `url`: str 链接地址
            `headers`: 自定义请求头
            `thread_count`: int 下载线程数

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6%E5%88%B0%E7%BC%93%E5%AD%98%E7%9B%AE%E5%BD%95
        """
        return (await self._asynclink("/download_file", {
            "url": url,
            "headers": headers,
            "thread_count": thread_count
        }))["data"]["file"]

    def check_url_safely(
        self,
        url: str
    ):
        """
        检查链接安全性

        Args:
            `url`: str 需要检查的链接

        Returns:
            `level`: int 安全等级, `1`: 安全 `2`: 未知 `3`: 危险

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E9%93%BE%E6%8E%A5%E5%AE%89%E5%85%A8%E6%80%A7
        """
        return self._link("/check_url_safely", {
            "url": url
        })

    def _get_word_slices(
        self,
        content: str
    ):
        """
        获取中文分词 ( 隐藏 API )

        Args:
            `content`: str 内容

        Returns:
            `slices`: list[str] 词组

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D-%E9%9A%90%E8%97%8F-api
        """

        return self._link("/.get_word_slices", {
            "content": content
        })

    def _handle_quick_operation(
        self,
        context,
        operation: dict[str, Any]
    ):
        """
        对事件执行快速操作 ( 隐藏 API )

        Args:
            `context`: 事件数据对象, 可做精简, 如去掉 `message` 等无用字段
            `operation`: 快速操作对象, 例如 `{"ban": true, "reply": "请不要说脏话"}`

        go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E5%AF%B9%E4%BA%8B%E4%BB%B6%E6%89%A7%E8%A1%8C%E5%BF%AB%E9%80%9F%E6%93%8D%E4%BD%9C-%E9%9A%90%E8%97%8F-api
        """
        self.add("/.handle_quick_operation", {
            "context": context,
            "operation": operation
        })
