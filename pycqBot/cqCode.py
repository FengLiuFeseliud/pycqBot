from typing import Any, Union, Optional
from time import time
import json as json_data


def strToCqCode(message: str) -> list[str]:
    """
    提取字符串中的 cqCode 字符串
    """
    msg = list(message)
    cq_code = ""
    cq_code_in = False
    cq_code_list = []
    for str in msg:
        if cq_code_in and str != "]":
            cq_code += str
            continue
        
        if cq_code_in and str == "]":
            cq_code += str
            cq_code_list.append(cq_code)
            cq_code = ""
            cq_code_in = False
            continue

        if str == "[":
            cq_code = ""
            cq_code += str
            continue

        if str == "C":
            cq_code += str
            continue

        if str == "Q":
            cq_code += str
            continue

        if str == ":" and cq_code == "[CQ":
            cq_code += str
            cq_code_in = True

    return cq_code_list


def strToCqCodeToDict(message: str) -> list[dict[str, Union[str, dict[str, Any]]]]:
    """
    提取字符串中的 cqCode 字符串转换为字典
    """
    CqCodeList = []
    for item in strToCqCode(message):
        CqCodeList.append(get_cq_code(item))
    
    return CqCodeList


def set_cq_code(code: dict[str, Any]) -> str:
    """
    转换 pycqBot 的 cqCode 字典为 cqCode 字符串
    """
    data_str = ""
    for key, data in code["data"].items():
        if data is None:
            continue

        data_str += ",%s=%s" % (key, data)
    
    cqCode = "[CQ:%s%s]" % (code["type"], data_str)
    return cqCode


def get_cq_code(code_str: str) -> dict:
    """
    转换 cqCode 字符串为字典
    """
    code_str = code_str.lstrip("[CQ:").rsplit("]")[0]
    code_list = code_str.split(",")

    cq_code: dict[str, Any] = {
        "type": code_list[0],
        "data":{

        }
    }

    if len(code_list) == 1:
        return cq_code

    for code_data in code_list[1:]:
        key_data = code_data.split("=")
        if len(key_data) != 2:
            key_data[1] = "=".join(key_data[1:])
        cq_code["data"][key_data[0]] = key_data[1]

    if cq_code["type"] == "json":
        cq_code["data"]["data"] = cqJsonStrToDict(cq_code["data"]["data"])
    
    return cq_code


def e_code(data: str):
    data = data.replace("&", "&amp;")
    data = data.replace(",", "&#44;")
    data = data.replace("[", "&#91;")
    data = data.replace("]", "&#93;")
    return data


def d_code(data: str):
    data = data.replace("&#44;", ",")
    data = data.replace("&amp;", "&")
    data = data.replace("&#91;", "[")
    data = data.replace("&#93;", "]")
    return data


def cqJsonStrToDict(cq_json_str: str) -> dict[str, Any]:
    """
    转换 cqCode 中的 json 字符串为字典
    """
    return json_data.loads(d_code(cq_json_str))


def DictTocqJsonStr(dict: dict[str, Any]) -> str:
    """
    转换字典为 cqCode 中的 json 字符串
    """
    return e_code(json_data.dumps(dict, separators=(',', ':'),ensure_ascii=False)).replace("'", '"')


def DictToCqCode(dict: dict) -> str:
    """
    转换字典为 cqCode json
    """
    return set_cq_code({
        "type": "json",
        "data": {
            "data": DictTocqJsonStr(dict)
        }
    })


"""
go-cqhttp v1.0.0 cqCode

https://docs.go-cqhttp.org/cqcode/
"""


def node_list(message_list: list[str], name: str, uin: int) -> str:
    """
    合并转发列表生成
    """
    node_list_data = []
    for message in message_list:
        node_list_data.append(node(content=message, name=name, uin=uin))
    
    return json_data.dumps(node_list_data, separators=(',', ':'), ensure_ascii=False)


def face(
    id: int
) -> str:
    """
    QQ 表情
    
    QQ 表情 ID 见:
    https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8

    Args:
        `id`: QQ 表情 ID

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85
    """
    return set_cq_code({
        "type": "face",
        "data": {
            "id": id
        }
    })


