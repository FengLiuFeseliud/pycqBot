# 介绍

## 什么是 pycqBot？

pycqBot 是一个基于 go-cqhttp 的 Ptyhon QQ bot 框架

内部使用异步进行处理，外部直接使用

特点搭建快速使用简单，只须一点点 Ptyhon 基础即可使用！

自动化的 cqCode 解析，全面的指令权限设置

## 安装

pycqBot 的安装十分方便

```bash
# 使用 pip 安装
pip install pycqBot
```

## 快速上手

**初始化一个 bot**

```python
from pycqBot.cqApi import cqBot, cqHttpApi, cqLog

# 启用日志 默认日志等级 DEBUG
cqLog()

cqapi = cqHttpApi()
cqBot(cqapi,
    options={
        # 设置指令标识符 默认 "/"
        "commandSign": "#",
    },
)

# 堵塞主线程
input("")

# 成功启动可以使用 指令标识符+help 使用内置指令 help
```

**设置日志等级**

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

**设置第一个指令 echo 输出信息**

```python
cqapi = cqHttpApi()

# echo 函数
def echo(commandData, message, from_id):
    # 发送群消息
    cqapi.send_group_msg(from_id, " ".join(commandData))

cqBot(cqapi,
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        "QQ 群号"
    ],
    command = {
        # 设置指令为 echo
        "echo": {
            # 绑定 echo 函数, 函数名不需要与指令相同
            # 但我还是推荐相同, 方便查看
            "function": echo,
            # echo 帮助
            "help": [
                "#echo - 输出文本"
            ]
        }
    },
    options={
        "commandSign": "#",
    },
)

input("")

# 成功启动可以使用 指令 help, echo
# 使用 指令标识符+echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助
```
**设置指令类型**

上面的指令 echo 没有设置指令类型，默认只能在群里使用

如何修改指令类型？非常简单修改指令字段 `type` 就行

```python
cqapi = cqHttpApi()

def echo(commandData, cqCodeList, message, from_id):
    # send_reply 会根据 message 自动判断发送
    cqapi.send_reply(message, " ".join(commandData))

cqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    command = {
        "echo": {
            "function": echo,
            "help": [
                "#echo - 输出文本"
            ],
            # 指令类型 群指令 "group", 私聊指令 "private", 全局指令 "all", 默认 "group"
            # 修改指令类型 为全局指令
            "type": "all"
        }
    },
    options={
        "commandSign": "#",
    },
)

input("")

# 成功启动后 指令 echo 支持在群和私聊中使用
```

**设置指令权限组**

上面的指令 echo 没有设置指令权限组，默认在群可以所有人使用

如果这个指令可以修改系统或者文件，是很危险的

如何修改指令权限组？非常简单修改指令字段 `user` 就行

```python
cqapi = cqHttpApi()

def echo(commandData, cqCodeList, message, from_id):
    cqapi.send_reply(message, " ".join(commandData))

cqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    command = {
        "echo": {
            "function": echo,
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
        }
    },
    options={
        "commandSign": "#",
    },
)

input("")

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

**自动化的 cqCode 解析**

pycqBot 将自动解析消息中的 cqCode 并且向下传递

消息中的 cqCode 将自动解析为字典并添加到列表

```python
cqapi = cqHttpApi()

# 群消息勾子
def on_group_msg(message, cqCodeList):
    # 输出需处理群每一条群消息中的 cqCode 到终端
    for cqCode in cqCodeList:
        print(cqCode)

def code(commandData, cqCodeList, message, from_id):
    cqapi.send_reply(message, "这条消息解析到了 %s 条 cqCode!" % len(cqCodeList))

cqBot(cqapi,
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
    command = {
        # 注意使用空格分割指令与 cqCode 如 #code+空格+图片+...
        # 图片也是 cqCode 可以使用图片或者简单的 at
        "code": {
            "function": code,
            "help": [
                "#code - 输出消息 cqCode 数"
            ],
            "type": "all"
        }
    },
    options={
        "commandSign": "#",
    },
)

input("")
# 成功启动后 指令 code+空格+图片+... 会输出消息 cqCode 数
# 并且输出需处理群每一条群消息中的 cqCode 到终端
```

**设置消息中的 cqCode**

cqCode 名字，参数完全相同于 go-cqhttp cqCode，可以直接参考 go-cqhttp cqCode文档

如何使用 cqCode？ 下面是发送一张我的~~p站~~b站头像

```python
# 引入 image
from pycqBot.cqCode import image

cqapi = cqHttpApi()
def show(commandData, cqCodeList, message, from_id):
    # image("图片名", "图片url")
    cqapi.send_group_msg(from_id, "我的b站头像! %s" % image("head.jpg",
        "https://i1.hdslb.com/bfs/face/3ad60a0f5d22e182d7a2a822710d483bc16153e2.jpg"
    ))

cqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    command = {
        "show": {
            "function": show,
            "help": [
                "#show - 显示我的b站头像"
            ],
            "type": "all"
        }
    },
    options={
        "commandSign": "#",
    },
)

input("")
# 成功启动后 指令 show 发送一张我的b站头像
```
**重写 bot cq 事件**

bot 事件 名字，参数完全相同于 go-cqhttp cqCode，可以直接参考 go-cqhttp cqCode文档

如何使用 bot 事件？下面是一个简单防撤回实现

```python
# 继承 cqBot
class myCqBot(cqBot):

    # 重写 notice_group_recall 事件
    def notice_group_recall(self, message):
        # 获取被撤回的消息
        message = self.cqapi.get_msg(message["message_id"])["data"]
        # 重新发送被撤回的消息
        self.cqapi.send_reply(message, "有一条消息无了 群友还没看清楚呢！ %s：%s" % (
                message["sender"]["nickname"],
                message["message"]
            )
        )

cqapi = cqHttpApi()
# 使用新的 myCqBot
myCqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    options={
        "commandSign": "#",
    },
)

input("")
# 成功启动后 bot 可以防撤回
```

**bot 定时任务**

```python
cqapi = cqHttpApi()

def timejob(from_id):
    cqapi.send_group_msg(from_id, "test bot timing job!!!")

cqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    options={
        "commandSign": "#",
    },
    timing={
        # bot 会自动新开一个名为 timejob 的线程
        "timejob":{
            # 绑定函数 timejob
            "function": timejob,
            # 每隔5秒
            "timeSleep": 5
        }
    }
)
input("")
# 成功启动后每隔5秒发送 "test bot timing job!!!"
```
> [!tip]
> 这只是定时任务基础用法
>
> pycqBot 可以帮助我们写的模块自动监听 重置状态
>
> 定时任务详细使用参见文档