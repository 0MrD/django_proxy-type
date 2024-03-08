import json
import logging
from proxiesapp.writeProxy.storageModule.RedisClient import RedisClient
#页面爬取到代理后保存到数据库,并设置初始分数为10
class inisave_proxy_redis():
    def __init__(self):
        self.redisClient = RedisClient()

    def save_proxy_redis(self, generator):
        for ip in generator:
            self.redisClient.hset(ip["proxy"].split("//")[-1],json.dumps(ip))
        logging.info(f"代理保存到数据库完成")

