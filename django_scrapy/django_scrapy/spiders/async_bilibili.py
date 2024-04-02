import hashlib
import json
import time
import urllib.parse
from datetime import datetime
import scrapy
from ..items import DjangoScrapyItem
import aiohttp

# -*- coding: utf-8 -*-
# @Author  : C_d_HF
# @Time    : 2024/3/19 11:38
# @Function:
class BilibiliSpider(scrapy.Spider):
    name = "async_bilibili"
    allowed_domains = ["www.bilibili.com"]
    start_urls = ["http://www.bilibili.com/"]

    # 解析
    """使用异步解析,因为scrapy框架本身就是异步的,会自动创建事件循环和管理事件循环,所以我们不用再去创建事件循环了,不然会出现报错
        只需要标记async就可以；虽然scrapy本身就是异步的，但是我们还是用asyncio来做异步方法,因为这样比scrapy本身的异步处理快
    """
    async def parse(self, response):
        url, headers = self.construct_url()
        start = time.time()
        async with  aiohttp.ClientSession() as session:
            for i in range(1, 380):  # 因为bilibili这个是xhr方式获取评论的,且根据时间,所以这里循环执行10次
                # 因为requests模块会自动编码url中的params信息,所有这里我们直接拼接url得到我们需要的url
                response = await session.get(url=url, headers=headers)
                re = await response.json()
                try:
                # 解析
                    datas = re["data"]["replies"]
                    for data in datas:
                        item = DjangoScrapyItem()
                        item["v_bid"] = "https://www.bilibili.com/video/BV1To4y1b7xZ/"  # 视频的id为BV1To4y1b7xZ,不同视频的id不一样
                        item["page_number"] = data["type"]
                        item["author"] = data["member"]["uname"]
                        item["c_time"] = self.format_date(data["ctime"])
                        item["ip_location"] = data["reply_control"]["location"].split("：")[-1]
                        item["likes"] = data["like"]
                        item["content"] = data["content"]["message"]
                        yield item
                except Exception as e:
                    print("异常：", e)
                    continue
            end = time.time()
            print("请求时间:", end - start)


    # 时间戳转换
    def format_date(self, c_time):
        """10位时间戳转换为时间字符串"""
        dt_obj = datetime.fromtimestamp(c_time)
        otherStyleTime = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    # 构造真正返回数据的url
    def construct_url(self):
        # 构造url信息
        wts = str(round(time.time()))
        pagination_str = {
            "offset": "{\"type\":1,\"direction\":1,\"session_id\":\"1752518247929182\",\"data\":{}}"}  # session_id会过期,所以要定时换
        pagination_str_encoded = urllib.parse.quote(json.dumps(pagination_str).replace(" ", ""))
        Wt = "ea1db124af3c7062474693fa704f4ff8"
        Jt = f'mode=3&oid=397712597&pagination_str={pagination_str_encoded}&plat=1&type=1&web_location=1315875&wts={wts}'
        w_rid = hashlib.md5((Jt + Wt).encode()).hexdigest()
        parame = {
            "oid": 397712597,
            "type": 1,
            "mode": 3,
            "pagination_str": json.dumps(pagination_str).replace(" ", ""),
            "plat": 1,
            "web_location": 1315875,
            "w_rid": w_rid,
            "wts": wts
        }
        headers = {
            'authority': 'api.bilibili.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            # cookie可能会过期,所以需要随时更换
            'cookie':"buvid3=A3B8D23D-6C2C-3612-B860-4A5A684797C244593infoc; b_nut=1694510444; _uuid=FBB7CBB8-1672-9679-D1072-8948107A8FB3144782infoc; buvid4=B5FF27E6-ECE0-87A4-4368-4A14B7A915F247420-023091217-cHGytz2Yu5Gcuv3nPrJFXw==; enable_web_push=DISABLE; header_theme_version=CLOSE; rpdid=|(um|u~)RulR0J'uYmmRk~|kJ; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO4016994271333969; CURRENT_FNVAL=4048; home_feed_column=5; bsource=search_baidu; PVID=1; fingerprint=4d0e7db595614687fef04a75d9d487d6; buvid_fp_plain=undefined; buvid_fp=4d0e7db595614687fef04a75d9d487d6; bp_video_offset_36123526=912759826924175368; b_lsid=CBD610101F_18E789A7161; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE2ODAzNDMsImlhdCI6MTcxMTQyMTA4MywicGx0IjotMX0.35p4BjJYoOragglVAow1E9Q_AraXq4NoPQSFDZSbCwQ; bili_ticket_expires=1711680283; browser_resolution=1448-720; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW; SESSDATA=0e23044d,1726975095,10edf*31CjClJtp8W0pER-D8WOZKGkdNeiDGEbjdnTXI0A15vg1QTF9CBIudRbTEAK2xn-7uYvISVk53UEh6Z1BEUVFtVEZ6RlF0X2ZTWjlWZ0EwV1ZhZ2o5RnFXX3NiZ2JEbFRWeDZaXzlqcU9LSGpEcENMUVEtZUhHd1lZTm9EeXpMaVl4NFBTWjR2VTZRIIEC; bili_jct=ad6d40181a1b8b30c99b09a2352f76d1; DedeUserID=36123526; DedeUserID__ckMd5=614ce7af2fc12d34; sid=4ufsx5j6",
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/video/BV1To4y1b7xZ/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        encoded_params = "&".join([f"{k}={v}" for k, v in parame.items()])
        url = f"https://api.bilibili.com/x/v2/reply/wbi/main?{encoded_params}"
        return url, headers
