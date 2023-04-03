# Message

所有关于 群/私聊 消息事件都可以获取到 Message 消息对象

## 属性

> [!note]
>
> 消息对象属性有原 go-cqhttp 群/私聊 消息的所有数据可以参考
>
> [https://docs.go-cqhttp.org/event/#私聊消息](https://docs.go-cqhttp.org/event/#私聊消息)
>
> [https://docs.go-cqhttp.org/event/#群消息](https://docs.go-cqhttp.org/event/#群消息)

除了其它原 go-cqhttp 群/私聊 消息数据共有属性，之外还提供了其他属性使用

> **`code`** 自动解析出的 cqCode 字典
>
> **`code_str`** 自动解析出的 cqCode 字符串
>
> **`event`** 消息事件对象
>
> **`sender`** 与 go-cqhttp 不同, 这里 `sender` 将是发送者 [User](/pycqBot/User) 对象

## 函数

[cqHttpApi](/pycqBot/cqHttpApi) 中仍旧可以使用这里的相关函数，但使用 message 类函数更加简洁

**`def reply(self, message: str, auto_escape: bool=False) -> None:`**

回复该消息，会自动添加回复 cqcode

> **`message`** 需发送的字符串
>
> **`auto_escape`** 消息内容是否作为纯文本发送 (即不解析 CQ 码)，默认 False

**`def reply_not_code(self, message: str, auto_escape: bool=False) -> None:`**

回复该消息不带 cqcode

> **`message`** 需发送的字符串
>
> **`auto_escape`** 消息内容是否作为纯文本发送 (即不解析 CQ 码)，默认 False

**`def record(self, time_end: int) -> None:`**

存储该消息

> **`time_end`** 消息存储有效时长 单位秒

## Private_Message

私聊消息

私聊消息事件可以获取到继承 Message 类的 Private_Message 消息对象

### 函数

> 暂无

## Group_Message

群消息

群消息事件可以获取到继承 Message 类的 Group_Message 消息对象

### 函数

**`def set_essence(self):`**

设置精华消息

**`def delete_essence(self):`**

移出精华消息
