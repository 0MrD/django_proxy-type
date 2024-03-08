import redis
import random
from proxiesapp.writeProxy.setting import REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_KEY,PROXY_SCORE_MIN

"""存储模块：对数据库中的代理进行操作"""
class RedisClient():
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
        self.redis_db = redis.Redis(host, port, db,decode_responses=True)   #设置decode_responses=True,输出就不会有前缀'b'了
    #随机获取ip并校验
    def get_random_proxy(self):
        #其实这里还可以加一个先随机最高分数50的,然后再随机50分以下的,但是这个因为是使用hash,所以不好设计
        keys = self.hkeys()
        random_key = random.choice(keys)
        return random_key
        """proxies = self.redis_db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX)  # 先随机最大分数的,确保最大分数50的都能被使用到
        if len(proxies):
            return random.choice(proxies)
        proxies = self.redis_db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)  # 随机50分以下的
        if len(proxies):
            return random.choice(proxies)
        return Exception  # 以上都没有则报错"""

    #增加/修改键值
    def hset(self,k,v):
        return self.redis_db.hset(REDIS_KEY,k,v)
    # 获取哈希元素个数 类似于len
    def hcount(self):
        return self.redis_db.hlen(REDIS_KEY)
    #获取所有的key
    def hkeys(self):
        return self.redis_db.hkeys(REDIS_KEY)
    #获取所有的value值
    def hvals(self):
        return self.redis_db.hvals(REDIS_KEY)
    #根据key获取value
    def hget(self,key):
        return self.redis_db.hget(REDIS_KEY,key)
    #根据key删除键值对
    def hdel(self,key):
        return self.redis_db.hdel(REDIS_KEY,key)
    #获取所有的键值对
    def hgetAll(self):
        return self.redis_db.hgetall(REDIS_KEY)
    #代理不可用,则降低分数,如果小于PROXY_SCORE_MIN,则删除
    def hash_update_proxy_db(self, score,key,value):
        if score <= PROXY_SCORE_MIN:
            return self.hdel(key)
        else:
            return self.hset(key,value)


