#只负责高层逻辑的调度，不包含具体功能的实现细节
from api.weather_api import fetch_weather #从api包的weather_api模块导入获取天气函数
from utils.file_util import save_to_json #导入保存文件函数
from utils.logger import get_logger #导入获取记录器函数
logger=get_logger("Main") # 获取名为Main的主程序日志记录器
def main():
    logger.info("天气获取程序启动")
    weather_data=fetch_weather() #调用天气抓取函数
    if weather_data: #若成功获取数据，则调用保存函数写入文件
        save_to_json(weather_data,'石家庄天气.json')
    else:
        logger.warning("未获取到天气数据，已跳过存储步骤")#记录警告级别的日志
    logger.info("天气获取程序运行结束") #记录程序正常结束的日志
if __name__ == "__main__": #判断当前脚本是否作为主程序直接运行
    main() #执行主函数