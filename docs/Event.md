# Event

除 群/私聊 消息事件是获取到 Message 消息对象, 其它所有事件上报都会获取到 Event 对象

`Message_Event` `Notice_Event` `Request_Event` `Meta_Event` 都继承自 Event

## 属性

> **`data`** 事件数据
>
> **`post_type`** 事件上报的类型
>
> **`sub_type`** 事件子类型

## 函数

### **`def get_event_sub_type(self) -> str:`**

获取事件副类型

### **`def get_event_name(self) -> str:`**

获取完整事件名

将 `post_type` `sub_type` 事件副类型 拼接为 cqEvent 事件函数名的格式

## Message_Event

消息事件

消息对象可以获取到 Message_Event 对象

### 属性

> **`message_type`** 消息类型

## Notice_Event

通知事件

### 属性

> **`notice_type`** 通知类型

## Request_Event

请求事件

### 属性

> **`request_type`** 请求类型

## Meta_Event

元事件

### 属性


> **`meta_event_type`** 元类型
