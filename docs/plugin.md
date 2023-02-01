## 什么是插件(plugin)？为什么要使用插件？

插件可以让我们在不修改 bot 的代码时为 bot 添加功能，也可以使用别人的插件在我们的 bot 上添加功能

使用插件代码也会更清晰，功能分开的更清楚，功能移植更简单


## 如何加载一个插件？

插件使用十分简单直接使用 bot 实例的 `plugin_load` 加载

如果是第三方插件，首先在主入口文件目录创建一个名为 `plugin` 的目录放进去后把插件名加进 `plugin_load`

```python
# main.py
from pycqBot.cqApi import cqHttpApi, cqLog
cqLog()

cqapi = cqHttpApi()
bot = cqapi.create_bot()

# 导入内置插件 test
bot.plugin_load(["pycqBot.plugin.test"])

"""
多个插件
bot.plugin_load([
    "pycqBot.plugin.test",
    "myPlugin",
    "botplugin"
    ···
])
"""

bot.start()
```

> [!tip]
> 插件可以动态加载( 运行 bot 时通过自定义事件 / 自定义指令中使用 plugin_load 等等)，但是目前不能动态禁用


## 如何配置一个插件？

插件配置很简单在 bot 主入口文件目录创建一个名为 `plugin_config.yml` 的文件

插件配置格式和 go-cphttp 统一使用 yaml 不了解的可以看他的视频[yaml文件语法 (b站 BV17U4y1w79Z)](https://www.bilibili.com/video/BV17U4y1w79Z)，我觉得讲的可以

在 `plugin_config.yml` 中创建一个与插件同名的对象

```yaml
# 这里是随便写的根据你的情况改
blhx:
```

然后在插件同名的对象下添加键值对就行, 比如这里是 blhx 在下面写就是在添加 blhx 插件配置

```yaml
# 这里是随便写的根据你的情况改
blhx:
    # 根据你的情况改
    text: "我超, 不是吧"
    # 多个值 根据你的情况改
    list_test:
    - 233
    - 2333
    - 23333
```
## 如何编写(制作)一个插件？

很简单首先在主入口文件目录创建一个名为 `plugin` 的目录，有的话就不用创建

在 `plugin` 目录下创建一个目录, 在新目录下创建一个 py 文件，新目录/文件名字很重要这是我们插件加载时要保持一致的，也就是插件名， 注意新目录要于文件名一致

然后在刚刚创建的文件中创建一个类，类名要与文件名一致

这里我创建一个 myPlugin 文件，所以我的类名也是要和文件名一致，也就是要创建一个 myPlugin 类

```python
class myPlugin:
    pass
```

这样就是一个插件类但是目前 pycqBot 不会认为这是一个插件因为我们没有说明它是一个插件

如何说明它是一个插件？ 继承 `pycqBot.object.Plugin` 就行

```python
from pycqBot.object import Plugin

class myPlugin(Plugin):
    pass
```

插件在被加载时会被给予三个参数

> `bot` 当前 bot 实例
>
> `cqapi` 当前 bot 实例使用的 cqapi 实例
>
> `plugin_config` 插件配置 (在`plugin_config.yml` 下同名对象的内容)

所以一个插件的最基本写法为如下，不这样写你的插件不会被加载

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message

class myPlugin(Plugin):
    # : xxx 是为了让你的IDE有语法提示
    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)
```

: xxx 是为了让你的IDE有语法提示，不需要可以简化为

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.object import Plugin

class myPlugin(Plugin):
    # : xxx 是为了让你的IDE有语法提示
    def __init__(self, bot, cqapi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)
```

然后把插件名加进 `plugin_load` 就行，不过目前这个插件没有实现任何功能
只会在 bot 启动时提醒加载了该插件

## 如何编写(制作)插件，来为我们的 bot 添加功能？

聪明的小伙伴们看到插件在被加载时会被给予的前两个参数 `bot` `cqapi` 就知道该怎么写了

众所周知 `__init__`  会在类被实例化时调用，而 pycqBot 会进行插件的实例化

所以我们在 `__init__` 中用 `bot` `cqapi` 就可以像之前一样添加指令和使用 cqapi 了

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        # 添加 test 指令
        bot.command(self.test_plugin, "test", {
            "type": "all"
        })

        """

        self 中也有 bot 与 cqapi

        self.bot.command(self.test_plugin, "test", {
            "type": "all"
        })

        """
    
    def test_plugin(self, cdata, message: Message):
        message.reply("这里是 myPlugin 中的 test!")
```

## 如何编写插件事件？

看到这里小伙伴们可能会说 “什么啊，没法加事件还是要修改 bot 代码添加事件”

当然可以在插件中编写事件啦，在插件中编写事件不用继承 `cqBot`，可以直接编写

如，在插件中实现防撤回

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        bot.command(self.test_plugin, "test", {
            "type": "all"
        })

    def test_plugin(self, cdata, message: Message):
        message.reply("这里是 myPlugin 中的 test!")
    
    # notice_group_recall (消息被撤回) 事件
    # 事件的 message 和指令的 message 不一样， 事件的 message 是 json 数据
    def notice_group_recall(self, message):
        # 获取被撤回的消息
        message = self.cqapi.get_msg(message["message_id"])["data"]
        # 重新发送被撤回的消息
        self.cqapi.send_group_msg(message, "有一条消息无了 群友还没看清楚呢！ %s：%s" % (
                message["sender"]["nickname"],
                message["message"]
            )
        )
```
> [!tip]
> 插件事件并非重写了 bot 事件，而是在 bot 运行过这个事件后把插件中同名的全部运行一次

## 如何使用插件配置？

这里就要用到 `plugin_config` 了

比如我在 `plugin_config.yml` 中的 myPlugin 对象添加了这个 text 配置

```yaml
# plugin_config.yml

myPlugin:
    text: "这里是 plugin_config.yml 中的 myPlugin 配置 test!"
```

怎么获取这个 `text` 呢？ 很简单，在 `plugin_config.yml` 中的 text 在插件 `plugin_config` 中就是 text

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        bot.command(self.test_plugin, "test", {
            "type": "all"
        })

        # 获取这个 `text`
        self.text = plugin_config["text"]

    def test_plugin(self, cdata, message: Message):
        message.reply(self.text)
```

如果是多个值，在插件中就是数组

```yaml
# plugin_config.yml

myPlugin:
    list: 
        - 233
        - 2333
        - 2333
```

```python
# plugin/myPlugin/myPlugin.py
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.object import Plugin, Message


class myPlugin(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)

        bot.command(self.test_plugin, "test", {
            "type": "all"
        })

        # 获取这个 `list`
        self.list = plugin_config["list"]

    def test_plugin(self, cdata, message: Message):
        list_len = len(self.list)
        message.reply("这里是 plugin_config.yml 中的 myPlugin 配置 list！有 %s 值！！！" % list_len)
```