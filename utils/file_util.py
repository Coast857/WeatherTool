#将原有的save_to_file功能抽离成通用的文件工具模块
import json
import os
from utils.logger import get_logger #从自定义的logger模块导入获取记录器的函数
logger = get_logger(__name__)#初始化当前文件的日志记录器，__name__会自动传入当前模块名
def save_to_json(data,filename,directory='data'):#定义保持JSON文件的函数，增加目录参数增强灵活性
    try:#开启异常捕获块
        if not os.path.exists(directory):#检查目标保存目录是否存在
            os.makedirs(directory)
        filepath=os.path.join(directory,filename)#拼接完整的保存路径
        with open(filepath,'w',encoding='utf-8') as f:#以写入模式打卡文件
            json.dump(data,f,ensure_ascii=False,indent=4)#将Python字典序列化为JSON格式并写入文件，缩进对齐
        logger.info(f"数据已成功保存到{filepath}")#记录保存成功的INFO级别日志
        return True
    except Exception as e:#捕获所有运行时的异常
        logger.error(f"保存文件失败：{e}")#记录异常的ERROR级别日志
        return False