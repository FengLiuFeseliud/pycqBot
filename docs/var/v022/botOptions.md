# pycqBot v0.2.x

## 选项

> **`cqapi`** cqHttpApi 对象 必须
> 
> **`on_group_msg`** 群信息勾子
> 
> **`on_private_msg`** 私信息勾子
> 
> **`group_id_list`** 需处理群列表 为空全部处理
> 
> **`user_id_list`** 需处理私信列表 为空全部处理
> 
> **`command`** 指令列表
> 
> **`timing`** 定时任务
> 
> **`options`** options 选项

**on_group_msg 的使用**

绑定一个函数，所有需处理群消息都会调用 on_group_msg

这个函数会被提供两个参数

> `message` 当前群消息
>
> `cq_code_list` 自动解析后的 cqCode 列表

```python
cqapi = cqHttpApi()

def on_group_msg(message, cq_code_list):
    print("新消息！%s" % message["message"])
    print("cq_code_list len: %s" % len(cq_code_list))

cqBot(cqapi,
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
)
input("")
```

**on_private_msg 的使用**

与 on_group_msg 一致只不过是需处理私信都会调用

可以直接参考 on_group_msg

## options 选项

> **`host`** go-cqhttp websocket 会话服务地址 默认127.0.0.1
> 
> **`port`** go-cqhttp websocket 会话服务端口 默认5700
> 
> **`debug`** websocket 会话 debug 默认False
> 
> **`admin`** bot 管理员列表 默认为空
> 
> **`commandSign`** 指令标志符 默认 "/"
> 
> **`help_text`** 帮助信息模版
> 
> **`auto_start`** 自动启动连接
> 
> **`auto_timing_start`** 自动启动定时任务

**help_text 的使用**

可以随意修改 指令 help 帮助信息样式

插入 `{help_command_text}` 就可以插入自动生成的帮助信息

```python
cqapi = cqHttpApi()

cqBot(cqapi,
    options={
        # 注意转意!
        "help_text": "这是新的帮助信息!!!\\n本bot帮助信息!\\n{help_command_text}\\npycqbot v0.1.0"
    },
)
input("")
```

> [!attention]
> 帮助信息只会在启动时自动生成 动态添加的指令帮助不会生效
>
> 需重新生成再次调用 _set_help_text

> [!tip]
> 重写 _set_help_text 就可以修改自动生成的帮助信息样式
>
> 我纯懒狗不太想动这个

**auto_start 的使用**

关闭后使用 `cqBot.link()` 手动启动

**auto_timing_start 的使用**

关闭后使用 `cqBot.timing_start()` 手动启动

## 指令

在选项 `command` 中定义指令，`command` 为字典

指令定义格式为键值对，键为指令，值为指令选项，目前支持以下选项

> **`function`** 指令绑定函数 必须
> 
> **`type`** 指令类型
> 
> **`admin`** 指令是否为 admin 指令
> 
> **`user`** 指令权限组
> 
> **`ban`** 指令在何处被禁用列表
> 
> **`help`** 指令帮助信息

被绑定函数可以获得以下值

> **`commandData`** 指令参数 (内部使用空格分割)
>
> **`cqCode_list`** 当前消息的 cqCode 字典列表
>
> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

**type 的使用**

指定指令类型

> **`group`** 群可用 默认
>
> **`private`** 私聊可用
>
> **`all`** 所有地方都可以使用

**admin 的使用**

指令是否为 admin 指令，默认 False 不是

配合 options 选项 admin 使用

**user 的使用**

指令权限组，可以指定多个组 用 "," 分割

> **`all`** 全部权限组可以使用 默认
>
> **`nall`** 除了匿名组 全部权限组可以使用
>
> **`owner`** 群主可以使用
>
> **`admin`** 管理员可以使用
>
> **`member`** 群员可以使用

> [!note]
> user 和 admin 会同时生效
>
> 如 admin:True + user:member 只有在 admin 表中的群员可以使用
>
> 如 admin:True + user:admin,owner 只有在 admin 表中的 管理员/群主 可以使用

**help 的使用**

指令帮助信息，这是个列表，每次一行加一元素

```python
cqapi = cqHttpApi()

def echo(commandData, cqCode_list, message, from_id):
    cqapi.send_group_msg(from_id, " ".join(commandData))

cqBot(cqapi,
    command = {
        "echo": {
            "function": echo,
            # 指令帮助信息
            "help": [
                "#echo - 输出文本",
                "   这个指令没有参数~",
                "   这个指令所有用户可用~",
            ]
        }
    },
)
input("")
```

## 定时任务

在选项 `timing` 中定义指令，`timing` 为字典

定时任务定义格式为键值对，键为定时任务名称，值为定时任务选项，目前支持以下选项

> **`function`** 定时任务绑定函数 必须
> 
> **`timeSleep`** 定时任务间隔 单位秒 必须
> 
> **`ban`** 定时任务在何处被禁用列表

被绑定函数可以获得以下值

> **`from_id`** 当前执行的群号

> [!tip]
> 通过 bot 事件让定时任务更加灵活！