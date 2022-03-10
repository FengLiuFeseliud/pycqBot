import logging
import json
from pycqBot.cqCode import image, node_list
from lxml import etree
import requests
import random


class Bilibili:

    def __init__(self, cqapi, monitor_live=[], monitor_dynamic=[]):
        self.cqapi = cqapi
        self._lives_old = []
        self._live_monitor_in = True
        self._monitor_live_uids = monitor_live
        self._dynamic_list_old = {}
        self._dynamic_monitor_in = True
        self._monitor_dynamic_uids = monitor_dynamic
        self._send_msg_list = []

        # 初始化 self._dynamic_list_old
        if self._monitor_dynamic_uids != []:
            for uid in self._monitor_dynamic_uids:
                self._dynamic_list_old[uid] = {
                    "time": 0,
                    "data": {}
                }
            
        self.monitor()
        self.monitor_send_clear()
    
    def _json_data_check(self, json_data):
        if json_data["code"] != 0:
            self.biliApiError(json_data["code"], json_data["message"])
            return False
        
        return json_data

    async def get_lives_status(self, live_list):
        api = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
        post_data = {
            "uids": live_list
        }
        return self._json_data_check(await self.cqapi.link(
                api, 
                mod="post", 
                data=json.dumps(post_data)
            )
        )
    
    async def get_dynamic(self, uid):
        api = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=%s" % uid
        return self._json_data_check(await self.cqapi.link(api))
    
    async def get_cv_viewinfo(self, cvid):
        api = "https://api.bilibili.com/x/article/viewinfo?id=%s" % cvid
        return self._json_data_check(await self.cqapi.link(api))
    
    async def get_cv_list(self, rlid):
        api = "http://api.bilibili.com/x/article/list/web/articles?id=%s" % rlid
        return self._json_data_check(await self.cqapi.link(api))
    
    async def get_video(self, bvid):
        api = "https://api.bilibili.com/x/web-interface/view?bvid=%s" % bvid
        return self._json_data_check(await self.cqapi.link(api))
    
    async def get_root_init(self, rootid):
        api = "http://api.live.bilibili.com/room/v1/Room/room_init?id=%s" % rootid
        return self._json_data_check(await self.cqapi.link(api))

    async def _get_all_url(self, surl):
        surl = surl.split("?")[0]
        url_text = await self.cqapi.link(surl, allow_redirects=False, json=False)
        all_url = url_text.replace('<a href="', "").replace('">Found</a>.', "")
        return surl, all_url

    async def _get_share_video(self, cq_json):
        """
        异步获取QQ小程序分享视频信息
        """
        surl, all_url = await self._get_all_url(cq_json["meta"]["detail_1"]["qqdocurl"])
        bv_id = all_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        bv_json = await self.get_video(bv_id)

        return bv_json["data"], cq_json, surl
    
    async def _get_share_live(self, all_url):
        """
        异步获取QQ小程序分享直播间信息
        """
        root_id = all_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        uid = (await self.get_root_init(root_id))["data"]["uid"]
        live_json = await self.get_lives_status([uid])

        return live_json["data"][str(uid)]
    
    async def _get_share_dynamic(self, all_url):
        """
        异步获取QQ小程序分享动态信息
        """
        dynamic_id = all_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        api = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=%s" % dynamic_id
        dynamic_json = await self.cqapi.link(api, "get")

        dynamic_message = await self._dynamic_check(dynamic_json["data"]["card"])
        return dynamic_message
    
    async def _get_share_cv(self, all_url):
        """
        异步获取QQ小程序分享专栏信息
        """
        cv_id = all_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        api = "https://www.bilibili.com/read/cv%s" % cv_id
        cv_viewinfo_json = await self.get_cv_viewinfo(cv_id)
        # 爬取专栏内容
        html = await self.cqapi.link(api, json=False, mod="get")
        cv_text = self.set_cv_text(html)

        return cv_text, cv_viewinfo_json["data"]
    
    async def _get_share_cv_list(self, all_url):
        """
        异步获取QQ小程序分享文集信息
        """
        rl_id = all_url.split("?")[0].rsplit("/rl", maxsplit=1)[-1]
        cv_list_json = await self.get_cv_list(rl_id)

        return cv_list_json["data"]

    async def _share_type_check(self, cq_code):
        """
        异步判断QQ小程序分享信息类型
        """
        cq_json = cq_code["data"]["data"]
        if cq_json["prompt"] == "[QQ小程序]哔哩哔哩":
            bv_json, cq_json, surl = await self._get_share_video(cq_json)
            return self.set_share_video_message(bv_json, cq_json, surl)
        
        if "detail_1" in cq_json["meta"]:
            return self.set_share_media_message(cq_json)
        
        if "news" not in cq_json["meta"]:
            return False
        
        if "tag" not in cq_json["meta"]["news"]:
            return False

        if cq_json["meta"]["news"]["tag"] == "哔哩哔哩":

            if cq_json["prompt"][0:4] != "[分享]":
                return False
            
            surl, all_url = await self._get_all_url(cq_json["meta"]["news"]["jumpUrl"])
            url_path = all_url.split("?")[0].rsplit("/", maxsplit=1)[0]

            if url_path == "https://m.bilibili.com/dynamic":
                dynamic = await self._get_share_dynamic(all_url)
                return self.set_share_dynamic_message(dynamic, cq_json, surl)

            if url_path == "https://live.bilibili.com":
                liveData = await self._get_share_live(all_url)
                return self.set_share_live_message(liveData, cq_json, surl)
            
            if url_path == "https://www.bilibili.com/read/mobile":
                cv_text, cv_viewinfo_json = await self._get_share_cv(all_url)
                return self.set_share_cv_message(cv_text, cv_viewinfo_json, cq_json, surl)
            
            if url_path == "https://www.bilibili.com/read/readlist":
                cv_list_json = await self._get_share_cv_list(all_url)
                return self.set_share_cv_list_message(cv_list_json, cq_json, surl)
        
        return False
    
    async def _get_link(self, group_id, cq_code):
        """
        异步发送QQ小程序分享信息
        """
        try:
            message = await self._share_type_check(cq_code)
            if message == False:
                return

            self.cqapi.send_group_msg(group_id, message)
            logging.debug("解析到了分享信息 %s" % message)
        except Exception as err:
            self.getShareVideoError(err)
    
    def get_link(self, group_id, cq_code):
        """
        发送QQ小程序分享信息
        """
        self.cqapi.add_task(self._get_link(group_id, cq_code))
    
    def set_cv_text(self, html):
        """
        解析 html 节点获取专栏内容
        """
        cv_text = ""
        html_etree = etree.HTML(html)
        text_list = html_etree.xpath("//div[@id='read-article-holder']//text()")
        for text in text_list:
            if len(text) < 5:
                cv_text.rstrip("\n")
                cv_text += text
                continue

            cv_text += text + "\n"
        
        return cv_text
    
    def set_share_video_message(self, bv_json, cq_json, surl):
        """
        分享视频消息格式
        """
        return "分享视频：\n%s\n上传者：%s\n视频分区：%s\n视频url：%s\n====================\n%s\n%s" % (
            bv_json["title"],
            bv_json["owner"]["name"],
            bv_json["tname"],
            surl,
            bv_json["desc"],
            image(bv_json["pic"].rsplit("/")[-1], bv_json["pic"])
        )
    
    def set_share_live_message(self, liveData, cq_json, surl):
        """
        分享直播间消息格式
        """
        cover_file_name = liveData["cover_from_user"].split("/")[-1]
        return "分享直播间：\n%s\n主播：%s\n直播分区：%s\n====================\n%s\n%s" % (
            liveData["title"],
            liveData["uname"],
            "%s-%s-%s" % (
                liveData["area_name"], 
                liveData["area_v2_parent_name"], 
                liveData["area_v2_name"]
            ),
            image(cover_file_name, liveData["cover_from_user"]),
            surl
        )
    
    def set_share_dynamic_message(self, dynamic_message, cq_json, surl):
        """
        分享动态消息格式
        """
        return "分享动态：\n动态短链接：%s\n====================\n%s" % (
            surl,
            dynamic_message
        )
    
    def set_share_cv_message(self, cv_text, cv_viewinfo_json, cq_json, surl):
        """
        分享专栏消息格式
        """
        img_list = ""
        for image_url in cv_viewinfo_json["origin_image_urls"]:
            img_list += image(image_url.split("/")[-1], image_url)

        return "分享专栏：\n%s\n专栏作者：%s\n专栏点击：%s\n专栏短链接：%s\n====================\n%s\n%s" % (
            cv_viewinfo_json["title"],
            cv_viewinfo_json["author_name"],
            cv_viewinfo_json["stats"]["view"],
            surl,
            cv_text,
            img_list
        )
    
    def set_share_cv_list_message(self, cv_list_json, cq_json, surl):
        """
        分享专栏文集消息格式
        """
        cv_list_text = ""
        for cv in cv_list_json["articles"][0:10]:
            cv_list_text = "%s\n    %s" % (cv_list_text, cv["title"])

        image_name = cv_list_json["list"]["image_url"].split("/")[-1]
        return "分享专栏文集：\n%s\n文集作者：%s\n文集短链接：%s\n====================\n%s\n文集前10条专栏：%s\n%s" % (
            cv_list_json["list"]["name"],
            cv_list_json["author"]["name"],
            surl,
            cv_list_json["list"]["summary"],
            cv_list_text,
            image(image_name, cv_list_json["list"]["image_url"])
        )
    
    def set_share_media_message(self, cq_json):
        """
        分享番剧消息格式
        epid 不能直接调 api 获取番剧详细懒得爬了
        """
        media_data = cq_json["meta"]["detail_1"]["title"].lstrip("《").split("》 ", 1)
        image_name = cq_json["meta"]["detail_1"]["preview"].split("/")[-1]
        return "分享番剧：\n%s\n番剧短链接：%s\n====================\n%s\n%s" % (
            media_data[0],
            cq_json["meta"]["detail_1"]["qqdocurl"].split("?")[0],
            media_data[1],
            image(image_name, "https://%s" % cq_json["meta"]["detail_1"]["preview"])
        )
    
    def set_live_message(self, liveData):
        """
        开播消息格式
        """
        cover_file_name = liveData["cover_from_user"].split("/")[-1]
        return "%s开播了！\n%s\n直播分区：%s\n====================\n%s\n%s" % (
            liveData["uname"],
            liveData["title"],
            "%s-%s-%s" % (
                liveData["area_name"], 
                liveData["area_v2_parent_name"], 
                liveData["area_v2_name"]
            ),
            image(cover_file_name, liveData["cover_from_user"]),
            "https://live.bilibili.com/%s" % liveData["room_id"],
        )
    
    def set_live_end_message(self, liveData):
        """
        下播消息格式
        """
        cover_file_name = liveData["cover_from_user"].split("/")[-1]
        return "%s下播了...\n%s\n直播分区：%s\n====================\n%s\n%s" % (
            liveData["uname"],
            liveData["title"],
            "%s-%s-%s" % (
                liveData["area_name"], 
                liveData["area_v2_parent_name"], 
                liveData["area_v2_name"]
            ),
            image(cover_file_name, liveData["cover_from_user"]),
            "https://live.bilibili.com/%s" % liveData["room_id"],
        )
    
    def set_dynamic_forward_message(self, dynamic, dynamic_id, forward_dynamic_msg):
        """
        转发动态消息格式
        """
        return "%s的动态更新！\n动态url：%s\n====================\n%s\n====================\n转发：%s" % (
            dynamic["user"]["uname"],
            "https://t.bilibili.com/%s" % dynamic_id,
            dynamic["item"]["content"],
            forward_dynamic_msg
        )
    
    def set_dynamic_forward_delete_message(self, dynamic, dynamic_id):
        """
        转发被删除动态消息格式
        """
        return "%s的动态更新！\n动态url：%s\n====================\n%s\n====================\n转发：%s" % (
            dynamic["user"]["uname"],
            "https://t.bilibili.com/%s" % dynamic_id,
            dynamic["item"]["content"],
            dynamic["item"]["tips"]
        )
    
    def set_dynamic_message(self, dynamic, dynamic_id):
        """
        动态消息格式
        """
        return "%s的动态更新！\n动态url：%s\n====================\n%s" % (
                dynamic["user"]["uname"],
                "https://t.bilibili.com/%s" % dynamic_id,
                dynamic["item"]["content"],
            )

    def set_dynamic_big_message(self, dynamic, dynamic_id):
        """
        动态消息格式
        """
        img_list = ""
        for image_url in dynamic["item"]["pictures"]:
            img_list += image(image_url["img_src"].split("/")[-1], image_url["img_src"])
        
        return "%s的动态更新！\n动态url：%s\n====================\n%s\n%s" % (
                dynamic["user"]["name"],
                "https://t.bilibili.com/%s" % dynamic_id,
                dynamic["item"]["description"],
                img_list
            )
    
    def set_dynamic_cv_message(self, dynamic, dynamic_id, cv_text):
        """
        专栏消息格式
        """
        img_list = ""
        for image_url in dynamic["image_urls"]:
            img_list += image(image_url.split("/")[-1], image_url)
        return "%s的专栏动态更新！\n%s\n动态url：%s\n====================\n%s\n%s" % (
            dynamic["author"]["name"],
            dynamic["title"],
            "https://t.bilibili.com/%s" % dynamic_id,
            cv_text,
            img_list,
        )
    
    def set_dynamic_video_message(self, dynamic, dynamic_id):
        """
        视频消息格式
        """
        return "%s的视频动态更新！\n%s\n视频分区：%s\n视频url：%s\n====================\n%s\n%s" % (
            dynamic["owner"]["name"],
            dynamic["title"],
            dynamic["tname"],
            dynamic["short_link"],
            dynamic["desc"],
            image(dynamic["pic"].split("/")[-1], dynamic["pic"]),
        )
    
    def set_dynamic_delete_message(self, dynamic_old_message):
        """
        记录的旧动态被删除
        """
        return "有旧动态被删除了...\n让我们永远记住它...\n====================\n%s" % dynamic_old_message
    
    def _dynamic_type_check(self, dynamic_type, dynamic, dynamic_id):
        """
        type: 动态类型

        1: 转发动态
        2: 普通动态 (日常动态?)
        4: 普通动态 (无图, B站这 api 为啥分开写???)
        8: 视频更新动态
        64: 专栏更新动态
        """
        if "card" in dynamic:
            card = json.loads(dynamic["card"])
        else:
            card = dynamic

        if dynamic_type == 1:
            if "origin" not in card:
                return self.set_dynamic_forward_delete_message(
                    card, dynamic_id
                )
            forward_dynamic = json.loads(card["origin"])
            forward_dynamic_type = card["item"]["orig_type"]
            forward_dynamic_id = card["item"]["orig_dy_id"]
            return self.set_dynamic_forward_message(card, dynamic_id, 
                self._dynamic_type_check(forward_dynamic_type, forward_dynamic, forward_dynamic_id))

        if dynamic_type == 2:
            return self.set_dynamic_big_message(card, dynamic_id)

        if dynamic_type == 4:
            return self.set_dynamic_message(card, dynamic_id)

        if dynamic_type == 8:
            return self.set_dynamic_video_message(card, dynamic_id)

        if dynamic_type == 64:
            cv_url = "https://www.bilibili.com/read/cv%s" % card["id"]
            # 爬取专栏内容
            with requests.get(cv_url) as req:
                cv_text = self.set_cv_text(req.text)

            return self.set_dynamic_cv_message(card, dynamic_id, cv_text)
    
    async def _monitor_live(self):
        """
        异步直播开播监听处理
        """
        live_list = await self.get_lives_status(self._monitor_live_uids)
        if not live_list:
            return

        for live_id in live_list["data"]:
            if live_list["data"][live_id]["live_status"] in (0, 2):
                if live_id in self._lives_old:
                    self._lives_old.remove(live_id)
                    live_end_message = self.set_live_end_message(live_list["data"][live_id])
                    self._send_msg_list.append(live_end_message)
                    logging.debug("监听到了下播 %s" % live_end_message)

                continue

            if live_id in self._lives_old:
                continue
            
            live_message = self.set_live_message(live_list["data"][live_id])
            self._send_msg_list.append(live_message)
            self._lives_old.append(live_id)
            logging.debug("监听到了开播 %s" % live_message)
    
    async def _dynamic_check(self, dynamic):
        dynamic = self._dynamic_type_check(
            dynamic["desc"]["type"], 
            dynamic, 
            dynamic["desc"]["dynamic_id"]
        )
        return dynamic

    async def _monitor_dynamic(self):
        """
        异步动态监听处理
        """
        dynamic_list = {}
        for uid in self._monitor_dynamic_uids:
            dynamic_data = await self.get_dynamic(uid)
            if not dynamic_data:
                return
            dynamic_new = dynamic_data["data"]["cards"][0]

            dynamic_list[uid] = {
                "time": dynamic_new["desc"]["timestamp"],
                "data": dynamic_new
            }
        
        for uid in dynamic_list:
            # 检查动态时间
            if dynamic_list[uid]["time"] == self._dynamic_list_old[uid]["time"]:
                continue
            
            # 记录的新动态被删除 (获取的新动态时间小干记录的新动态)
            if dynamic_list[uid]["time"] < self._dynamic_list_old[uid]["time"]:
                # 如果是视频更新 time 字段无法正常判断, 重新检查
                if dynamic_list[uid]["data"]["desc"]["type"] == 8:
                    # 检查动态 id
                    if dynamic_list[uid]["data"]["desc"]["dynamic_id"]  == self._dynamic_list_old[uid]["data"]["desc"]["dynamic_id"]:
                        continue

                dynamic = self.set_dynamic_delete_message(await self._dynamic_check(
                    self._dynamic_list_old[uid]["data"])
                )
                self._send_msg_list.append(dynamic)
                logging.debug("监听到了动态删除 %s" % dynamic)
                continue
            
            dynamic = await self._dynamic_check(
                    dynamic_list[uid]["data"]
                )
            self._send_msg_list.append(dynamic)
            logging.debug("监听到了新的动态 %s" % dynamic)

        self._dynamic_list_old = dynamic_list
    
    async def _monitor(self):
        """
        异步监听
        """
        try:
            if self._monitor_live_uids != {}:
                await self._monitor_live()
                self._live_monitor_in = False
            else:
                self._live_monitor_in = False
        except Exception as err:
            self.monitorLiveError(err)
        
        try:
            if self._monitor_dynamic_uids != {}:
                await self._monitor_dynamic()
                self._dynamic_monitor_in = False
            else:
                self._dynamic_monitor_in = False
        except Exception as err:
            self.monitorDynamicError(err)
    
    def monitor(self):
        """
        监听
        """
        self.cqapi.add_task(self._monitor())
        while self._dynamic_monitor_in or self._live_monitor_in:
            pass

        self._dynamic_monitor_in = True
        self._live_monitor_in = True
    
    def monitor_send(self, group_id):
        """
        发送监听到的信息
        """
        for message in self._send_msg_list:
            self.cqapi.send_group_msg(group_id, message)
    
    def monitor_send_clear(self):
        """
        清空监听到的信息
        """
        self._send_msg_list = []
    
    def monitorLiveError(self, err):
        """
        监听直播信息时错误
        """
        logging.error("监听直播信息发生错误! Error: %s" % err)
        logging.exception(err)

    def monitorDynamicError(self, err):
        """
        监听动态信息时错误
        """
        logging.error("监听动态信息发生错误! Error: %s" % err)
        logging.exception(err)
    
    def getShareVideoError(self, err):
        """
        解析分享信息时错误
        """
        logging.error("解析分享信息发生错误! Error: %s" % err)
        logging.exception(err)
    
    def biliApiError(self, code, err_msg):
        """
        请求 bilibili api 时错误
        """
        logging.error("请求 bilibili api发生错误! Error: %s code:%s" % (err_msg, code))


