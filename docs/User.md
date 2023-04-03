# User

可以从 Message 对象 sender 属性获取到 User 对象

## 函数

[cqHttpApi](/pycqBot/cqHttpApi) 中仍旧可以使用这里的相关函数，但使用 User 类函数更加简洁

**`def get_stranger_info(self, no_cache: bool = False):`**

获取陌生人信息

> **`no_cache`** 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）

**`def delete(self):`**

删除好友

**`def delete_unidirectional(self):`**

删除单向好友

**`def send_message(self, message: str, auto_escape: bool = False):`**

发送私聊消息

> **`messages`** 要发送的内容
>
> **`auto_escape`**  消息内容是否作为纯文本发送 ( 即不解析 CQ 码 )

**`def send_forward_msg(self, messages: str):`**

发送合并转发

> **`messages`** 转发消息 [(设置可以被发送的转发消息?)](/pycqBot/cqCode)

**`def waiting_reply(self, sleep: int):`**

发送消息并等待回复，在指令中使用时不会堵塞其他操作

等待超时返回 None 用于进行判断

> **`sleep`** 等待时间 单位秒

## Private_User

私聊用户

### 函数

> 同上

## Group_User

群聊用户

### 函数

**`def poke(self):`**

群戳一戳

**`def ban(self, duration: int = 30):`**

群禁言

> **`duration`** 禁言持续时间 单位秒

**`def kick(self, reject_add_request: bool = False):`**

群踢人

> **`reject_add_request`** 拒绝此人的加群请求

**`def admin(self, enable: bool):`**

设置群管理员

> **`enable`** true 为设置, false 为取消

**`def set_card(self, card: str):`**

设置群名片 ( 群备注 )

> **`card`**  群名片内容

**`def set_special_title(self, title: str, duration: int = -1):`**

设置群专属头衔

> **`title`** 群专属头衔内容
>
> **`duration`** 持续时间 单位秒