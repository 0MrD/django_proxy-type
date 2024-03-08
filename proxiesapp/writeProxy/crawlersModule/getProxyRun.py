import logging
import multiprocessing
from proxiesapp.writeProxy.crawlersModule.getProxy_KXdaili import crawles_KXdaili
from proxiesapp.writeProxy.crawlersModule.getProxy_89daili import crawles_89daili
from proxiesapp.writeProxy.crawlersModule.getProxy_qiyundaili import crawles_qiyundaili

class getProxyRun():
    def run_KXdaili(self):
        self.crawles_KXdaili = crawles_KXdaili()
        self.crawles_KXdaili.run()

    def run_89daili(self):
        self.crawles_89daili = crawles_89daili()
        self.crawles_89daili.run()

    def run_qiyundaili(self):
        self.crawles_qiyundaili = crawles_qiyundaili()
        self.crawles_qiyundaili.run()

    #使用进程来并行执行
    def run(self):
        global first_process, two_process,tree_process
        try:
            logging.info('爬取工作开始...')
            if True:
                logging.info(f'爬取KXdaili代理网址...')
                first_process = multiprocessing.Process(target=self.run_KXdaili())
                first_process.start()
            """if True:
                logging.info(f'爬取89daili代理网址...')
                two_process = multiprocessing.Process(target=self.run_89daili())
                two_process.start()"""

            if True:
                logging.info(f'爬取qiyundaili代理网址...')
                tree_process = multiprocessing.Process(target=self.run_qiyundaili())
                tree_process.start()
            first_process.join()
            #two_process.join()
            tree_process.join()
        except KeyboardInterrupt:   #异常
            first_process.terminate()   #强制终止进程
            #two_process.terminate()
            tree_process.terminate()
        finally:
            first_process.join()
            #two_process.join()
            tree_process.join()
            logging.info('爬取工作结束...')
if __name__ == '__main__':
    get = getProxyRun()
    get.run()