def record(
    file: str, 
    magic: int = 0, 
    cache: int = 1, 
    proxy: int = 1,
    timeout: int = 0
) -> str:
    """
    发语音

    Args:
        `file`: 语音文件名
        `magic`: 发送时可选, 默认 `0`, 设置为 `1` 表示变声
        `cache`: 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 `1`
        `proxy`: 只在通过网络 URL 发送时有效, 表示是否通过代理下载文件 ( 需通过环境变量或配置文件配置代理 ) , 默认 `1`
        `timeout`: 只在通过网络 URL 发送时有效, 单位秒, 表示下载网络文件的超时时间, 默认不超时

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E8%AF%AD%E9%9F%B3
    """
    return set_cq_code({
        "type": "record",
        "data": {
            "file": file,
            "magic": magic,
            "cache": cache,
            "proxy": proxy,
            "timeout": timeout
        }
    })


def video(
    file: str,
    cover: Optional[str] = None,
    c: Optional[int] = None
) -> str:
    """
    短视频

    Args:
        `file`: 视频地址, 支持 http 和 file 发送
        `cover`: 视频封面, 支持 http, file 和 base64 发送, 格式必须为 jpg
        `c`: 通过网络下载视频时的线程数, 默认单线程. (在资源不支持并发时会自动处理)

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E7%9F%AD%E8%A7%86%E9%A2%91
    """
    return set_cq_code({
        "type": "video",
        "data": {
            "file": file,
            "cover": cover,
            "c": c
        }
    })


def at(
    qq: Union[int, str], 
    name: Optional[str] = None
) -> str:
    """
    @某人

    Args:
        `qq`: @的 QQ 号, `all` 表示全体成员
        `name`: 当在群中找不到此QQ号的名称时才会生效

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E6%9F%90%E4%BA%BA
    """
    return set_cq_code({
        "type": "at",
        "data": {
            "qq": qq,
            "name": name
        }
    })


def rps() -> str:
    """
    猜拳魔法表情 (该 cqCode 暂未被 go-cqhttp 支持)

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E7%8C%9C%E6%8B%B3%E9%AD%94%E6%B3%95%E8%A1%A8%E6%83%85
    """
    return set_cq_code({
        "type": "rps",
        "data": {}
    })


def dice() -> str:
    """
    掷骰子魔法表情 (该 cqCode 暂未被 go-cqhttp 支持)

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E6%8E%B7%E9%AA%B0%E5%AD%90%E9%AD%94%E6%B3%95%E8%A1%A8%E6%83%85
    """
    return set_cq_code({
        "type": "dice",
        "data": {}
    })


def shake() -> str:
    """
    窗口抖动（戳一戳）(该 cqCode 暂未被 go-cqhttp 支持)

    相当于戳一戳最基本类型的快捷方式

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E7%AA%97%E5%8F%A3%E6%8A%96%E5%8A%A8-%E6%88%B3%E4%B8%80%E6%88%B3
    """
    return set_cq_code({
        "type": "shake",
        "data": {}
    })


def anonymous() -> str:
    """
    匿名发消息 (该 cqCode 暂未被 go-cqhttp 支持)

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E5%8C%BF%E5%90%8D%E5%8F%91%E6%B6%88%E6%81%AF
    """
    return set_cq_code({
        "type": "anonymous",
        "data": {}
    })


def share(
    url: str, 
    title: str, 
    content: Optional[str] = None, 
    image: Optional[str] = None
) -> str:
    """
    链接分享

    Args:
        `url`: URL
        `title`: 标题
        `content`: 发送时可选, 内容描述
        `image`: 发送时可选, 图片 URL

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E9%93%BE%E6%8E%A5%E5%88%86%E4%BA%AB
    """
    return set_cq_code({
        "type": "share",
        "data": {
            "url": url,
            "title": title,
            "content": content,
            "image": image
        }
    })


def contact(
    type: str, 
    contact_id: int
) -> str:
    """
    推荐好友/群 (该 cqCode 暂未被 go-cqhttp 支持)

    Args:
        `type`: 推荐好友/群
        `contact_id`: 被推荐的 QQ （群）号

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E6%8E%A8%E8%8D%90%E5%A5%BD%E5%8F%8B-%E7%BE%A4
    """

    return set_cq_code({
        "type": "contact",
        "type": {
            "type": type,
            "id": contact_id
        }
    })


