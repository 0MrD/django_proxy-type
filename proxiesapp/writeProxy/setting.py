import logging
from environs import Env
from fake_headers import Headers
"""配置文件"""
env = Env()
# redis host
REDIS_HOST = env.str('PROXYPOOL_REDIS_HOST',
                     env.str('REDIS_HOST', '127.0.0.1'))
# redis port
REDIS_PORT = env.int('PROXYPOOL_REDIS_PORT', env.int('REDIS_PORT', 6379))
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('PROXYPOOL_REDIS_PASSWORD',
                         env.str('REDIS_PASSWORD', None))
# redis db, if no choice, set it to 0
REDIS_DB = env.int('PROXYPOOL_REDIS_DB', env.int('REDIS_DB', 3))

#redis key
REDIS_KEY = env.str('PROXYPOOL_REDIS_KEY', env.str(
    'REDIS_KEY', 'proxies:universal'))
#数据库代理数
Redis_PROXY_MIN = 40

#代理分数的定义
PROXY_SCORE_MAX = 50
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 10
Iteration_score = 1 #请求失败分数每次减1

#响应返回状态
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])
#asyncio并发数
ASYNCIO_SEMAPHORE = 10
#请求超时时间
REQUEST_TIMEOUT=10

#日志格式等设置
format = "%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d：%(message)s"
datefmt= "%Y/%m/%d %H:%M:%S"
logging.basicConfig(format=format,datefmt=datefmt,level=logging.INFO)
#生成随机header信息
REQUEST_HEADER = str(Headers(headers=True).generate())