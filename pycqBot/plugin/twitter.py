import logging
import time
from pycqBot.object import Plugin
from pycqBot.cqApi import cqBot, cqHttpApi


class twitter(Plugin):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config) -> None:
        super().__init__(bot, cqapi, plugin_config)
        self._send_msg_list = []
        self._proxy = ("http://%s" % plugin_config["proxy"]) if "proxy" in plugin_config else None
        self._bearer_token = plugin_config["bearerToken"]

        self._headers = {
            "Authorization": f"Bearer {self._bearer_token}"
        }
        self._user_list = plugin_config["monitor"]
        if self._user_list is None:
            logging.warning("twitter 插件未配置 monitor 中止加载")
            return

        self._user_id_list = []
        self._old_tweets_id_list = []
        self._monitor_in = True

        self.monitor()
        self.monitor_send_clear()

        bot.timing(self.monitor_send, "twitter_monitor_send", {
            "timeSleep": plugin_config["timeSleep"] if "timeSleep" in plugin_config else 60
        })
    
    def timing_jobs_start(self, job, run_count):
        if job["name"] == "twitter_monitor_send":
            self.monitor()
    
    def timing_jobs_end(self, job, run_count):
        if job["name"] == "twitter_monitor_send":
            self.monitor_send_clear()

    def _json_data_check(self, data):
        if data is None:
            return None
            
        if "status" in data:
            self.twitterApiError(data["status"], data["title"])
            return None

        return data

    async def get_user(self, user_list):
        api = "https://api.twitter.com/2/users/by?usernames=%s" % ",".join(user_list)
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._headers))

    async def get_timelines(self, user_id):
        api = "https://api.twitter.com/2/users/%s/tweets" % user_id
        return self._json_data_check(await self.cqapi.link(api, proxy=self._proxy, headers=self._headers))

    async def get_user_id_list(self):
        user_data_list = await self.get_user(self._user_list)
        if user_data_list is None:
            return

        for user_data in user_data_list["data"]:
            self._user_id_list.append(user_data["id"])
    
    def set_tweets_message(self, text):
        return text

    def set_tweets_delete_message(self, text):
        return text

    async def _monitor(self):
        try:
            if self._user_id_list == []:
                await self.get_user_id_list()

            for index, user_id in enumerate(self._user_id_list):
                timelines = await self.get_timelines(user_id)
                if timelines is None:
                    return

                newest_id = timelines["meta"]["newest_id"]
                try:
                    if newest_id == self._old_tweets_id_list[index]:
                        continue
                    
                    if newest_id > self._old_tweets_id_list[index]:
                        self._send_msg_list.append(self.set_tweets_message(timelines["data"][0]["text"]))
                    
                    if newest_id < self._old_tweets_id_list[index]:
                        self._send_msg_list.append(self.set_tweets_delete_message(timelines["data"][0]["text"]))

                except IndexError:
                    self._old_tweets_id_list.append(newest_id)

        except Exception as err:
            self.monitorTweetsError(err)
        
        self._monitor_in = False

    def monitor(self):
        self.cqapi.add_task(self._monitor())
        while self._monitor_in:
            time.sleep(1)
        
        self._monitor_in = True
    
    def monitor_send_clear(self):
        self._send_msg_list = []

    def monitor_send(self, group_id):
        """
        发送监听到的信息
        """
        for message in self._send_msg_list:
            self.cqapi.send_group_msg(group_id, message)
    
    def twitterApiError(self, code, error):
        """
        推特 api 错误
        """
        logging.error("推特 api 错误 code: %s error: %s" % (code, error))
    
    def monitorTweetsError(self, err):
        """
        推文更新错误
        """
        logging.error("监听推文更新错误 error: %s" % err)
        logging.exception(err)