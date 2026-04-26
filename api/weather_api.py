# api/weather_api.py
import yaml  # 解析yaml配置文件
import os  # 读取环境变量
from utils.logger import get_logger  # 导入日志工具
from utils.request_util import RequestUtil  # 导入请求工具

#初始化日志
logger = get_logger(__name__)

# 初始化请求工具
request_util = RequestUtil()

def load_config():
    """
    根据环境变量加载对应的配置文件

    ENV=dev → dev.yaml
    ENV=test → test.yaml
    ENV=prod → prod.yaml
    """

    try:
        # 获取环境变量ENV
        # 如果没有设置，默认使用dev环境
        env = os.getenv("ENV", "dev")

        # 构建配置文件路径
        config_path = f"config/{env}.yaml"

        logger.info(f"加载配置文件: {config_path}")

        # 打开配置文件
        with open(config_path, "r", encoding="utf-8") as f:

            # 解析yaml
            config = yaml.safe_load(f)

            return config

    except Exception as e:

        logger.error(f"读取配置文件失败: {e}")

        return None


def fetch_weather(city_name):
    """
    获取指定城市天气

    city_name: 城市名称（北京/上海等）
    """

    config = load_config()

    if not config:
        logger.error("配置加载失败")
        return None

    try:

        # 获取API配置
        api_config = config.get("api")

        # 获取城市配置
        city_dict = config.get("city")

        timezone = config.get("timezone")

        # 检查城市是否存在
        if city_name not in city_dict:

            logger.error(f"未找到城市配置: {city_name}")

            return None

        # 获取城市经纬度
        lat = city_dict[city_name]["lat"]

        lon = city_dict[city_name]["lon"]

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

        logger.info(
            f"开始请求 {city_name} 天气 ({lat},{lon})"
        )

        # 调用请求工具
        data = request_util.send_request(

            method="GET",

            url=api_config["base_url"],

            params=params,

            timeout=5,

            retry=3

        )

        if not data:

            logger.error("未获取到天气数据")

            return None

        current = data.get("current", {})

        logger.info(
            f"{city_name} 当前温度：{current.get('temperature_2m')}℃"
        )

        return data

    except Exception as e:

        logger.error(f"天气获取失败: {e}")

        return None