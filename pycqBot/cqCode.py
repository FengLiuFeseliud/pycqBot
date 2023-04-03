from typing import Any, Union
from time import time
import json


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
    for key in code["data"].keys():
        data_str += ",%s=%s" % (key, code["data"][key])
    
    cqCode = "[CQ:%s%s]" % (code["type"], data_str)
    return cqCode

def get_cq_code(code_str: str) -> dict[str, Union[str, dict[str, Any]]]:
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

def cqJsonStrToDict(cq_json_str: str) -> dict[str, Any]:
    """
    转换 cqCode 中的 json 字符串为字典
    """
    cq_json_str = cq_json_str.replace("&#44;", ",")
    cq_json_str = cq_json_str.replace("&amp;", "&")
    cq_json_str = cq_json_str.replace("&#91;", "[")
    cq_json_str = cq_json_str.replace("&#93;", "]")

    return json.loads(cq_json_str)

def DictTocqJsonStr(dict: dict[str, Any]) -> str:
    """
    转换字典为 cqCode 中的 json 字符串
    """
    cq_json_str = json.dumps(dict, separators=(',', ':'),ensure_ascii=False)
    cq_json_str = cq_json_str.replace("&", "&amp;")
    cq_json_str = cq_json_str.replace(",", "&#44;")
    cq_json_str = cq_json_str.replace("[", "&#91;")
    cq_json_str = cq_json_str.replace("]", "&#93;")
    cq_json_str = cq_json_str.replace("'", '"')

    return cq_json_str

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

def node_list(message_list: list[str], name: str, uin: int) -> str:
    """
    合并转发列表生成
    """
    node_list_data = []
    for message in message_list:
        node_list_data.append(node(message, name, uin))
    
    return json.dumps(node_list_data, separators=(',', ':'))

def face(face_id: int) -> str:
    """
    QQ 表情
    QQ 表情 ID 表: https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
    """

    return set_cq_code({
        "type": "face",
        "data": {
            "id": face_id
        }
    })


def record(file: str, magic: int=0, cache: int=1, proxy: int=1) -> str:
    """
    发语音
    """

    return set_cq_code({
        "type": "record",
        "data": {
            "file": file,
            "magic": magic,
            "cache": cache,
            "proxy": proxy,
        }
    })


def video(file: str) -> str:
    """
    短视频
    """

    return set_cq_code({
        "type": "video",
        "data": {
            "file": file,
        }
    })


def at(qq: int, name: str="") -> str:
    """
    @某人
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
    猜拳魔法表情
    """

    return set_cq_code({
        "type": "rps",
        "data": {}
    })


def dice() -> str:
    """
    掷骰子魔法表情
    """

    return set_cq_code({
        "type": "dice",
        "data": {}
    })


def shake() -> str:
    """
    窗口抖动（戳一戳）
    """

    return set_cq_code({
        "type": "shake",
        "data": {}
    })


def anonymous() -> str:
    """
    匿名发消息
    """

    return set_cq_code({
        "type": "anonymous",
        "data": {}
    })


def share(url: str, title: str, content: str="", image: str="") -> str:
    """
    链接分享
    """

    cq_code: dict[str, Any] = {
        "type": "share",
        "data": {
            "url": url,
            "title": title
        }
    }

    if content != "":
        cq_code["data"]["content"] = content
    
    if image != "":
        cq_code["data"]["image"] = image

    return set_cq_code(cq_code)


def contact(type: str, contact_id: int) -> str:
    """
    推荐好友/群
    """

    return set_cq_code({
        "type": "contact",
        "type": {
            "type": type,
            "id": contact_id
        }
    })


def location(lat: float, lon: float, title: str="", content: str="") -> str:
    """
    位置
    """

    cq_code: dict[str, Any] = {
        "type": "location",
        "data": {
            "lat": lat,
            "lon": lon
        }
    }

    if content != "":
        cq_code["data"]["content"] = content
    
    if title != "":
        cq_code["data"]["title"] = title

    return set_cq_code(cq_code)


def music(type: str, id: int) -> str:
    """
    音乐分享
    """

    return set_cq_code({
        "type": "music",
        "data": {
            "type": type,
            "id": id
        }
    })


def music_my(url: str, audio: str, title: str, content: str="", image: str="") -> str:
    """
    音乐自定义分享
    """

    cq_code: dict[str, Any] = {
        "type": "music",
        "data": {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title
        }
    }

    if content != "":
        cq_code["data"]["content"] = content
    
    if image != "":
        cq_code["data"]["image"] = image

    return set_cq_code(cq_code)


def image(file: str, url: str="", type: str="", cache: int=1, show_id: str="") -> str:
    """
    图片
    """

    cq_code: dict[str, Any] = {
        "type": "image",
        "data":{
            "file": file,
            "cache": cache
        }
    }

    if url != "":
        cq_code["data"]["url"] = url

    if type != "":
        cq_code["data"]["type"] = type
    
    if show_id != "":
        cq_code["data"]["id"] = show_id

    return set_cq_code(cq_code)


def node(message: str, name: str, uin: int) -> dict[str, Union[str, dict[str, Any]]]:
    """
    合并转发消息节点

    特殊 cqCode 不返回字符串 返回 node 字典
    """

    return {
        "type":"node",
        "data": {
            "content": message,
            "name": name,
            "uin": uin
        }
    }

def reply(msg_id: int, text: str="", seq: str="", qq: Union[int, str]="") -> str:
    """
    回复
    """

    cq_code: dict[str, Any] = {
        "type": "reply",
        "data":{
            "id": msg_id
        }
    }

    if text != "":
        cq_code["data"]["text"] = msg_id
        cq_code["data"]["qq"] = qq
        cq_code["data"]["seq"] = seq
        cq_code["data"]["time"] = int(time())

    return set_cq_code(cq_code)


def redbag(title: str) -> str:
    """
    红包
    """

    return set_cq_code({
        "type":"redbag",
        "data":{
            "title":title
        }
    })


def poke(qq: int) -> str:
    """
    戳一戳
    """

    return set_cq_code({
        "type": "poke",
        "data":{
            "qq": qq
        }
    })