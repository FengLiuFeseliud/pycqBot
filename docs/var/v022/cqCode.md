有绝大部分的 go-cqhttp cqCode 同名函数，大部分参数一致

因此你可以直接参考 go-cqhttp cqCode 文档来使用 cqCode

> [!note]
>
> go-cqhttp cqCode 文档地址
>
> [https://docs.go-cqhttp.org/cqcode](https://docs.go-cqhttp.org/cqcode)

## 内置处理函数

pycqBot 内置的函数可以帮助你简单的解析出 cqCode

也可以帮助你快速发送 cqCode

**解析 cqCode**

```python
from pycqBot.cqCode import strToCqCodeToDict

# 提取字符串中的所有 cqCode 字符串转换为字典列表
print(strToCqCodeToDict("[CQ:at,qq=xxxxxx] [CQ:image,file=testcqcode,type=1]"))
```

**设置 cqCode**

```python
# 引入 cqCode
from pycqBot.cqCode import at, image

cqapi = cqHttpApi()

def at_user(commandData, _, __, from_id):
    # at
    cqapi.send_group_msg(from_id, at(commandData[0]))

def show(commandData, _, __, from_id):
    # image
    cqapi.send_group_msg(from_id, image(
            "test.png",
            "https://img.sakuratools.top/bg.png@0x0x0x80"
        )
    )

cqBot(cqapi,
    group_id_list=[
        "QQ 群号"
    ],
    command={
        "at":{
            "function": at_user,
            "help": [
                "#at - at 指定 qq 号"
            ]
        },
        "show":{
            "function": show,
            "help": [
                "#show - 显示我的网站背景"
            ]
        },
    },
    options={
        "commandSign": "#",
    },
)

input()
# 成功启动可以用 #at+空格+qq号 来 at 人
# 也可以用 #show 显示一张图片
```

### strToCqCodeToDict

提取字符串中的所有 cqCode 字符串转换为字典列表

> **`message`** 当前字符串

返回一个包括一个或多个 cqCode 字典的列表

### get_cq_code

转换 cqCode 字符串为字典

> **`code`** cqCode 字符串

返回一个 cqCode 字典

### strToCqCode

提取字符串中的所有 cqCode 字符串

> **`message`** 当前字符串

返回一个包括一个或多个 cqCode 字符串的列表

### cqJsonStrToDict

转换 cqCode 中的 json 字符串为字典

cqJsonStrToDict 会自动字符替换并解析 json 字符串

> **`cq_json_str`** cqCode 字典中的 json 字符串

> [!attention]
>
> cqCode 中的 json 字符串不进行字符替换无法正常解析

### DictTocqJsonStr

转换字典为 cqCode 中的 json 字符串

DictTocqJsonStr 会转换字典为 json 字符串，并自动字符替换

> **`dict`** 字典数据

> [!attention]
>
> json 字符串不进行字符替换无法正常解析

### DictToCqCode

转换字典为 cqCode json类型

DictToCqCode 会转换字典为 json 字符串并生成 cqCode

> **`dict`** 字典数据

### set_cq_code

转换 pycqBot 的 cqCode 字典为 cqCode 字符串

> **`code`** pycqBot 转换的出 cqCode 字典 (如 strToCqCodeToDict)