# 更新日志

如果没有需要的历史版本文档，说明版本之间差距不大 观看旧版本文档

#### v0.4.3

对 go-cqhttp 的自身上报消息支持增加两条消息协议

自身群消息上报 message_sent_group_normal

自身消息私聊上报 message_sent_private_friend

添加私聊合并转发支持 cqapi.send_private_forward_msg （go-cqhttp v1.0.0-rc2）

将匿名消息拆分成一条消息协议 message_group_anonymous

一个插件将拥有一个同名插件目录，以多文件开发

#### v0.4.0

添加插件编写

删除内置模块

#### v0.3.4

添加 windows 下启动 go-cqhttp

#### v0.3.3

自动启动配置 go-cqhttp 

添加消息对象

内置模块 pixiv 新增关注用户随机图

内置模块 pixiv 补充注释

#### v0.3.2

修复用户组无法解析

#### v0.3.1.1

重新添加心跳事件

优化性能 使用wsaccel

补充 recordMessage 日志

#### v0.3.0

大更新，优化 bot 初始化的方式，更加清晰，并且可以多文件模块化的编写功能

优化选项

添加等待回复

添加内置消息存储

新增内置模块 pixiv

#### v0.2.2

添加内置模块 bilibili 转发被删除动态消息格式 `set_dynamic_forward_delete_message`

优化 cqCode json 的支持，添加了转 cqCode json 格式和字典转 cqCode json 类型的方式

修复内置模块 bilibili 转发被删除动态，无法正常监听的问题

修复内置模块 bilibili 重复发送视频动态

#### v0.2.1

修复 bug 两处

#### v0.2.0

内部实现改为新开线程执行异步操作

新增内置模块 bilibili

优化 cqCode 的解析

优化错误捕捉

优化日志输出