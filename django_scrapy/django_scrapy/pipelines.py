# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import json
import time

import pandas as pd

from itemadapter import ItemAdapter


class DjangoScrapyPipeline:
    filename = r'D:\pythonProjects\django_proxy_检测了代理类型\django_scrapy\django_scrapy\saveInfo\bilibili淄博评论爬取.csv'
    headers = ('视频链接', '评论页码', '评论作者', '评论时间', 'ip属地', '点赞数', '评论内容')

    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        # 这里不能使用with open() as方式,因为这种方式会自动.close()关闭文件的,
        # 会导致process_item()方法里writer.writerow(row_data)写入数据失败
        self.file = open(self.filename, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)  # 初始化文件对象
        if self.file.tell() == 0:  # 检查文件指针位置,判断是否需要写入标题行
            self.writer.writerow(self.headers)

    def process_item(self, item, spider):
        row_data = [
            item.get("v_bid", "N/A"),  # 没有数据则返回N/A
            item.get("page_number", "N/A"),
            item.get("author", "N/A"),
            item.get("c_time", "N/A"),
            item.get("ip_location", "N/A"),
            item.get("likes", "N/A"),
            item.get("content", "N/A")
        ]
        self.writer.writerow(row_data)
        return item

    def close_spider(self, spider):
        self.drop_duplicates()
        self.file.close()
    #去重
    def drop_duplicates(self):
        df = pd.read_csv(filepath_or_buffer=self.filename,nrows=300)
        df.drop_duplicates(subset=["评论作者", "评论时间", "评论内容"], inplace=True)
        df.to_csv(r'D:\pythonProjects\django_proxy_检测了代理类型\django_scrapy\django_scrapy\saveInfo\bilibili淄博评论爬取2.csv')