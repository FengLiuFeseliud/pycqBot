import logging
import random
from lxml import etree
from pycqBot.cqApi import cqBot, cqHttpApi
from pycqBot.cqCode import image, node_list
from pycqBot.object import Plugin, Message


class pixiv(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)
        self._forward_qq = plugin_config["forward_qq"]
        self._forward_name = plugin_config["forward_name"]
        self._following_count = 0
        self._max_rlen = plugin_config["max_rlen"] if "max_rlen" in plugin_config else 10
        self._max_pid_len = plugin_config["max_pid_len"] if "max_pid_len" in plugin_config else 20
        self._proxy= "http://%s" % plugin_config["proxy"]
        self.user_id = plugin_config["cookie"].split("PHPSESSID=")[-1].split("_", maxsplit=1)[0]
        self._headers = [
            "referer=https://www.pixiv.net/",
            "cookie=%s" % plugin_config["cookie"]
        ]

        self._pyheaders = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "cookie": plugin_config["cookie"]
        }

        self.command_load()
    
    def command_load(self):
        self.bot.command(self.search_image_random, "搜索用户", {
                "help": [
                    "#搜索用户 - 从指定用户返回指定量图",
                    "   格式: #搜索用户 [用户名] [指定量]"
                ]
            }
        )

        self.bot.command(self.search_user_image_random, "搜索作品", {
                "help": [
                    "#搜索作品 - 从指定标签返回指定量图",
                    "   格式: #搜索作品 [标签] [指定量]"
                ]
            }
        )

        self.bot.command(self.search_following_image_random, "图来", {
            "help": [
                "#图来 - 从本 bot pixiv 关注画师返回随机5张图",
                "这个质量可控，跟着 bot xp 随机",
                "   格式: #图来"
            ]
        })

        self.bot.command(self.search_pid, "pid", {
                "help": [
                    "#pid - 从指定 pid 返回图",
                    "   格式: #pid [pid]"
                ]
            }
        )

    def _json_data_check(self, data):
        if data["error"]:
            self.pixivApiError(data)
            return False
        
        return data
    
    def search_image_random_message(self, image_data, img_code):
        return "标题：%s\n画师：%s\n%s\n%s" % (
            image_data["title"],
            image_data["userName"],
            "https://www.pixiv.net/artworks/%s" % image_data["id"],
            img_code
        )
    
    def search_user_random_message(self, image_data, img_code):
        return img_code
    
    def search_pid_message(self, image_data, img_code):
        return img_code
    
    def _ck_send_type(self, image_data, img_code, send_type):
        if send_type == 1:
            return self.search_image_random_message(image_data, img_code)
        
        if send_type == 2:
            return self.search_user_random_message(image_data, img_code)
        
        if send_type == 3:
            return self.search_pid_message(image_data, img_code)
    
    async def _send_image_list(self, image_list, message, send_type):
        """
        转发图片表
        """
        message_list = []
        for image_url in image_list:
            cache_file = await self.cqapi._cqhttp_download_file(image_url[1], self._headers)
            message_list.append(self._ck_send_type(
                    image_url[0], 
                    image("file://%s" % cache_file),
                    send_type
                )
            )

        self.cqapi.send_group_forward_msg(message.group_id, node_list(message_list, 
            self._forward_name,
            self._forward_qq
        ))
    
    async def _get_following(self, offset):
        api = "https://www.pixiv.net/ajax/user/%s/following?offset=%s&limit=24&rest=show&tag=&lang=zh" % (
            self.user_id,
            offset
        )
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._pyheaders))

    async def _search_image(self, search_data, page):
        api = "https://www.pixiv.net/ajax/search/artworks/%s?word=%s&order=date_d&mode=all&p=%s&s_mode=s_tag_full&type=all&lang=zh" % (
            search_data,
            search_data,
            page
        )
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._pyheaders))
    
    async def _user_image_id(self, user_id):
        api = "https://www.pixiv.net/ajax/user/%s/profile/all?lang=zh" % (
            user_id
        )
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._pyheaders))
    
    async def _get_image(self, img_id, message):
        """
        获取图片数据
        """
        try:
            data = await self.cqapi.link("https://www.pixiv.net/ajax/illust/%s/pages?lang=zh" % img_id, proxy=self._proxy, headers=self._pyheaders)
            self._json_data_check(data)
            if data["error"]:
                self.notImage(img_id, data["message"], message)
                return False
            
            return data["body"]
        except Exception as err:
            self.getImageError(img_id, err)
            return False

    
    async def _get_user(self, user_name, nick=False):
        """
        获取用户
        """
        try:
            # 完全匹配 (nick 啥意思啊?)
            if nick:
                nick = ""
            else:
                nick = "&nick_mf=1"

            html_text = await self.cqapi.link("https://www.pixiv.net/search_user.php?s_mode=s_usr&nick=%s%s" % (user_name, nick), json=False, proxy=self._proxy, headers=self._pyheaders)

            html = etree.HTML(html_text)
            user_item = html.xpath('//li[@class="user-recommendation-item"]')
            if len(user_item) == 0:
                return False
            
            user_item = user_item[0]
            user_id = user_item.xpath('./a/@href')[0].split("/")[-1]
            user_count = user_item.xpath('./dl[@class="meta inline-list"]/dd//text()')
            user_caption = user_item.xpath('./p[@class="caption"]//text()')
            
            user_item = {
                "user_name": user_name,
                "user_id": user_id,
                "user_count": user_count,
                "user_caption": user_caption
            }

        except Exception as err:
            self.getUserError(user_name, nick, err)
            return False

        return user_item
    
    async def _random_image(self, image_list, rlen, message):
        random_image_list = []
        img_id_list = []
        # 随机原图
        for _ in range(0, int(rlen)):
            while True:
                img_data = random.choice(image_list)

                if img_data in img_id_list:
                    continue

                if "id" in img_data:
                    img_id_list.append(img_data["id"])
                else:
                    img_id_list.append(img_data)

                break

            img_url = await self._get_image(img_id_list[-1], message)
            if not img_url:
                continue
                
            random_image_list.append([img_data, img_url[0]["urls"]["original"]])
        
        return random_image_list
    
    async def _search_image_random(self, search_data, rlen, message):
        """
        随机搜索
        """
            
        try:
            if int(rlen) > self._max_rlen:
                self.maxRlen(rlen, message)
                rlen = self._max_rlen

            # 获取数据量
            data = await self._search_image(search_data, 1)
            if not data:
                return
            
            count = data["body"]["illustManga"]["total"]
            if count == 0:
                self.none_search_image(search_data, rlen, message)
                return 
            
            page = int(count / 60)
            if page > 1:
                random_page = random.randint(1, page)
            else:
                random_page = 1

            # 获取页数据
            data = await self._search_image(search_data, random_page)
            image_list = data["body"]["illustManga"]["data"]

            if len(image_list) < int(rlen):
                rlen = len(image_list)
                self.insufficient_search_image(search_data, rlen, message)
            
            await self._send_image_list(await self._random_image(image_list, rlen, message), message, 1)
        except Exception as err:
            self.randomSearchImageError(search_data, rlen, err)
            return False
    
    async def _user_image_random(self, user_id, rlen, message):
        user_image_id_list = await self._user_image_id(user_id)
        user_image_id_list = list(user_image_id_list["body"]["illusts"].keys())

        await self._send_image_list(await self._random_image(user_image_id_list, rlen, message), message, 2)
    
    async def _search_user_image_random(self, user_name, rlen, message, nick=False):
        """
        随机用户作品
        """

        try:
            if int(rlen) > self._max_rlen:
                self.maxRlen(rlen, message)
                rlen = self._max_rlen

            # 获取用户作品 id
            user_item = await self._get_user(user_name, nick)
            if not user_item:
                self.searchNotUser(user_name, rlen, nick, message)
                return False
            
            await self._user_image_random(user_item["user_id"], rlen, message)
        except Exception as err:
            self.randomSearchUserImageError(user_name, rlen, nick, err)
            return False
    
    async def _search_pid(self, pid, message):
        try:
            img_data = await self._get_image(pid, message)
            if not img_data:
                return False
            
            if len(img_data) > self._max_pid_len:
                self.maxPidLen(len(img_data), message)
                img_data = img_data[0: self._max_pid_len]

            send_img = []
            for img in img_data:
                send_img.append([pid, img["urls"]["original"]])
                
            await self._send_image_list(send_img, message, 3)
        except Exception as err:
            self.searchPidError(pid, err)
            return False
    
    async def _search_following_image_random(self, rlen, message):
        try:
            offset = 0
            if self._following_count != 0:
                random_page = random.randint(1, int(self._following_count / 24))
                if random_page != 1:
                    offset = random_page * 24

            following_data = await self._get_following(offset)
            if following_data["error"]:
                self.getFollowingError(following_data["message"])
                return False

            self._following_count = following_data["body"]["total"]
            following_user = random.choice(following_data["body"]["users"])

            await self._user_image_random(following_user["userId"], rlen, message)
        except Exception as err:
            self.randomSearchFollowingImageError(err)
            return False
    
    def search_image_random(self, commandData, message: Message):
        """
        搜索标签随机图
        """
        self.cqapi.add_task(self._search_image_random(commandData[0], commandData[1], message))
    
    def search_user_image_random(self, commandData, message: Message):
        """
        搜索用户随机图
        """
        nick = False
        if len(commandData) == 3:
            if commandData[2] == "模糊":
                nick = True
        self.cqapi.add_task(self._search_user_image_random(commandData[0], commandData[1], message, nick))
    
    def search_pid(self, commandData, message: Message):
        """
        搜索pid
        """
        self.cqapi.add_task(self._search_pid(commandData[0], message))
    
    def search_following_image_random(self, commandData, message: Message):
        """
        搜索关注用户随机图
        """
        self.cqapi.add_task(self._search_following_image_random(5, message))
    
    def none_search_image(self, search_data, rlen, message):
        """
        没有搜索到数据
        """
        message.reply("%s 没有搜索到数据..." % search_data)
    
    def insufficient_search_image(self, search_data, rlen, message):
        """
        数据量不足于指定量
        """
        message.reply("%s 数据量不足于指定量，将全部返回%s张" % (search_data, rlen))
    
    def notImage(self, img_id, err_msg, message):
        """
        没有搜索到 pid
        """
        message.reply("无法获得到 %s，%s" % (img_id, err_msg))
    
    def searchNotUser(self, user_name, rlen, nick, message):
        """
        没有搜索到用户
        """
        message.reply("没有 %s 的用户" % user_name)
    
    def maxRlen(self, rlen, message):
        """
        指定量超出最大值
        """
        message.reply("指定量 %s 超出最大值 %s，将返回最大值" % (rlen, self._max_rlen))
    
    def maxPidLen(self, rlen, message):
        """
        指定量超出PID获取最大值 
        """
        message.reply("指定量 %s 超出 PID 获取最大值 %s，将截取" % (rlen, self._max_pid_len))
        
    def randomSearchImageError(self, search_data, rlen, err):
        """
        搜索随机图片时错误
        """
        logging.error("搜索 %s 随机图片时发生错误! Error: %s " % (search_data, err))
        logging.exception(err)
    
    def randomSearchUserImageError(self, user_name, rlen, nick, err):
        """
        随机用户作品时错误
        """
        logging.error("随机 %s 作品时发生错误! Error: %s " % (user_name, err))
        logging.exception(err)
    
    def randomSearchFollowingImageError(self, err):
        """
        随机关注用户作品时发生错误
        """
        logging.error("随机关注用户作品时发生错误! Error: %s " % err)
        logging.exception(err)
    
    def searchPidError(self, pid_list, err):
        """
        搜索PID时发生错误
        """
        logging.error("搜索 PID %s 时发生错误! Error: %s " % (pid_list, err))
        logging.exception(err)
    
    def getImageError(self, img_id, err):
        """
        搜索图片时发生错误
        """
        logging.error("搜索图片 %s 时发生错误! Error: %s " % (img_id, err))
        logging.exception(err)
    
    def getUserError(self, user_name, nick, err):
        """
        搜索用户时发生错误
        """
        logging.error("搜索用户 %s 时发生错误! Error: %s " % (user_name, err))
        logging.exception(err)
    
    def getFollowingError(self, following_data):
        """
        获取关注用户时发生错误
        """
        logging.error("获取关注用户时发生错误! Error: %s " % following_data)

    def pixivApiError(self, err_msg):
        """
        请求 pixiv api 时错误
        """
        logging.error("请求 pixiv api发生错误! Error: %s " % err_msg)