# 介绍

## 什么是 pycqBot？

pycqBot 是一个基于 go-cqhttp 的 Python QQ bot 框架

内部使用异步进行处理，外部直接使用

特点搭建快速使用简单，只须一点点 Ptyhon 基础即可使用！

自动化的 cqCode 解析，全面的指令权限设置

支持模块化编写 bot 项目

## 安装

pycqBot 的安装十分方便

```bash
# 使用 pip 安装
pip install pycqBot
```

### 支持 PyPy

可以使用 PyPy3 进行性能提升

```bash
pypy3 -m pip install pycqBot
# 改用 PyPy 运行
pypy3 ./main.py
```

## 快速上手

### 初始化一个 bot

**注意启动前请[下载 go-cqhttp 最新版本](https://github.com/Mrs4s/go-cqhttp/releases) 并放在当前目录**

```python
from pycqBot import cqHttpApi, cqLog

# 启用日志 默认日志等级 DEBUG
cqLog()

cqapi = cqHttpApi()
bot = cqapi.create_bot()
bot.start()

# 成功启动可以使用 指令标识符+help 使用内置指令 help
```

成功启动后

![Alt](/img/bot1.png)

### 设置日志等级

与 python 的内置日志库 logging 一样，传入 logging 常量

```python
import logging

# 日志等级 DEBUG (默认)
cqLog(logging.DEBUG)

# 日志等级 INFO
cqLog(logging.INFO)
```

> [!tip]
>
> 其它日志等级参考 logging
>

### 设置第一个指令 echo 输出信息

```python
from pycqBot.data import Message

cqapi = cqHttpApi()

# echo 函数
def echo(commandData, message: Message):
    # 回复消息
    message.reply(" ".join(commandData))

bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        123456 # 替换为你的QQ群号
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ]
})

bot.start()

# 成功启动可以使用 指令 help, echo
# 使用 #echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助
```

### 链式调用

bot 的指令，定时任务都可以链式设置

```python
# 链式设置多个指令

# echo 函数
def echo(commandData, message: Message):
    # 回复消息
    message.reply(" ".join(commandData))

bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ]
}).command(echo, "echo2", {
    # echo 帮助
    "help": [
        "#echo2 - 输出文本"
    ]
}).command(echo, "echo3", {
    # echo 帮助
    "help": [
        "#echo3 - 输出文本"
    ]
}).start()
```

### 设置指令类型

上面的指令 echo 没有设置指令类型，默认只能在群里使用

如何修改指令类型？非常简单修改指令字段 `type` 就行

```python
cqapi = cqHttpApi()

# echo 函数
def echo(commandData, message: Message):
    message.reply(" ".join(commandData))

bot = cqapi.create_bot(
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ],
    # 指令类型 群指令 "group", 私聊指令 "private", 全局指令 "all", 默认 "group"
    # 修改指令类型 为全局指令
    "type": "all"
})

bot.start()

# 成功启动后 指令 echo 支持在群和私聊中使用
```

### 设置指令权限组

上面的指令 echo 没有设置指令权限组，默认在群可以所有人使用

如果这个指令可以修改系统或者文件，是很危险的

如何修改指令权限组？非常简单修改指令字段 `user` 就行

```python
cqapi = cqHttpApi()

def echo(commandData, message: Message):
    message.reply(" ".join(commandData))

bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        123456 # 替换为你的QQ群号
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ],
    "type": "all",
    """
    user: 指定可以使用该指令的权限组
        all 全部权限组可以使用
        nall 除了匿名组 全部权限组可以使用
        owner 群主可以使用
        admin 管理员可以使用
        member 群员可以使用
    可以指定多个组 用 "," 分割
    注意: user 和 admin 会同时生效
    如 admin:True + user:member 只有在 admin 表中的群员可以使用
    如 admin:True + user:admin,owner 只有在 admin 表中的 管理员/群主 可以使用
    """
    "user": "owner"
})

bot.start()
# 成功启动后 指令 echo 支持在群主使用
# 但是 type all 使私聊也可以使用
# 这就是鱼和熊掌不可兼得啊... 解决方法 type group
```

> [!tip]
> 提示: admin 权限也可以解决这个问题，使私聊也可以使用
>
> admin 权限为我们指定的用户
>
> 只有我们指定的用户可以使用指令，最安全
>
> admin 的使用可以参见文档这里不进行演示

### 自动化的 cqCode 解析

pycqBot 将自动解析消息中的 cqCode 并且向下传递

消息中的 cqCode 将自动解析为字典并添加到列表

```python
cqapi = cqHttpApi()

def on_group_msg(message: Message):
    # 输出需处理群每一条消息中的 cqCode 到终端
    for cqCode in message.code:
        print(cqCode)

def code(commandData, message: Message):
    message.reply("这条消息解析到了 %s 条 cqCode!" % len(message.code))

bot = cqapi.create_bot(
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

bot.on_group_msg = on_group_msg
bot.command(code, "code", {
    # 注意使用空格分割指令与 cqCode 如 #code+空格+图片+...
    # 图片也是 cqCode 可以使用图片或者简单的 at
    "help": [
        "#code - 输出消息 cqCode 数"
    ],
    "type": "all"
})

bot.start()
# 成功启动后 指令 code+空格+图片+... 会输出消息 cqCode 数
# 并且输出需处理群每一条群消息中的 cqCode 到终端
```

### 设置消息中的 cqCode

cqCode 名字，参数完全相同于 go-cqhttp cqCode，可以直接参考 go-cqhttp cqCode文档

如何使用 cqCode？ 下面是发送一张我的~~p站~~b站头像

```python
# 引入 image
from pycqBot.cqCode import image

cqapi = cqHttpApi()
def show(commandData, message: Message):
    # image("图片名", "图片url")
    message.reply("我的b站头像! %s" % image("head.jpg",
        "https://i1.hdslb.com/bfs/face/3ad60a0f5d22e182d7a2a822710d483bc16153e2.jpg"
    ))

bot = cqapi.create_bot(
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

bot.command(show, "show", {
    "help": [
        "#show - 显示我的b站头像"
    ],
    "type": "all"
})

bot.start()
# 成功启动后 指令 show 发送一张我的b站头像
```

### 转发消息

主要是可以用来发涩图，一次可以发最多200张

```python
# 引入 node_list image
from pycqBot.cqCode import node_list, image

cqapi = cqHttpApi()
def show(commandData, message: Group_Message):
    # 转发消息列表 转发三张我的头像
    message_list = [
        # image("图片名", "图片url")
        image("head.jpg",
        "https://i1.hdslb.com/bfs/face/3ad60a0f5d22e182d7a2a822710d483bc16153e2.jpg"
        ),
        image("head.jpg",
        "https://i1.hdslb.com/bfs/face/3ad60a0f5d22e182d7a2a822710d483bc16153e2.jpg"
        ),
        image("head.jpg",
        "https://i1.hdslb.com/bfs/face/3ad60a0f5d22e182d7a2a822710d483bc16153e2.jpg"
        )
    ]

    message.send_forward_msg(message.group_id, node_list(message_list, 
        "test",
        "QQ号"
    ))

bot = cqapi.create_bot(
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

bot.command(show, "show", {
    "help": [
        "#show - 显示我的b站头像"
    ],
})

bot.start()
# 成功启动后 指令 show 转发三张我的头像
```

### 重写 bot cq 事件

bot 事件 名字，参数完全相同于 go-cqhttp cqCode，可以直接参考 go-cqhttp cqCode文档

如何使用 bot 事件？下面是一个简单防撤回实现

```python
from pycqBot import cqBot
from pycqBot.data import *

# 继承 cqBot
class myCqBot(cqBot):

    # 重写 notice_group_recall 事件
    def notice_group_recall(self, event: Notice_Event):
        # 获取被撤回的消息
        message = self.cqapi.get_msg(event.data["message_id"])["data"]
        # 重新发送被撤回的消息
        self.cqapi.send_group_msg(message["group_id"], "有一条消息无了 群友还没看清楚呢！ %s：%s" % (
                message["sender"]["nickname"],
                message["message"]
            )
        )

cqapi = cqHttpApi()
# 使用新的 myCqBot
bot = myCqBot(cqapi,
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

bot.start()
# 成功启动后 bot 可以防撤回
```

### bot 定时任务

```python
cqapi = cqHttpApi()

def timejob(from_id):
    cqapi.send_group_msg(from_id, "test bot timing job!!!")

bot = cqapi.create_bot(
    group_id_list=[
        123456 # 替换为你的QQ群号
    ],
)

# bot 会自动新开一个名为 timejob 的线程
bot.timing(timejob, "timejob", {
    # 每隔5秒
    "timeSleep": 5
})

bot.start()
# 成功启动后每隔5秒发送 "test bot timing job!!!"
```

> [!tip]
> 这只是定时任务基础用法
>
> pycqBot 可以帮助我们写的模块自动监听 重置状态
>
> 定时任务详细使用参见文档

### 插件编写

所有插件需要放在 bot 入口文件目录下 `plugin` 目

#### **如下创建目录与文件**

创建 `main.py`

创建 `plugin` 目录

创建 `plugin/myPlugin` 目录

创建 `plugin/myPlugin.py`

> [!attention]
> 插件目录名 需要和 插件入口文件 插件入口类 一致
> 插件类必须继承 **`pycqBot.object.Plugin`** 不然会不进行加载

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin
from pycqBot.data import *


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        bot.command(self.test_plugin, "test", {
            "type": "all"
        })
    
    def test_plugin(self, cdata, message: Message):
        message.reply("this 插件 myPlugin")
```

加载插件 `myPlugin`

```python
# main.py
from pycqBot.cqApi import cqHttpApi, cqLog
cqLog()

cqapi = cqHttpApi()
bot = cqapi.create_bot()

bot.plugin_load(["myPlugin"])

bot.start()
```

### 插件配置

在 bot 入口文件目录下创建 `plugin_config.yml` 文件

在插件名下配置插件

```yaml
# plugin_config.yml

myPlugin:
    text: "plugin_config.yml -> myPlugin"
```

在插件 `plugin_config` 中获取配置

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin
from pycqBot.data import *


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)
        # 获取 plugin_config.yml -> myPlugin -> text
        self.text = plugin_config["text"]

        bot.command(self.test_plugin, "test", {
            "type": "all"
        })
    
    def test_plugin(self, cdata, message: Message):
        message.reply(self.text)
```
