'''
Author: Derry
Email: drlv@stu.xidian.edu.cn
Date: 2021-01-27 21:37:47
LastEditors: Derry
LastEditTime: 2021-01-31 13:38:54
Description: 爬取车站名称和车站代码的对应表，并存储为json格式
'''

import re
import json
import requests

def load_station():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9163"
    # requests模块在访问HTTPS网站时，如果设置移除SSL认证参数“verify=False”，执行代码是会提示“InsecureRequestWarning”警告，再请求页面时加入此段代码可以屏蔽掉警告信息
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, verify=False) # 请求12306所有城市的拼音和代号网页
    result = re.findall(r"([\u4e00-\u9fa5]+)\|([A-Z]+)", r.text) # 正则匹配车站中文名和英文编号对应的数据
    stations = dict(result) # 将获取的数据转成字典
    stations['济 南'] = 'EEI'
    stations['福州 南'] = 'FXS'
    with open('station_info.json', 'w', encoding='utf-8') as f:
        json.dump(stations, f, ensure_ascii=False, indent=4)
    return stations


if __name__ == '__main__':
    load_station()
