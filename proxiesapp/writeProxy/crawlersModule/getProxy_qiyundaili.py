import logging
from lxml import etree
import requests
from proxiesapp.writeProxy.setting import PROXY_SCORE_INIT, REQUEST_HEADER
from proxiesapp.writeProxy.storageModule.iniSaveProxyRedis import inisave_proxy_redis

class crawles_qiyundaili():
    def __init__(self):
        self.inisaveproxyredis = inisave_proxy_redis()

    def parse(self):
        header = {"User-Agent": REQUEST_HEADER}
        ips = []
        for i in range(1,11):
            url = f"https://proxy.ip3366.net/free/?action=china&page={i}"
            res = requests.get(url= url,headers = header).text
            etree_tree = etree.HTML(res)
            ip_list = etree_tree.xpath('//*[@id="content"]/section/div[2]/table/tbody/tr/td[1]/text()')
            port_list = etree_tree.xpath('//*[@id="content"]/section/div[2]/table/tbody/tr/td[2]/text()')
            url_type_list = etree_tree.xpath('//*[@id="content"]/section/div[2]/table/tbody/tr/td[4]/text()')
            for ip,port,type in zip(ip_list,port_list,url_type_list):
                ips.append(f"{ip}:{port}")
                ip_port=ip+":"+port
                dict={
                    "proxy":type.lower()+"://"+ip_port,
                    "score":PROXY_SCORE_INIT    #爬取代理，默认设置score为PROXY_SCORE_INIT
                }
                yield dict
        logging.info(f"qiyun代理一共爬取到 {len(ips)} 个代理数")

    def run(self):
        generator = self.parse()
        self.inisaveproxyredis.save_proxy_redis(generator)  #代理保存到数据库