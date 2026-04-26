#实现多城市参数化测试，结合fixture来动态拦截并替换配置文件的读取
import pytest
from unittest.mock import patch #用于拦截和替换原有函数行为
from api.weather_api import fetch_weather #导入需测试的目标函数fetch_weather
import yaml #用于读取外部的yaml测试数据文件
import os
import allure #用于生成测试报告
from jsonschema import validate,ValidationError #导入schema校验核心函数和异常类

#定义接口schema图纸
WEATHER_SCHEMA={
    "type":"object",#最外层必须是一个字典（对象）
    #接口必须返回纬度、经度和当前天气信息
    "required":["latitude","longitude","current"],
    "properties":{
        "latitude":{"type":"number"},#纬度必须是数字
        "longitude":{"type":"number"},#经度必须是数字
        "current":{
            "type":"object",#current本身节点必须是一个字典
            "required":["temperature_2m"], #current里面必须包含温度字段
            "properties":{
                "temperature_2m":{"type":"number"}#温度必须是数字类型
            }
        }
    }
}
def read_yaml_data(yaml_path):
    #定义一个辅助函数，用来读取yaml文件并返回测试数据列表

    #拼接路径
    full_path=os.path.join(os.getcwd(),yaml_path)
    try:
        with open(full_path,'r',encoding='utf-8') as f:
            data=yaml.safe_load(f)#解析文件，转换为python字典或列表
            return data
    except Exception as e:
        print(f"读取测试数据文件失败：{e}")
        return [] #返回空列表，避免程序崩溃

#调用刚定义的函数读取weather_data.yaml中的数据
test_data=read_yaml_data('data/weather_data.yaml')

@pytest.fixture
def mock_config_generator():
    '''
    定义fixture工厂函数，动态生成不同城市的配置数据
    使得我们绕过真实的config.yaml文件，进行多城市测试
    '''
    #定义一个内部函数，接收经纬度参数
    def _generate(lat,lon):
        #返回一个字典，结构与yaml文件解析出的字典完全一致
        return {
            'api': {'base_url': "https://api.open-meteo.com/v1/forecast"},
            'city': {'lat': lat, 'lon': lon, 'timezone': "Asia/Shanghai"}
        }
    return _generate #将内部函数对象返回，供测试用例调用

#标记项目的最高层级：天气查询服务项目
@allure.epic('天气查询服务项目')
#标记当前测试文件所属的特性模块：核心API接口测试
@allure.feature("核心API接口测试")

#用parametrize装饰器进行数据驱动测试
#"data"是注入到测试函数的变量名，test_data是包含了字典的列表源数据
#运行时，pytest会自动遍历test_data,每次去除一个字典赋值给data参数
@pytest.mark.parametrize("data",test_data)
def test_weather_api(data,mock_config_generator):
    #测试fetch_weather函数能否正确处理不同城市的请求

    #从传入的字典data中提取当前循环城市名称
    city_name=data['city']
    #从传入的字典data中提取当前循环的纬度
    lat=data['lat']
    #从传入的字典data中提取当前循环的经度
    lon=data['lon']
    #动态设置测试用例标题
    allure.dynamic.title(f"获取城市天气数据 - {city_name}")
    #动态设置故事模块的名称
    allure.dynamic.story(f"查询{city_name}天气功能")

    #使用with allure.step记录测试的准备阶段
    with allure.step(f"步骤1：准备{city_name}的模拟配置数据(经度：{lon},纬度{lat})"):
        #生成当前城市的模拟配置字典
        mock_config_data=mock_config_generator(lat,lon)

    #使用patch拦截api.weather_api模块中的load_config函数
    #当fetch_weather内部调用load_config时，它不会读取文件，而是直接返回mock_config_data
    with patch('api.weather_api.load_config',return_value=mock_config_data):
        with allure.step("步骤2：调用fetch_weather接口发起网络请求"):
            #1.执行被测函数
            result=fetch_weather(city_name)
        with allure.step("步骤3：校验接口返回的数据结构和核心字段"):
            #2.核心断言：验证结果不为空
            assert result is not None,f"获取{city_name}天气数据失败，返回了None"
            #3.核心断言：验证返回的JSON数据中包含'current'核心字段
            assert 'current' in result,f"{city_name}的返回数据结构异常，缺少‘current’节点"
            #4.核心断言：验证温度数据存在
            assert 'temperature_2m' in result['current'],f"未获取到{city_name}的温度数据"
        with allure.step("步骤4：执行json schema结构强校验"):
            try:
                #使用顶部定义的schema图纸，强制校验实际返回的result结构
                validate(instance=result,schema=WEATHER_SCHEMA)
            except ValidationError as e:
                #若校验发现类型不对或少了字段，测试直接判为失败并输出原因
                pytest.fail(f"schema校验失败，原因：{e.message}")
        with allure.step("步骤5：校验接口返回的经纬度精度"):
            #5.用round保留一位小数对比断言返回的纬度与请求的纬度
            assert round(result['latitude'],1)==round(lat,1),f"{city_name}纬度数据不匹配"



