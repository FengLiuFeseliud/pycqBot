实现 bilibili 监听动态/直播 消息 自动解析 bilibili qq 小程序分享信息

## 插件配置

> **`monitorLive`** 监听直播 uid 列表
>
> **`monitorDynamic`** 监听动态 uid 列表
>
> **`timeSleep`** 监听间隔 (秒)

在 plugin_config.yml 配置插件, 监听碧蓝航线

```yaml
# plugin_config.yml

bilibili:
    monitorLive:
        # 碧蓝航线
        - 233114659
        # 碧蓝海事局
        - 205889201

    monitorDynamic:
        # 碧蓝航线
        - 233114659
        # 碧蓝海事局
        - 205889201
    
    # 监听间隔 30s
    timeSleep: 30
```

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