class pixiv:

    def __init__(self, cqapi, forward_name, forward_qq, proxy=None, cookie="", max_rlen=10, max_pid_len=20):
        self.cqapi = cqapi
        self._forward_qq = forward_qq
        self._forward_name = forward_name
        self._max_rlen = max_rlen
        self._max_pid_len = max_pid_len
        self._proxy= "http://%s" % proxy
        self._headers = [
            "referer=https://www.pixiv.net/",
            "cookie=%s" % cookie
        ]

        self._pyheaders = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "cookie": cookie
        }
    
    def _json_data_check(self, data):
        if data["error"]:
            self.pixivApiError(data)
            return False
        
        return data
    
    async def send_image_list(self, image_list, message):
        """
        转发图片表
        """
        message_id_list = []
        for image_url in image_list:
            cache_file = await self.cqapi._cqhttp_download_file(image_url, self._headers)
            message_id_list.append(image("file://%s" % cache_file))

        self.cqapi.send_group_forward_msg(message["group_id"], node_list(message_id_list, 
            self._forward_name,
            self._forward_qq
        ))

    async def search_image(self, search_data, page):
        api = "https://www.pixiv.net/ajax/search/artworks/%s?word=%s&order=date_d&mode=all&p=%s&s_mode=s_tag_full&type=all&lang=zh" % (
            search_data,
            search_data,
            page
        )
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._pyheaders))
    
    async def user_image_id(self, user_id):
        api = "https://www.pixiv.net/ajax/user/%s/profile/all?lang=zh" % (
            user_id
        )
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._pyheaders))
    
    async def get_image(self, img_id, message):
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

    
    async def get_user(self, user_name, nick=False):
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
    
    async def random_image(self, image_list, rlen, message):
        random_image_list = []
        img_id_list = []
        # 随机原图
        for _ in range(0, int(rlen)):
            while True:
                img_id = random.choice(image_list)

                if img_id in img_id_list:
                    continue

                if "id" in img_id:
                    img_id_list.append(img_id["id"])
                else:
                    img_id_list.append(img_id)

                break

            img_data = await self.get_image(img_id_list[-1], message)
            if not img_data:
                continue
                
            random_image_list.append(img_data[0]["urls"]["original"])
        
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
            data = await self.search_image(search_data, 1)
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
            data = await self.search_image(search_data, random_page)
            image_list = data["body"]["illustManga"]["data"]

            if len(image_list) < int(rlen):
                rlen = len(image_list)
                self.insufficient_search_image(search_data, rlen, message)
            
            await self.send_image_list(await self.random_image(image_list, rlen, message), message)
        except Exception as err:
            self.randomSearchImageError(search_data, rlen, err)
            return False
    
    async def _search_user_image_random(self, user_name, rlen, message, nick=False):
        """
        随机用户作品
        """

        try:
            if int(rlen) > self._max_rlen:
                self.maxRlen(rlen, message)
                rlen = self._max_rlen

            # 获取用户作品 id
            user_item = await self.get_user(user_name, nick)
            if not user_item:
                self.searchNotUser(user_name, rlen, nick, message)
                return False

            user_image_id_list = await self.user_image_id(user_item["user_id"])
            user_image_id_list = list(user_image_id_list["body"]["illusts"].keys())

            await self.send_image_list(await self.random_image(user_image_id_list, rlen, message), message)
        except Exception as err:
            self.randomSearchUserImageError(user_name, rlen, nick, err)
            return False
    
    async def _search_pid(self, pid, message):
        try:
            img_data = await self.get_image(pid, message)
            if not img_data:
                return False
            
            if len(img_data) > self._max_pid_len:
                self.maxPidLen(len(img_data), message)
                img_data = img_data[0: self._max_pid_len]

            send_img = []
            for img in img_data:
                send_img.append(img["urls"]["original"])
                
            await self.send_image_list(send_img, message)
        except Exception as err:
            self.searchPidError(pid, err)
            return False
    
    def search_image_random(self, search_data, rlen, message):
        self.cqapi.add_task(self._search_image_random(search_data, rlen, message))
    
    def search_user_image_random(self, user_name, rlen, message, nick=False):
        self.cqapi.add_task(self._search_user_image_random(user_name, rlen, message, nick))
    
    def search_pid(self, pid, message):
        self.cqapi.add_task(self._search_pid(pid, message))
    
    def none_search_image(self, search_data, rlen, message):
        self.cqapi.send_reply(message, "%s 没有搜索到数据..." % search_data)
    
    def insufficient_search_image(self, search_data, rlen, message):
        self.cqapi.send_reply(message, "%s 数据量不足于指定量，将全部返回%s张" % (search_data, rlen))
    
    def notImage(self, img_id, err_msg, message):
        self.cqapi.send_group_msg(message["group_id"], "无法获得到 %s，%s" % (img_id, err_msg))
    
    def searchNotUser(self, user_name, rlen, nick, message):
        self.cqapi.send_group_msg(message["group_id"], "没有 %s 的用户" % user_name)
    
    def maxRlen(self, rlen, message):
        self.cqapi.send_group_msg(message["group_id"], "指定量 %s 超出最大值 %s，将返回最大值" % (rlen, self._max_rlen))
    
    def maxPidLen(self, rlen, message):
        self.cqapi.send_group_msg(message["group_id"], "指定量 %s 超出 PID 获取最大值 %s，将截取" % (rlen, self._max_pid_len))
    
        
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
    
    def searchPidError(self, pid_list, err):
        logging.error("搜索 PID %s 时发生错误! Error: %s " % (pid_list, err))
        logging.exception(err)
    
    def getImageError(self, img_id, err):
        logging.error("搜索图片 %s 时发生错误! Error: %s " % (img_id, err))
        logging.exception(err)
    
    def getUserError(self, user_name, nick, err):
        logging.error("搜索用户 %s 时发生错误! Error: %s " % (user_name, err))
        logging.exception(err)

    def pixivApiError(self, err_msg):
        """
        请求 pixiv api 时错误
        """
        logging.error("请求 pixiv api发生错误! Error: %s " % err_msg)