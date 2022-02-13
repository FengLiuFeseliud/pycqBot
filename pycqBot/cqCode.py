from time import time


def set_cq_code(code):
    data_str = ""
    for key in code["data"].keys():
        data_str += ",%s=%s" % (key, code["data"][key])
    
    cqCode = "[CQ:%s%s]" % (code["type"], data_str)
    return cqCode


def get_cq_code(code_str):
    code_str = code_str.lstrip("[CQ:").rsplit("]")
    code_list = code_str.split(",")

    cq_code = {
        "type": code_list[0],
        "data":{

        }
    }

    if len(code_list) == 1:
        return cq_code

    for code_data in code_list[1:]:
        key, data = code_data.split("=")
        cq_code["data"][key] = data
    
    return cq_code


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


def image(file, url, type="", cache=1, show_id=""):
    """
    图片
    """

    cq_code = {
        "type": "image",
        "data":{
            "file": file,
            "type": type,
            "url": url,
            "cache": cache
        }
    }


    if type != "":
        cq_code["data"]["type"] = type
    
    if show_id != "":
        cq_code["data"]["id"] = show_id

    return set_cq_code(cq_code)


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