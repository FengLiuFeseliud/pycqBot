from time import time
import json


def strToCqCode(message):
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

def strToCqCodeToDict(message):
    """
    提取字符串中的 cqCode 字符串转换为字典
    """
    CqCodeList = strToCqCode(message)
    for count in range(0, len(CqCodeList)):
        CqCodeList[count] = get_cq_code(CqCodeList[count])
    
    return CqCodeList

def set_cq_code(code):
    """
    转换 pycqBot 的 cqCode 字典为 cqCode 字符串
    """
    data_str = ""
    for key in code["data"].keys():
        data_str += ",%s=%s" % (key, code["data"][key])
    
    cqCode = "[CQ:%s%s]" % (code["type"], data_str)
    return cqCode

def get_cq_code(code_str):
    """
    转换 cqCode 字符串为字典
    """
    code_str = code_str.lstrip("[CQ:").rsplit("]")
    code_list = code_str[0].split(",")

    cq_code = {
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

def cqJsonStrToDict(cq_json_str):
    """
    转换 cqCode 中的 json 字符串为字典
    """
    cq_json_str = cq_json_str.replace("&#44;", ",")
    cq_json_str = cq_json_str.replace("&amp;", "&")
    cq_json_str = cq_json_str.replace("&#91;", "[")
    cq_json_str = cq_json_str.replace("&#93;", "]")

    return json.loads(cq_json_str)

def DictTocqJsonStr(dict):
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

def DictToCqCode(dict):
    """
    转换字典为 cqCode json
    """
    return set_cq_code({
        "type": "json",
        "data": {
            "data": DictTocqJsonStr(dict)
        }
    })

def node_list(message_list, name, uin):
    """
    合并转发列表生成
    """
    node_list_data = []
    for message in message_list:
        node_list_data.append(node(message, name, uin))
    
    return json.dumps(node_list_data, separators=(',', ':'))

def face(face_id):
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


def record(file, magic=0, cache=1, proxy=1):
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


def video(file):
    """
    短视频
    """

    return set_cq_code({
        "type": "video",
        "data": {
            "file": "http://baidu.com/1.mp4",
        }
    })


def at(qq, name=""):
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


def rps():
    """
    猜拳魔法表情
    """

    return set_cq_code({
        "type": "rps",
        "data": {}
    })


def dice():
    """
    掷骰子魔法表情
    """

    return set_cq_code({
        "type": "dice",
        "data": {}
    })


def shake():
    """
    窗口抖动（戳一戳）
    """

    return set_cq_code({
        "type": "shake",
        "data": {}
    })


def anonymous():
    """
    匿名发消息
    """

    return set_cq_code({
        "type": "anonymous",
        "data": {}
    })


def share(url, title, content="", image=""):
    """
    链接分享
    """

    cq_code = {
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


def contact(type, contact_id):
    """
    推荐好友/群
    """

    return set_cq_code({
        "type": "contact",
        "type": {
            "url": type,
            "id": contact_id
        }
    })


def location(lat, lon, title="", content=""):
    """
    位置
    """

    cq_code = {
        "type": "location",
        "data": {
            "lat": "39.8969426",
            "lon": "116.3109099"
        }
    }

    if content != "":
        cq_code["data"]["content"] = content
    
    if title != "":
        cq_code["data"]["title"] = title

    return set_cq_code(cq_code)


def music(type, id):
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


def music_my(url, audio, title, content="", image=""):
    """
    音乐自定义分享
    """

    cq_code = {
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


def image(file, url="", type="", cache=1, show_id=""):
    """
    图片
    """

    cq_code = {
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


def node(message, name, uin):
    """
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

def reply(text, seq, msg_id="", qq=""):
    """
    回复
    """

    cq_code = {
        "type": "reply",
        "data":{
            "text": text,
            "seq": seq,
            "time": int(time())
        }
    }


    if msg_id != "":
        cq_code["data"]["msg_id"] = msg_id
    
    if qq != "":
        cq_code["data"]["qq"] = qq

    return set_cq_code(cq_code)


def redbag(title):
    """
    红包
    """

    return set_cq_code({
        "type":"redbag",
        "data":{
            "title":title
        }
    })


def poke(qq):
    """
    戳一戳
    """

    return set_cq_code({
        "type": "poke",
        "data":{
            "qq": qq
        }
    })