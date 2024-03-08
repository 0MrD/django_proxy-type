import logging
import time
from proxiesapp.writeProxy.checkModule.checkProxy import check_proxy_ip
#调度模块
class Scheduler():
    def run_get_check_proxy(self):
        self.check_proxy_ip = check_proxy_ip()
        loop = 1
        while True:
            logging.info(f"第 {loop} 轮调度开始...")
            self.check_proxy_ip.run()
            loop += 1
            #使用sleep来实现定时去检查数据库的代理是否可用
            time.sleep(20)
    def run(self):
        self.run_get_check_proxy()
if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()