import logging
import re
from proxiesapp.writeProxy.setting import REQUEST_HEADER
from proxiesapp.writeProxy.storageModule.iniSaveProxyRedis import inisave_proxy_redis
import requests
#爬取89代理网址
class crawles_89daili():
    def __init__(self):
        self.inisaveproxyredis = inisave_proxy_redis()
    def parse(self):
        header = {"User-Agent": REQUEST_HEADER}
        ips = []
        for i in range(1,11):
            url = f"https://www.89ip.cn/index_{i}.html"
            response = requests.get(url=url,headers=header).text
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                response)
            for proxy in proxies:
                ips.append(':'.join(proxy))
                yield ':'.join(proxy)# 使用yield,可以避免return的问题,它会直接返回值,然后记住这次执行的位置,下一次执行就从这个位置开始
        logging.info(f"89ip代理一共爬取到 {len(ips)} 个代理数")
    #运行
    def run(self):
        generator = self.parse()
        self.inisaveproxyredis.save_proxy_redis(generator)#代理保存到数据库

