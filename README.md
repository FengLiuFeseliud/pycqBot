# pycqBot

go-cqhttp python 框架，可以用于快速塔建 bot

### 	[基于 go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

### [项目地址](https://github.com/FengLiuFeseliud/pycqBot)

## 快速入门

安装 (未上传)

```bash
pip install pycqBot
```

测试 bot

```python
"""
一个监听所有消息的 bot

使用前启动 go-cqhttp
注意需要配置 ws 和 http
库默认地址 注意端口号
ws: 127.0.0.1:5700
http: 127.0.0.1:8000

配置文件参考项目 config.yml 文件
"""

from pycqBot import cqHttpApi, cqBot, cqLog, cqSocket

# log save
cqLog()
# cqHttpApi
cqapi = cqHttpApi()

# 实例化 bot
cqbot = cqBot(cqapi, group_id_list=[])
# 连接 go-cqhttp 服务使用 cqbot
cqSocket(cqbot)

# 堵塞主线程
input("")

"""
成功启动可以使用基本指令 $help
"""
```

## bot 设置

> cqHttpApi 名字 参数 完全相同于 go-cqhttp Api ，可以直接参考  go-cqhttp Api文档
>
> 如何使用 cqCode ？ 直接引入 cqCode
>
> cqCode 名字 参数 完全相同于 go-cqhttp cqCode ，可以直接参考  go-cqhttp cqCode文档
>
> ```python
> # 全部引入
> from pycqBot.cqCode import *
> # 按需引入
> # 引入 at 和 图片
> from pycqBot.cqCode import at, image
> 
> # 直接返回 cqCode 码
> print(at("qq号"))
> ```
>
> 解析 cqCode / 生成其他  cqCode
>
> ```python
> from pycqBot.cqCode import get_cq_code, set_cq_code
> 
> """
> 指定 cqCode 字段 [CQ:at,qq=xxxxx]
> 直接返回 cqCode 字典
> {
> 	"type": "at",
> 	"data":{
> 		"qq": "xxxxx"
> 	}
> }
> """
> print(get_cq_code("[CQ:at,qq=xxxxx]"))
> 
> # 生成其他 cqCode
> print(set_cq_code({
>     # 类型
>     "type": "test",
>     # 值
>     "data":{
>         "text": "my cqCode"
>     }
> }))
> """
> 直接返回 cqCode 字段 [CQ:test,text=cqCode]
> """
> ```
>
> bot 设置
>
> `cqBot(cq_api, on_group_msg=None, on_private_msg=None,
>             group_id_list=[], user_id_list=[],
>             command={}, 
>             options={})` 实例化 cqBot
>
> cq_api：cqHttpApi 实例
>
> on_group_msg： 接受到群消息勾子
>
> on_private_msg：接受到私聊消息勾子
>
> group_id_list：需处理消息群列表，空为全部处理，默认空
>
> user_id_list：需处理消息私信人列表，空为全部处理，默认空
>
> command：指令列表
>
> options：其他选项
>
> ## 基本指令设置
>
> 设置一个群指令 test 所有人可用
>
> ```python
> from pycqBot import cqHttpApi, cqBot, cqSocket
> 
> cqapi = cqHttpApi()
> 
> # test
> def test(commandData, message, from_id):
>     # 发送信息
>     cqapi.send_group_msg(from_id, "指令 test 被使用了!")
> 
> cqbot = cqBot(cqapi, 
> 	command={
>         # 设置一个群指令 test 所有人可用
>         "test":{
>             # 绑定 test
>             "function": test
>             # 指令帮助
>             "help":[
>                 "指令 test 发送一条信息"
>             ]
>         }
>     }
> )
> cqSocket(cqbot)
> 
> input("")
> """
> 成功设置启动可以使用: $help $test
> $help 自动添加 $test 指令帮助
> """
> ```
>
> *详细指令设置*
>
> ```python
> cqbot = cqBot(cqapi, 
> 	command={
>         # 设置一个群指令 test 所有人可用
>         "test":{
>             # 绑定方法
>             "function": test
>             # 指令类型 群指令 "group", 私聊指令 "private", 默认 "group"
>             "type": "group"
>             # 指令是否为权限指令 False 否, True 是, 默认 False
>             "admin": False
>             # 这条指令在何处被禁用, 为空不被禁用 qq/群号
>             "ban": []
>             # 指令帮助 会自动添加到 help 指令
>             "help":[
>                 "指令 test 发送一条信息"
>             ]
>         }
>     }
> )
> ```
>
> 详细 bot options 选项
>
> admin：*管理员列表*
>
> commandSign：*指令标志符*
>
> help_text：*帮助信息模版*  在需要使用指令帮助的地方加上 {help_command_text}
>
> ## 重写 bot 事件
>
> 拥有 go-cqhttp 所有同名事件 可以参考 go-cqhttp 文档
>
> 其他 pycqBot 事件 / 如何重写
>
> ```python
> from pycqBot import cqHttpApi, cqBot, cqSocket
> 
> cqapi = cqHttpApi()
> 
> # 继承 cqBot
> class myCqBot(cqBot):
> 	
>     # 重写启动成功事件
>     def meta_event_connect(self, message):
>         # 新加入的 print
>         print("新加入的 print !!!")
>         return super().meta_event_connect(message)
> 
> # 使用新 bot
> cqbot = myCqBot(cqapi, group_id_list=[])
> 
> cqSocket(cqbot)
> input("")
> ```

> 其他 pycqBot 事件
>
> ```python
> from pycqBot import cqBot
> 
> 
> class myCqBot(cqBot):
>     """
>     所有可用参数
>     message: 被触发时的消息
>     from_id: 从哪里被触发 qq/群号
>     err: 错误
>     """
>     
>     def meta_event_connect(self, message):
>         """
>         连接响应
>         """
>     
>     def user_log_srt(self, message):
>         """
>         user 打印 格式
>         """
>     
>     def check_command(self, message, from_id):
>         """
>         指令开始检查勾子
>         """
>     
>     def notCommandError(self, message, from_id):
>         """
>         指令不存在时错误
>         """
>     
>     def banCommandError(self, message, from_id):
>         """
>         指令被禁用时错误
>         """
>     
>     def purviewError(self, message, from_id):
>         """
>         指令权限不足时错误
>         """
>     
>     def runCommandError(self, message, err, from_id):
>         """
>         指令运行时错误
>         """
> ```
>
> 