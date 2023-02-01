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

> **`ip`** go-cqhttp Http 服务地址 默认127.0.0.1
>
> **`port`** go-cqhttp Http 服务端口 默认8000
> 
> **`download_path`** 文件下载目录 默认当前 bot 运行目录下的 download
> 
> **`chunk_size`** 文件下载缓存 默认1024kb

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

bot = cqBot(cqapi ,
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
)

input()
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

bot = cqBot(cqapi ,
    # 绑定函数 on_group_msg
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
)

input()
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

cqBot(cqapi,
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
)

input()
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