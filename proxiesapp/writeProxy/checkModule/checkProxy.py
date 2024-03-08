import json
from proxiesapp.writeProxy.storageModule.RedisClient import *  # 导入RedisClient类里的所有,包括里面的模块等
from proxiesapp.writeProxy.setting import *
from proxiesapp.writeProxy.crawlersModule.getProxyRun import getProxyRun
import asyncio, aiohttp

"""检测模块：检测数据库中的代理是否可用"""
class check_proxy_ip():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.getProxyRun = getProxyRun()
        self.redisClient = RedisClient()
        self.semaphore = asyncio.Semaphore(ASYNCIO_SEMAPHORE)  # 控制并发量

    # 校验数据库里抓取下来的IP是否可用,然后更新
    async def check_proxy_ip(self,url,proxies):
        header = {"User-Agent": REQUEST_HEADER}
        key = proxies.split("//")[-1]  # 通过拼接获取到redis中的key
        dict_values = self.str_to_obj(self.redisClient.hget(key))  # 根据key获取到value,然后使用json.loads将字符串转为字典的对象类型
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url=url,headers=header, proxy=proxies, timeout=REQUEST_TIMEOUT,allow_redirects=False) as response:
                        await asyncio.sleep(5)
                        if response.status in TEST_VALID_STATUS:
                            dict_values["score"] = PROXY_SCORE_MAX
                            self.redisClient.hset(key,self.obj_to_str(dict_values)) # 可用代理,则分数设置为50
                            logging.info(f"{proxies} 可用,分数设置为{PROXY_SCORE_MAX}")
                        else:
                            # 可用代理,但可以服务器因为超出最大连接等原因,则分数dict_values["score"] - 1
                            dict_values["score"] = dict_values["score"] - Iteration_score
                            self.redisClient.hash_update_proxy_db(dict_values["score"],key,self.obj_to_str(dict_values))
                            logging.info(f"{proxies} 可能超时,分数将-1")
                except Exception as e:
                    # 可能是请求超时,则分数dict_values["score"] - 1
                    dict_values["score"] = dict_values["score"] - Iteration_score
                    self.redisClient.hash_update_proxy_db(dict_values["score"], key, self.obj_to_str(dict_values))
                    logging.error(f"{proxies} 可能超出最大连接,分数将-1")

    # 实现定时去爬取页面的代理：检测数据库里代理数如果小于Redis_PROXY_INIT,则再去获取代理
    def check_count(self):
        count = self.redisClient.hcount()
        if count < Redis_PROXY_MIN:
            logging.info(f"当前数据库代理量小于{Redis_PROXY_MIN},则再次执行代理爬取工作")
            return self.getProxyRun.run()

    # 对象转为字符串
    def obj_to_str(self,data):
        return json.dumps(data)

    # 字符串转为对象
    def str_to_obj(self,data):
        return json.loads(data)#检测代理的是http还是https的类型

    def check_type(self, proxy):
        https_url = "https://www.qq.com/"
        http_url = "http://httpbin.org/get"
        if proxy.startswith('https'):
            url = https_url
        else:
            url = http_url
        proxies = {url.split(":")[0]: proxy}
        return url, proxies

    # 构建一个关于代理的列表,以便于实现多任务异步协程
    def proxy_list(self,values):
        list = []
        for value in values:
            obj_value = self.str_to_obj(value)
            url,proxy = self.check_type(obj_value["proxy"])
            dict = {    #构建字典
                "url": url,
                "proxy": proxy
            }
            list.append(dict)   #添加到列表
        return list
    # 运行
    def run(self):
        self.check_count()  # 检测数据库中的代理数量
        values = self.redisClient.hvals()
        list = self.proxy_list(values)
        task_list = [self.check_proxy_ip(proxy["url"],[i for i in proxy["proxy"].values()][-1]) for proxy in list]  # 多任务
        self.loop.run_until_complete(asyncio.wait(task_list))


"""另一种方式控制并发量
        count = self.redisClient.count()
        task_list=[]
        for i in range(0,count,20):
            start, end = i, min(i + 20, count)
            proxies = self.redisClient.get_proxy(start,end)
            task_list = [self.chek_proxy_ip(proxy) for proxy in proxies]
            self.loop.run_until_complete(asyncio.wait(task_list))"""
if __name__ == '__main__':
    check_proxy_ip = check_proxy_ip()
    check_proxy_ip.run()