def location(
    lat: float, 
    lon: float, 
    title: Optional[str] = None, 
    content: Optional[str] = None
) -> str:
    """
    位置 (该 cqCode 暂未被 go-cqhttp 支持)

    Args:
        `lat`: 纬度
        `lon`: 经度
        `title`: 发送时可选, 标题
        `content`: 发送时可选, 内容描述
    
    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E4%BD%8D%E7%BD%AE
    """
    return set_cq_code({
        "type": "location",
        "data": {
            "lat": lat,
            "lon": lon,
            "title": title,
            "content": content
        }
    })


def music(
    type: str, 
    id: int
) -> str:
    """
    音乐分享

    Args:
        `type`: `qq` `163` `xm` 分别表示使用 QQ 音乐、网易云音乐、虾米音乐
        `id`: 歌曲 ID

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E9%9F%B3%E4%B9%90%E5%88%86%E4%BA%AB
    """
    return set_cq_code({
        "type": "music",
        "data": {
            "type": type,
            "id": id
        }
    })


def music_custom(
    url: str, 
    audio: str, 
    title: str, 
    content: Optional[str] = None, 
    image: Optional[str] = None
) -> str:
    """
    音乐自定义分享

    Args:
        `url`: 点击后跳转目标 URL
        `audio`: 音乐 URL
        `title`: 标题
        `content`: 发送时可选, 内容描述
        `image`: 发送时可选, 图片 URL

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E9%9F%B3%E4%B9%90%E8%87%AA%E5%AE%9A%E4%B9%89%E5%88%86%E4%BA%AB
    """
    return set_cq_code({
        "type": "music",
        "data": {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title,
            "content": content,
            "image": image
        }
    })


def image(
    file: str, 
    type: Optional[str] = None, 
    subType: Optional[str] = None, 
    url: Optional[str] = None, 
    cache: Optional[int] =  None, 
    id: Optional[str] = None,
    c: Optional[int] = None
) -> str:
    """
    图片

    Args:
        `file`: 图片文件名
        `type`: 发送时可选, 图片类型, `flash` 表示闪照, `show` 表示秀图, 默认普通图片
        `subType`: 发送时可选, 图片子类型, 只出现在群聊
        `url`: 发送时可选, 图片 URL
        `cache`: 发送时可选, 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 `1`
        `id`: 发送时可选, 发送秀图时的特效id, 默认为 40000
        `c`: 发送时可选, 通过网络下载图片时的线程数, 默认单线程. (在资源不支持并发时会自动处理)

    可用的特效ID

    id:
        `40000`: 普通
        `40001`: 幻影
        `40002`: 抖动
        `40003`: 生日
        `40004`: 爱你
        `40005`: 征友

    子类型列表

    subType:
        `0`: 正常图片
        `1`: 表情包, 在客户端会被分类到表情包图片并缩放显示
        `2`: 热图
        `3`: 斗图
        `4`: 智图?
        `7`: 贴图
        `8`: 自拍
        `9`: 贴图广告?
        `10`: 有待测试
        `13`: 热搜图

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E5%9B%BE%E7%89%87
    """
    return set_cq_code({
        "type": "image",
        "data":{
            "file": file,
            "type": type,
            "subType": subType,
            "url": url,
            "cache": cache,
            "id": id,
            "c": c
        }
    })


def reply(
    id: int, 
    text: Optional[str] = None, 
    qq: Optional[Union[int, str]] = None,
    time: Optional[int] = None,
    seq: Optional[str] = None, 
) -> str:
    """
    回复

    Args:
        `id`: 回复时所引用的消息 id, 必须为本群消息
        `text`: 发送时可选, 自定义回复的信息
        `qq`: 发送时可选, 自定义回复时的自定义QQ, 如果使用自定义信息必须指定
        `time`: 发送时可选, 自定义回复时的时间, 格式为 Unix 时间
        `seq`: 发送时可选, 起始消息序号, 可通过 `get_msg` 获得
    
    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E5%9B%9E%E5%A4%8D
    """
    return set_cq_code({
        "type": "reply",
        "data":{
            "id": id,
            "text": text,
            "qq": qq,
            "time": time,
            "seq": seq
        }
    })

def poke(
    qq: int
) -> str:
    """
    戳一戳

    Args:
        `qq`: 需要戳的成员

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E6%88%B3%E4%B8%80%E6%88%B3
    """
    return set_cq_code({
        "type": "poke",
        "data":{
            "qq": qq
        }
    })


