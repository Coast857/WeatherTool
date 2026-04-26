import requests
import time #time模块，用于retry等待
from utils.logger import get_logger #导入日志工具

#创建当前模块的日志记录器
logger=get_logger(__name__)

# 通用请求工具类
class RequestUtil:
    #发送HTTP请求（核心函数）
    def send_request(
            self,
            method,
            url,
            params=None,
            json=None,
            headers=None,
            timeout=10,
            retry=3
    ):
        '''
        指数退避重试：
        第1次失败：等1s
        2次失败：等2s
        3次失败：等4s
        '''
        #retry核心循环
        for i in range(retry):
            try:
                #记录请求开始日志
                logger.info(f"开始请求：{method}{url}")
                #发送HTTP请求
                response=requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers=headers,
                    timeout=timeout
                )
                #打印返回状态码
                logger.info(f"请求完成 状态码：{response.status_code}")
                #若状态码不是200，会抛异常
                response.raise_for_status()
                #返回JSON数据
                return response.json()
            except requests.exceptions.RequestException as e:
                #记录失败日志
                logger.error(f"请求失败 第{i+1}次：{e}")
                #如果最后一次失败
                if i==retry-1:
                    logger.error("达到最大重试次数，请求最终失败")
                    return None
                #指数退避
                sleep_time= 2**i
                logger.info(
                    f"等待{sleep_time}秒后重试"
                )
                time.sleep(sleep_time)#等待1秒再重试