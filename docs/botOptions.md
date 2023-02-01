# pycqBot v0.4.x

## 选项

> **`cqapi`** cqHttpApi 对象 必须 (使用 create_bot 创建时不需要)
> 
> **`host`** 正向 websocket 地址
> 
> **`group_id_list`** 需处理群列表 为空全部处理
> 
> **`user_id_list`** 需处理私信列表 为空全部处理
> 
> **`options`** options 选项

**on_group_msg 的使用**

绑定一个函数，所有需处理群消息都会调用 on_group_msg

这个函数会被提供一个参数

> `message` 当前群消息

```python
cqapi = cqHttpApi()

def on_group_msg(message: Message):
    print("新消息！%s" % message["message"])
    print("cq_code_list len: %s" % len(message.code))

bot = cqapi.create_bot(
    group_id_list=[
        "QQ 群号"
    ],
)

bot.on_group_msg = on_group_msg

bot.start()
```

**on_private_msg 的使用**

与 on_group_msg 一致只不过是需处理私信都会调用

可以直接参考 on_group_msg

## options 选项

> **`debug`** websocket 会话 debug 默认False
> 
> **`admin`** bot 管理员列表 默认为空
> 
> **`commandSign`** 指令标志符 默认 "/"
> 
> **`help_text`** 帮助信息模版
> 
> **`messageSql`** 长效消息存储
>
> **`messageSqlPath`** 长效消息存储 数据库目录
> 
> **`messageSqlClearTime`** 长效消息存储 清理间隔
>

**help_text 的使用**

可以随意修改 指令 help 帮助信息样式

插入 `{help_command_text}` 就可以插入自动生成的帮助信息

```python
cqapi = cqHttpApi()

bot = cqapi.create_bot(
    options={
        # 注意转意!
        "help_text": "这是新的帮助信息!!!\\n本bot帮助信息!\\n{help_command_text}\\npycqbot v0.1.0"
    },
)

bot.start()
```

> [!attention]
> 帮助信息只会在启动时自动生成 动态添加的指令帮助不会生效
>
> 需重新生成再次调用 _set_help_text

> [!tip]
> 重写 _set_help_text 就可以修改自动生成的帮助信息样式
>
> 我纯懒狗不太想动这个

## 指令

使用 `bot.command` 定义指令

> **`function`** 指令绑定函数 必须
> 
> **`command_name`** 指令名 多个支持数组
> 
> **`options`** 指令选项

指令选项 `options` 为字典，目前支持以下选项

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
> **`message`** 当前消息对象

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

def echo(commandData, message: Message):
    message.reply( " ".join(commandData))

bot = cqapi.create_bot()

bot.command(echo, "echo"， {
    # 指令帮助信息
    "help": [
        "#echo - 输出文本",
        "   这个指令没有参数~",
        "   这个指令所有用户可用~",
    ]
})

bot.start()
```

## 定时任务

使用 `bot.timing` 定义定时任务

> **`function`** 定时任务绑定函数 必须
> 
> **`timing_name`** 定时任务名称
> 
> **`options`** 定时任务选项

定时任务选项 `timing` 为字典，目前支持以下选项

> **`timeSleep`** 定时任务间隔 单位秒 必须
> 
> **`ban`** 定时任务在何处被禁用列表

被绑定函数可以获得以下值

> **`from_id`** 当前执行的群号

> [!tip]
> 通过 bot 事件让定时任务更加灵活！

## bot 操作

### bot.start

> `go_cqhttp_path` go-cqhttp 所在目录 默认当前目录
>
> `print_error` 是否只输出 go-cqhttp 的错误与警告日志 默认 True 输出
>
> `start_go_cqhttp` 是否启动 go-cqhttp 默认 True 启动