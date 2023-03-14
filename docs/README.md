# 介绍

## 什么是 pycqBot？

pycqBot 是一个基于 go-cqhttp 的 Ptyhon QQ bot 框架

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
from pycqBot.cqApi import cqHttpApi, cqLog

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
from pycqBot import Message

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
def show(commandData, message: Message):
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

    cqapi.send_group_forward_msg(message.group_id, node_list(message_list, 
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
# 继承 cqBot
class myCqBot(cqBot):

    # 重写 notice_group_recall 事件
    def notice_group_recall(self, message):
        # 获取被撤回的消息
        message = self.cqapi.get_msg(message["message_id"])["data"]
        # 重新发送被撤回的消息
        self.cqapi.send_group_msg(message["group_id"], "有一条消息无了 群友还没看清楚呢！ %s：%s" % (
                message["sender"]["nickname"],
                message["message"]
            )
        )

cqapi = cqHttpApi()
# 使用新的 myCqBot
bot = myCqBot(cqapi, host="ws://127.0.0.1:5700",
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

### 多文件 / 模块化 编写

v0.3.0 的更新实现了模块化的编写

一个 pycqBot 需要一个入口文件， 一个 bot 配置文件，一个 bot 指令配置文件， 多个功能文件

也可能有，自定义 botClass 文件，自定义 cqHttpApiClass 文件

这里简单创建一个有自定义 botClass 文件的项目

**如下创建目录与文件**

入口 main.py

bot 配置文件 bot_src/bot.py

实列化出功能类 配置指令 bot_src/bot_fun.py

自定义 botClass bot_src/mybot.py

功能文件 bot_src/myClass.py

**入口 main.py**

```python
# 从 bot 配置文件 bot_src/bot.py 引入 bot
from bot_src.bot import bot

if __name__ in "__main__":
    # 启动 bot
    bot.start()
```

**bot 配置文件 bot_src/bot.py**

```python
# 引入 mybot.py 在 mybot.py 中引入 bot_fun.py 所有的函数与变量 避免循环引入
# 当然你可以直接在 bot.py 自定义 botClass
# 如果不用自定义 botClass 直接引入 bot_fun.py 所有的函数与变量就行
from .mybot import *

# 使用自定义 botClass
bot = myCqBot(cqapi, "ws://127.0.0.1:5700", options={
    "admin": [
        "bot 管理员 qq"
    ],
})

# 绑定 pid 指令函数 并创建三个指令 "pid", "p", "id"
bot.command(pid, ["pid", "p", "id"], {
    "type": "all"
})

# 绑定 simg 指令函数 并创建三个指令 "simg", "user", "img"
bot.command(simg, ["simg", "user", "img"], {
    "type": "all"
})
```

**实列化出功能类 配置指令 bot_src/bot_fun.py**

```python
from pycqBot.cqApi import cqHttpApi, cqLog
from pycqBot.module import pixiv
from pycqBot import Message
from logging import INFO

# 设置日志等级
cqLog(INFO)

cqapi = cqHttpApi()
cqpixiv = pixiv(cqapi, "pixivBot", "qq 号", "127.0.0.1:7890", "你的 pixiv COOKIE")

# 创建 pid 指令函数
def pid(cdata, message: Message):
    cqpixiv.search_pid(cdata[0], msg)

# 创建 simg 指令函数
def simg(cdata, message: Message):
    cqpixiv.search_user_image_random(cdata[0], cdata[1], msg)
```

**自定义 botClass bot_src/mybot.py**

```python
# 引入 bot_fun.py 所有的函数与变量
from .bot_fun import *
from pycqBot.cqApi import cqBot

class myCqBot(cqBot):

    def on_private_msg(self, message):
        for cq_code in message.code:
            if cq_code["type"] == "image":
                cqapi.download_img(cq_code["data"]["file"])
                message.reply("保存图片 %s..." % cq_code["data"]["file"])

    def at_bot(self, message, cqCode_list, cqCode):
        message.reply("你好!")
        return super().at_bot(message, cqCode_list, cqCode)
```

**功能文件 bot_src/myClass.py**

这里只用在这里做自己的功能类，然后在 `bot_src/bot_fun.py` 中实列出来并在指令函数中使用

同理可以多个 类似`from pycqBot.module import pixiv` 引入了一个功能类并使用

### 插件编写

所有插件需要放在 plugin 目录

**如下创建目录与文件**

创建 main.py

创建 plugin 目录

创建 plugin/myPlugin.py

> [!attention]
> 插件文件名需要和类一致
> 插件类必须继承 **`pycqBot.object.Plugin`** 不然会不进行加载

```python
# plugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        bot.command(self.test_plugin, "#test", {
            "type": "all"
        })
    
    def test_plugin(self, cdata, message: Message):
        message.reply("this 插件 myPlugin")
```

加载插件 myPlugin

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

在目录下创建 plugin_config.yml 文件

在插件名下配置插件

```yaml
# plugin_config.yml

myPlugin:
    text: "plugin_config.yml -> myPlugin"
```

在插件 `plugin_config` 中获取配置

```python
# plugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)
        # 获取 plugin_config.yml -> myPlugin -> text
        self.text = plugin_config["text"]

        bot.command(self.test_plugin, "#test", {
            "type": "all"
        })
    
    def test_plugin(self, cdata, message: Message):
        message.reply(self.text)
```
