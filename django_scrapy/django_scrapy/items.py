# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DjangoScrapyItem(scrapy.Item):
    v_bid = scrapy.Field()  #视频链接
    page_number = scrapy.Field()    #评论页码
    author = scrapy.Field() #评论作者
    c_time = scrapy.Field() #评论时间
    ip_location = scrapy.Field() #ip属地
    likes = scrapy.Field()  #点赞数
    content = scrapy.Field()    #评论内容