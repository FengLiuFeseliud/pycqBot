实现 bilibili 监听动态/直播 消息 自动解析 bilibili qq 小程序分享信息

## 快速上手

### 监听动态/直播 消息

配置 bot 定时任务事件 `timing_jobs_start` `timing_jobs_end`

并创建一条定时任务即可使用，以下实现监听碧蓝航线动态

```python
# 引入模块 Bilibili
from pycqBot.module import Bilibili

# DEBUG
cqLog(logging.DEBUG)

# bilibili uid 列表
blhx = [
    # 碧蓝航线
    233114659,
    # 碧蓝海事局
    205889201,
    # 坐看云起i
    108344724,
    # 臧贺Lunmta
    36397742,
    # 井号5467
    4305299
]

cqapi = cqHttpApi()

# 监听动态 并监听直播
cqmb = Bilibili(cqapi, blhx, blhx)

class myCqBot(cqBot):

    # 在 timing_jobs_start 准备数据
    def timing_jobs_start(self, job, run_count):
        # 检查是否为 模块 bilibili 的定时任务
        if job["name"] == "cqmb":
            # 调用模块 bilibili 监听
            cqmb.monitor()
    
    # 在 timing_jobs_end 清除数据
    def timing_jobs_end(self, job, run_count):
        # 检查是否为 模块 bilibili 的定时任务
        if job["name"] == "cqmb":
            # 清除在 timing_jobs_start 中准备好的数据
            cqmb.monitor_send_clear()


def cqmb_send_new_msg(from_id):
    # 发送模块 bilibili 在 timing_jobs_start 中准备好的数据
    cqmb.monitor_send(from_id)


myCqBot(cqapi ,
    group_id_list=[
        "QQ 群号"
    ],
    timing={
        "cqmb":{
            # 绑定 cqmb_send_new_msg
            "function": cqmb_send_new_msg,
            # 根据请求限制调整 直到挂机不会出现请求被拦截
            "timeSleep": 35
        }
    }
)

input()
```

### 解析小程序分享信息

```python
# 引入模块 Bilibili
from pycqBot.module import Bilibili

# DEBUG
cqLog(logging.DEBUG)

def on_group_msg(message, cq_code_list):
    for cq_code in cq_code_list:
        # 如果为 cqCode json
        if cq_code["type"] == "json":
            # 直接传入 cqmb.get_link 判断是否为 bilibili 小程序
            # 如果是解析小程序并发送
            cqmb.get_link(message["group_id"], cq_code)


cqBot(cqapi ,
    # 使用新的 on_group_msg
    on_group_msg=on_group_msg,
    group_id_list=[
        "QQ 群号"
    ],
)

input()
```
## 选项

> **`cqapi`** cqHttpApi 对象 必须
> 
> **`monitor_live`** 需监听直播间的 uid 列表
>
> **`monitor_dynamic`** 需监听动态的 uid 列表

## 模块函数

### get_link

发送QQ小程序分享信息

> **`group_id`** 需发送到的群 必须
> 
> **`cq_code`** QQ 小程序的 cqCode 字典 必须

### monitor

监听 (查询) b站 动态/直播 消息

monitor 如果查询到更新将向模块待发送列表添加消息

> monitor 没有参数

### monitor_send

发送监听到的信息

monitor_send 会发送所有在模块待发送列表中的消息

> monitor_send 没有参数

### monitor_send_clear

清空监听到的信息

monitor_send_clear 会清空所有在模块待发送列表中的消息

> monitor_send_clear 没有参数

## 修改消息样式

你可能不满足于内置的信息样式，这里提供了自定义！

直接重写内置的信息样式函数，返回设置好的消息就能使用

### set_share_video_message

分享视频消息格式，可以获取以下值

> **`bv_json`** 视频信息
>
> **`cq_json`** QQ小程序 json
>
> **`surl`** 分享视频的短链接

### set_share_live_message

分享直播间消息格式，可以获取以下值

> **`liveData`** 直播间信息
>
> **`cq_json`** QQ小程序 json
>
> **`surl`** 分享直播间的短链接

### set_share_dynamic_message

分享动态消息格式，可以获取以下值

> **`dynamic_message`** 动态消息 (已经被模块设置为消息)
>
> **`cq_json`** QQ小程序 json
>
> **`surl`** 分享视频的短链接

### set_share_cv_message

分享专栏消息格式，可以获取以下值

> **`cv_text`** 专栏内容
>
> **`cv_viewinfo_json`** 专栏信息
>
> **`cq_json`** QQ小程序 json
>
> **`surl`** 分享视频的短链接

### set_share_cv_list_message

分享专栏文集消息格式，可以获取以下值

> **`cv_list_json`** 专栏文集信息
>
> **`cq_json`** QQ小程序 json
>
> **`surl`** 分享视频的短链接

### set_share_media_message

分享番剧消息格式，可以获取以下值

> **`cq_json`** QQ小程序 json

### set_live_message

开播消息格式，可以获取以下值

> **`liveData`** 直播间信息

### set_live_end_message

下播消息格式，可以获取以下值

> **`liveData`** 直播间信息

### set_dynamic_forward_message

动态消息 转发动态消息格式，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id
>
> **`forward_dynamic_msg`** 转发动态消息

### set_dynamic_forward_delete_message

转发被删除动态消息格式，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id

### set_dynamic_message

动态消息 动态消息格式 (无图)，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id

### set_dynamic_big_message

动态消息 动态消息格式，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id

### set_dynamic_cv_message

动态消息 专栏消息格式，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id
>
> **`cv_text`** 专栏内容

### set_dynamic_video_message

动态消息 视频消息格式，可以获取以下值

> **`dynamic`** 动态消息 json
> 
> **`dynamic_id`** 动态 id

### set_dynamic_delete_message

记录的旧动态被删除，可以获取以下值

> **`dynamic_old_message`** 旧的动态消息

## bEvent

以下为模块中的内置事件，可以在某些时候调用我们定义的函数，或者修改日志打印

直接重写事件函数，就能使用

### monitorLiveError

监听直播信息时错误，内置日志输出

可以获取以下值

> **`err`** 捕获到的错误

### monitorDynamicError

监听动态信息时错误，内置日志输出

可以获取以下值

> **`err`** 捕获到的错误

### getShareVideoError

解析分享信息时错误，内置日志输出

可以获取以下值

> **`err`** 捕获到的错误

### biliApiError

请求 bilibili api 时错误，内置日志输出

可以获取以下值

> **`code`** 状态码
>
> **`err_msg`** 错误信息