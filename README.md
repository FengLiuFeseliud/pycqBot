# pycqBot

go-cqhttp python 框架，可以用于快速塔建 bot

![issues](https://img.shields.io/github/issues/FengLiuFeseliud/pycqBot)![forks](https://img.shields.io/github/forks/FengLiuFeseliud/pycqBot)![stars](https://img.shields.io/github/stars/FengLiuFeseliud/pycqBot)![license](https://img.shields.io/github/license/FengLiuFeseliud/pycqBot)

**项目文档不更新的话 请刷新浏览器缓存**

[项目文档 (移动至 Github Pages): https://fengliufeseliud.github.io/pycqBot/](https://fengliufeseliud.github.io/pycqBot/)

[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## 支持 PyPy

可以使用 PyPy3 进行性能提升

```bash
pypy3 -m pip install pycqBot
# 改用 PyPy 运行
pypy3 ./main.py
```

## 演示

### 创建指令

```python
from pycqBot import cqHttpApi, cqBot, cqLog
from pycqBot.data import *

cqLog()

def test(command_data, message: Message):
    message.reply("你好!")
 
bot = cqHttpApi().create_bot()
# 创建指令 "#test"
bot.command(test, "test")

bot.start()
```

### cqCode

```python
from pycqBot.cqCode import image, get_cq_code


cq_code = image("https://i.pixiv.cat/img-master/img/2020/03/25/00/00/08/80334602_p0_master1200.jpg")
# 字典 与 cqCode 互转
print(cq_code, "\n\n", get_cq_code(cq_code))
```

### 事件处理

```python
from pycqBot import cqHttpApi, cqBot, cqLog
from pycqBot.data import *


cqLog()

class myCqBot(cqBot):
    
    # 防撤回
    def notice_group_recall(self, event: Notice_Event):
        message = self.cqapi.get_msg(event.data["message_id"])["data"]
        self.cqapi.send_group_msg(message["group_id"], "有一条消息无了 群友还没看清楚呢！ %s：%s" % ( 
            message["sender"]["nickname"],
            message["message"]
        ))

bot = myCqBot(cqHttpApi()).start()
```
