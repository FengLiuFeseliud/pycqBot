message 消息对象从 v0.3.3 起被添加

所有关于 群/私聊 消息事件都可以获取到 message 消息对象

> [!note]
>
> 消息对象属性有原 go-cqhttp 群/私聊 消息的所有数据可以参考
>
> [https://docs.go-cqhttp.org/event/#私聊消息](https://docs.go-cqhttp.org/event/#私聊消息)
>
> [https://docs.go-cqhttp.org/event/#群消息](https://docs.go-cqhttp.org/event/#群消息)

## message 类属性

除了其它原 go-cqhttp 群/私聊 数据属性，之外还提供了其他属性使用

### code

自动解析出的 cqCode 字典

### code_str

自动解析出的 cqCode 字符串

## message 类函数

原 cqHttpApi 中仍旧可以使用这里的相关函数，但使用 message 类函数更加简洁

### reply

回复该消息，会自动添加回复 cqcode

> **`message`** 需发送的字符串
>
> **`auto_escape`** 消息内容是否作为纯文本发送 (即不解析 CQ 码)，只在 `message` 字段是字符串时有效，默认 False

### reply_not_code

回复该消息不带 cqcode

> **`message`** 需发送的q字符串
>
> **`auto_escape`** 消息内容是否作为纯文本发送 (即不解析 CQ 码)，只在 `message` 字段是字符串时有效，默认 False

### record

存储该消息

> **`time_end`** 消息存储有效时长 单位秒