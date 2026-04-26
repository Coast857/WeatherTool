#只负责高层逻辑的调度，不包含具体功能的实现细节
from api.weather_api import fetch_weather #从api包的weather_api模块导入获取天气函数
from utils.file_util import save_to_json #导入保存文件函数
from utils.logger import get_logger #导入获取记录器函数
import argparse #支持命令行解析工具
logger=get_logger("Main") # 获取名为Main的主程序日志记录器
def main():
    parser=argparse.ArgumentParser(
        description="天气查询工具"
    )
    parser.add_argument(
        "--city",
        required=True,
        help="输入城市名称，例如：北京"
    )
    args=parser.parse_args()
    city_name=args.city
    logger.info("天气获取程序启动")
    weather_data=fetch_weather(city_name) #调用天气抓取函数
    if weather_data: #若成功获取数据，则调用保存函数写入文件
        filename=f"{city_name}_天气.json"
        save_to_json(weather_data,filename)
    else:
        logger.warning("未获取到天气数据")#记录警告级别的日志
    logger.info("程序运行结束") #记录程序正常结束的日志
if __name__ == "__main__": #判断当前脚本是否作为主程序直接运行
    main() #执行主函数