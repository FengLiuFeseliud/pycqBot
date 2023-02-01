有绝大部分的 go-cqhttp API 同名函数，大部分参数一致

因此你可以直接参考 go-cqhttp API 文档来使用 cqHttpApi

> [!attention]
>
> 目前不支持频道 API ~~我也不用这个啊频道有什么用？~~

> [!note]
>
> go-cqhttp API 文档地址
>
> [https://docs.go-cqhttp.org/api](https://docs.go-cqhttp.org/api)

## 选项

> **`host`** go-cqhttp Http 服务地址 默认http://127.0.0.1:8000
> 
> **`download_path`** 文件下载目录 默认当前 bot 运行目录下的 download
> 
> **`chunk_size`** 文件下载缓存 默认1024kb

## 內置函数

cqHttpApi 提供了一些函数，使编写 bot 更加方便

### create_bot

直接创建一个 bot (就是创建一个 bot 实例返回)

### record_message

长效消息存储，将消息数据暂时存储在数据库，超过有效时间删除

默认 bot 不开启，需要将 bot options 中的 `messageSql` 设置为 True

默认每60秒检查一次消息有效时间，可通过 bot options 中的 `messageSqlClearTime` 设置

> **`message_data`** 消息数据字典 (bot 返回的消息)
> 
> **`time_end`** 消息有效时间 单位秒

### record_message_get

长效消息存储 获取，使用指定 qq 在数据库中检索暂储消息

返回一个数组，数组元素为元组，没有数据返回空数组

元组中的数据按以下排列

> (qq, 存储时间, 存储有效时间, 消息数据字符串)

> [!attention]
>
> 消息数据字符串需要使用 eval 转换为字典

### reply

等待指定 qq 的下一条消息 (可以理解为指定 qq 回复 bot)，在指令中使用时不会堵塞其他操作

等待超时返回空字典用于进行判断

> **`user_id`** 指定等待 qq
> 
> **`sleep`** 等待时间 单位秒

**消息存储与 reply 一起使用的例子**

以下例子使用 `#set` 时可以存储二次输入的消息有效时间一小时

使用 `#get` 时可以获取该用户存储的消息并显示出来

```python
cqapi = cqHttpApi()

bot = cqapi.create_bot(options={
    "messageSql": True
})

def get(_, __, msg, from_id):
    # 获取该条消息发送用户 qq 存储的消息
    message_list = cqapi.record_message_get(msg["user_id"])
    cqapi.send_reply(msg, "qq %s 存储了 %s 条消息 如有消息内容如下" % (msg["user_id"], len(message_list)))

    if message_list == []:
        return
        
    message_data = ""
    for message in message_list:
        message = eval(message[-1])
        message_data = "%s%s\n" % (message_data, message["message"])

    cqapi.send_reply(msg, message_data)

def set(_, __, msg, from_id):
    cqapi.send_reply(msg, "等待时间！20s")

    # 等待该条消息发送用户 二次输入
    data = cqapi.reply(msg["user_id"], 20)

    # 为空说明超时了也没进行输入
    if data == {}:
        cqapi.send_reply(msg, "超过等待时间！")
        return

    # 存储二次输入的消息
    # 存储时长 60 * 60 一小时
    cqapi.record_message(data, 60 * 60)

bot.command(get, "get")

bot.command(set, "set")

bot.start()
```


## 內置异步操作

### 异步图片下载 download_img

download_img 会向事件循环线程添加任务，不会影响 bot 线程

> **`file`** cqCode 中的图片缓存名

```python
cqapi = cqHttpApi(download_path="./test_download")

def on_group_msg(message, cq_code_list):
    for cq_code in cq_code_list:
        # 判断是否为图片
        if cq_code["type"] == "image":
            # 传入 cqCode 中的图片缓存名 
            cqapi.download_img(cq_code["data"]["file"])
            cqapi.send_reply(message, "保存图片 %s..." % cq_code["data"]["file"])

bot = cqapi.create_bot()
bot.on_group_msg = on_group_msg
bot.start()
```
> [!attention]
>
> 使用內置下载时将影响内部线程不要下载过大文件

### 异步文件下载 download_file

download_file 会向事件循环线程添加任务，不会影响 bot 线程

> **`file_name`** 文件名
>
> **`file_url`** 文件 url

> [!attention]
>
> 使用內置下载时将影响内部线程不要下载过大文件


### 向内部事件循环添加任务 add_task

> [!attention]
>
> 以下内容需要了解 Python 异步操作，一般情况不需要使用

add_task 会向事件循环线程添加任务，不会影响 bot 线程

> **`coroutine`** 协程对象

以下例子显示了如何使用 add_task

例子：成功启用将获取所有群消息详细并发送回去

```python
cqapi = cqHttpApi()

# 创建 async 函数 _on_group_msg
async def _on_group_msg(message, cq_code_list):
    data = {
        "message_id": message["message_id"]
    }
    # 使用內部 async 函数调用 go-cqhttp Api
    data = await cqapi._asynclink("/get_msg", data=data)
    # 发送
    cqapi.send_reply(message, "%s" % data)

# 创建非 async 函数 on_group_msg
def on_group_msg(message, cq_code_list):
    # 向内部事件循环线程添加任务, 调用 async 函数 _on_group_msg
    cqapi.add_task(_on_group_msg(message, cq_code_list))

bot = cqapi.create_bot()
bot.on_group_msg = on_group_msg
bot.start()
```

### 向内部事件循环添加 go-cqhttp Api 任务 add

> [!attention]
>
> 以下内容需要了解 Python 异步操作，一般情况不需要使用
>
> add 调用 Api 不会有返回值！

add 会向事件循环线程添加调用 go-cqhttp Api 任务，不会影响 bot 线程 

cqHttpApi 内部大量使用 add 使调用无返回值 Api 时不会影响 bot 线程

```python
"""
发送私聊消息
"""

cqapi = cqHttpApi()

post_data = {
    "user_id": user_id,
    "group_id": group_id,
    "message": message,
    "auto_escape": auto_escape
}
cqapi.add("/send_msg", post_data)

"""
发送群消息
"""
post_data = {
    "group_id":group_id,
    "message":message,
    "auto_escape":auto_escape
}
cqapi.add("/send_msg", post_data)

# 相当于

# 发送私聊消息
cqapi.send_private_msg()

# 发送群消息
cqapi.send_group_msg()
```

## cqHttpApi Event

cqHttpApi 事件可以在某些时候调用我们定义的函数，或者修改日志打印

使用很简单，直接重写事件函数

```python
# 继承 cqHttpApi
class myCqHttpApi(cqHttpApi):

    # 重写文件下载完成事件 download_end 
    def download_end(self, file_name, file_url, code):
        # 不调用原 download_end 日志输出, 修改输出
        print("文件下载好了, 但是我啥也不干, 还吞了日志输出捏:)")

# 使用修改好的 myCqHttpApi
cqapi = myCqHttpApi()

def on_group_msg(message, cq_code_list):
    for cq_code in cq_code_list:
        if cq_code["type"] == "image":
            cqapi.download_img(cq_code["data"]["file"])
            cqapi.send_reply(message, "保存图片 %s..." % cq_code["data"]["file"])

bot = cqapi.create_bot()
bot.on_group_msg = on_group_msg
bot.start()
# 成功启动自动下载群消息图片 并打印重写后的输出
```

### download_end

文件下载完成，可以获取以下值

> **`file_name`** 文件名
>
> **`file_url`** 文件 url
>
> **`code`** 状态码

### downloadFileError

文件下载失败，可以获取以下值

> **`file_name`** 文件名
>
> **`file_url`** 文件 url
>
> **`code`** 状态码

### downloadFileRunError

下载时发生错误，可以获取以下值

> **`err`** 捕获到的错误

### apiLinkError

cqapi 发生错误，可以获取以下值

> **`err_json`** 请求 go-cqhttp 返回的的错误信息

### apiLinkRunError

cqapi 请求时发生错误，可以获取以下值

> **`err`** 捕获到的错误