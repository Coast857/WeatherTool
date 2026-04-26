#日志工厂函数，确保整个项目使用统一的日志格式
import logging
import os
from datetime import datetime #导入时间模块用于生成日志文件名
def get_logger(name="ProjectLogger"):#定义获取日志记录器的函数
    logger=logging.getLogger(name) #获取一个现有的日志记录器
    if not logger.handlers:#判断记录器是否已经配置过处理器，避免重复添加导致日志打印多次
        logger.setLevel(logging.INFO)#设置记录器的最低捕获级别为INFO
        if not os.path.exists('logs'):#检查当前目录下是否存在logs文件夹
            os.makedirs('logs')
        current_time=datetime.now().strftime("%Y%m%d_%H%M%S")#获取当前时间并格式化为字符串
        log_file_path=f'logs/weather_{current_time}.log'#拼接日志文件的相对路径

        file_handler=logging.FileHandler(log_file_path,encoding='utf-8')#创建文件处理器
        file_handler.setLevel(logging.INFO)#设置文件处理器的日志级别为INFO

        console_handler=logging.StreamHandler()#创建控制台处理器
        console_handler.setLevel(logging.INFO)#设置控制台处理器的日志级别
        formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')#定义日志输出格式，加入name表示日志来源
        file_handler.setFormatter(formatter)#为文件处理器绑定格式
        console_handler.setFormatter(formatter) #为控制台处理器绑定格式
        logger.addHandler(file_handler)#将文件处理器添加到记录器中
        logger.addHandler(console_handler)#将控制台处理器添加到记录器中
    return logger #返回配置好的日志记录器