def gift(
    qq: int,
    id: int, 
) -> str:
    """
    礼物

    Args:
        `qq`: 接收礼物的成员
        `id`: 礼物的类型

    目前支持的礼物 ID

    id: 
        `0`: 甜 Wink
        `1`: 快乐肥宅水
        `2`: 幸运手链
        `3`: 卡布奇诺
        `4`: 猫咪手表
        `5`: 绒绒手套
        `6`: 彩虹糖果
        `7`: 坚强
        `8`: 告白话筒
        `9`: 牵你的手
        `10`: 可爱猫咪
        `11`: 神秘面具
        `12`: 我超忙的
        `13`: 爱心口罩

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E7%A4%BC%E7%89%A9
    """
    return set_cq_code({
        "type": "gift",
        "data":{
            "qq": qq,
            "id": id
        }
    })


def node(
    id: Optional[int] = None,
    name: Optional[str] = None,
    uin: Optional[int] = None,
    content: Optional[str] = None, 
    seq: Optional[str] = None
) -> dict[str, Union[str, dict[str, Any]]]:
    """
    合并转发消息节点

    特殊 cqCode 不返回字符串 返回 node 字典
    
    Args:
        `id`: 转发消息id, 直接引用他人的消息合并转发, 实际查看顺序为原消息发送顺序 与下面的自定义消息二选一
        `name`: 发送者显示名字, 用于自定义消息 (自定义消息并合并转发, 实际查看顺序为自定义消息段顺序)
        `uin`: 发送者QQ号, 用于自定义消息
        `content`: 具体消息, 用于自定义消息, 不支持转发套娃
        `seq`: 具体消息, 用于自定义消息
    
    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
    """
    if id is not None and content is not None:
        content = None

    code_data = {
        "type":"node",
        "data": {

        }
    }

    if id is not None:
        code_data["data"]["id"] = id

    if name is not None:
        code_data["data"]["name"] = name

    if uin is not None:
        code_data["data"]["uin"] = uin

    if content is not None:
        code_data["data"]["content"] = content

    if content is not None:
        code_data["data"]["seq"] = seq

    return code_data


def xml(
    data: str,
    resid: Optional[int] = None
) -> str:
    """
    XML 消息

    Args:
        `data`: xml 内容, xml 中的 value 部分 (自动实体化处理)
        `resid`: 可能为空, 或空字符串

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#xml-%E6%B6%88%E6%81%AF
    """
    return set_cq_code({
        "type": "xml",
        "data":{
            "data": e_code(data),
            "resid": resid
        }
    })


def json(
    data: str,
    resid: Optional[int] = None 
) -> str:
    """
    JSON 消息

    Args:
        `data`: json 内容, json 的所有字符串 (自动实体化处理)
        `resid`: 可能为空, 或空字符串

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#json-%E6%B6%88%E6%81%AF
    """
    return set_cq_code({
        "type": "json",
        "data":{
            "data": e_code(data),
            "resid": resid
        }
    })


def cardimage(
    file: str,
    minwidth: Optional[int] = None ,
    minheight: Optional[int] = None ,
    maxwidth: Optional[int] = None ,
    maxheight: Optional[int] = None ,
    source: Optional[int] = None ,
    icon: Optional[int] = None ,
) -> str:
    """
    cardimage 

    一种xml的图片消息（装逼大图）

    Args:
        `file`: 和 image 的 file 字段对齐, 支持也是一样的
        `minwidth`: 默认不填为 400, 最小 width
        `minheight`: 默认不填为 400, 最小 height
        `maxwidth`: 默认不填为 500, 最大 width
        `maxheight`: 默认不填为 1000, 最大 height
        `source`: 分享来源的名称, 可以留空
        `icon`: 分享来源的 icon 图标 url, 可以留空

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#cardimage
    """
    return set_cq_code({
        "type": "cardimage",
        "data":{
            "file": file,
            "minwidth": minwidth,
            "minheight": minheight,
            "maxwidth": maxwidth,
            "maxheight": maxheight,
            "source": source,
            "icon": icon,
        }
    })


def tts(
    text: str
) -> str:
    """
    文本转语音

    Args:
        `text`: 内容

    go-cqhttp 文档:
    https://docs.go-cqhttp.org/cqcode/#%E6%96%87%E6%9C%AC%E8%BD%AC%E8%AF%AD%E9%9F%B3
    """
    return set_cq_code({
        "type": "tts",
        "data":{
            "text": text
        }
    })