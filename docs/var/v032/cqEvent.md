支持所有 go-cqhttp API Event，同名与 pycqBot 事件函数

因此你可以直接参考 go-cqhttp Event 文档来使用 pycqBot 中的事件

> [!attention]
>
> 目前不支持频道事件 ~~我也不用这个啊频道有什么用？~~

> [!note]
>
> go-cqhttp Event 文档地址
>
> [https://docs.go-cqhttp.org/event](https://docs.go-cqhttp.org/event)

## 内置事件

以下为 pycqBot 中的内置事件，可以在某些时候调用我们定义的函数，或者修改日志打印

使用很简单，直接重写事件函数，以下是一个简单的回复 at

```python
cqapi = cqHttpApi()

# 继承 cqBot
class myCqBot(cqBot):

    # 重写 at_bot 事件
    def at_bot(self, message, cqCode):
        # 回复 at
        cqapi.send_reply(message, "你好!")
        # 调用原 at_bot 事件的日志写入
        return super().at_bot(message, cqCode)

# 使用新的 myCqBot
bot = myCqBot(cqapi, host="ws://127.0.0.1:5700",
    group_id_list=[
        "QQ 群号"
    ],
)

bot.start()
```

### meta_event_connect

连接响应

默认输出日志并执行 bot _meta_event_connect

_meta_event_connect 会根据 auto_timing_start 启动定时任务并保存 bot qq号

可以获取以下值

> **`message`** websocket 连接响应消息 (由 go-cqhttp 返回 有当前 bot 信息)

### check_command

指令开始检查，可以获取以下值

> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

### at_bot

接收到 at bot，可以获取以下值

> **`message`** 当前消息
>
> **`cqCode_list`** 当前 at 消息的 cqCode 列表
>
> **`cqCode`** 当前 at 的 cqCode


### at

接收到 at，可以获取以下值

> **`message`** 当前消息
>
> **`cqCode_list`** 当前 at 消息的 cqCode 列表
>
> **`cqCode`** 当前 at 的 cqCode

### timing_start

启动定时任务

默认输出日志并启动定时任务

### timing_jobs_start

群列表定时任务准备执行，可以获取以下值

> **`job`** 当前定时任务设置 (可以获取当前定时任务名称)
>
> **`run_count`** 当前定时任务执行次数

> [!tip]
>
> 在这里可以放你自己模块的需监听的函数并在模块里准备好数据

### timing_job_end 

> [!attention]
>
> 这里并没有执行完成定时任务，而是遍历出群列表中的一个群执行完一次定时任务

定时任务被执行，可以获取以下值

> **`job`** 当前定时任务设置 (可以获取当前定时任务名称)
>
> **`run_count`** 当前定时任务执行次数
>
> **`group_id`** 当前执行完的群号

> [!tip]
>
> 这里可以根据你需求使用

### timing_jobs_end

> [!attention]
>
> 这里遍历完了整个群列表，真正执行完成了一轮定时任务

群列表定时任务执行完成，可以获取以下值

> **`job`** 当前定时任务设置 (可以获取当前定时任务名称)
>
> **`run_count`** 当前定时任务执行次数

> [!tip]
>
> 在这里可以清除你自己模块在 timing_jobs_start 准备好的数据，来准备下一轮

### runTimingError

定时任务执行错误，可以获取以下值

> **`job`** 当前定时任务设置 (可以获取当前定时任务名称)
>
> **`run_count`** 当前定时任务执行次数
>
> **`err`** 捕获到的错误
>
> **`group_id`** 当前执行错误的群号

> [!attention]
>
> 这里和 timing_job_end 一样，并没有没有执行完成一轮定时任务

### notCommandError

指令不存在时错误，可以获取以下值

默认输出日志并回复错误消息

> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

### banCommandError

指令被禁用时错误，可以获取以下值

默认输出日志并回复错误消息

> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

### userPurviewError

指令用户组权限不足时错误，可以获取以下值

默认输出日志并回复错误消息

> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

### purviewError

指令权限不足时错误 (无 admin 权限)，可以获取以下值

默认输出日志并回复错误消息

> **`message`** 当前消息
>
> **`from_id`** 来源 id qq/群号

### runCommandError

指令运行时错误，可以获取以下值

默认输出日志并回复错误消息

> **`message`** 当前消息
>
> **`err`** 捕获到的错误
>
> **`from_id`** 来源 id qq/群号

