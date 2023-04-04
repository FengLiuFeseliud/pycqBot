> [!attention]
> 从 v0.4.0 起改用内置插件

## 导入内置插件

导入内置插件只需要在插件名前加上 pycqBot.plugin.

```python
from pycqBot.cqApi import cqHttpApi, cqLog
cqLog()

cqapi = cqHttpApi()
bot = cqapi.create_bot()

# 导入内置插件 test
bot.plugin_load(["pycqBot.plugin.test"])

bot.start()
```

#### bilibili

实现 bilibili 监听动态/直播 消息 自动解析 bilibili qq 小程序分享信息

#### pixiv

实现 pixiv 搜图/pid/用户

#### twitter

实现 twitter 监听推文

#### weather

实现天气查询

#### test

测试插件