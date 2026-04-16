# 业务接口模块
# 将网络请求逻辑改为使用RequestUtil统一管理
import yaml  # 导入yaml解析库
import os  # 导入os模块
from utils.logger import get_logger  # 导入日志模块
from utils.request_util import RequestUtil  # 导入请求工具类

# 初始化日志
logger = get_logger(__name__)
# 创建请求工具实例
request_util = RequestUtil()

def load_config(config_path='config/config.yaml'):
    try:

        # 打开配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            # 解析YAML并返回字典
            return yaml.safe_load(f)

    except Exception as e:
        # 记录错误日志
        logger.error(f"读取配置文件失败:{e}")
        return None
def fetch_weather():

    #获取天气数据（核心业务函数）
    # 加载配置
    config = load_config()
    # 判断配置是否成功加载
    if not config:
        logger.error("配置文件不存在或为空")
        return None
    # 获取api配置
    api_config = config.get('api')
    # 检查是否是字典
    if not isinstance(api_config, dict):
        logger.error(
            "配置文件结构错误：'api'节点不是字典"
        )
        return None
    # 获取city配置
    city_config = config.get('city')
    if not isinstance(city_config, dict):
        logger.error(
            "配置文件结构错误：'city'节点不是字典"
        )
        return None
    # 获取URL
    base_url = api_config['base_url']
    # 获取城市信息
    lat = city_config['lat']
    lon = city_config['lon']
    timezone = city_config['timezone']
    # 构建请求参数
    params = {

        "latitude": lat,

        "longitude": lon,

        "current":
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m,"
            "wind_direction_10m",

        "timezone": timezone
    }

    try:

        # 打印请求日志
        logger.info(
            f"开始请求天气数据: ({lat},{lon})"
        )
        # 使用RequestUtil发送请求（核心升级点）
        data = request_util.send_request(
            method="GET",
            url=base_url,
            params=params,
            timeout=5,
            retry=3
        )

        # 判断是否成功
        if not data:
            logger.error("未获取到天气数据")
            return None
        # 提取current字段
        current = data.get('current', {})
        # 打印天气信息
        logger.info(
            f"当前温度：{current.get('temperature_2m')}℃"
        )
        logger.info(
            f"体感温度：{current.get('apparent_temperature')}℃"
        )
        logger.info(
            f"湿度：{current.get('relative_humidity_2m')}%"
        )
        logger.info(
            f"降水量：{current.get('precipitation')}mm"
        )
        return data
    except Exception as e:
        logger.error(
            f"天气获取失败: {e}"
        )
        return None