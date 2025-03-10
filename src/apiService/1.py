import requests
def SunnyNetCreateRequest1():
    """
    [ /appShow/app/homepage/projects ]
    本函数由SunnyNet网络中间件生成    """
    url = "https://api.livelab.com.cn/appShow/app/homepage/projects"
    params = {
        "pageNum": "1",
        "pageSize": "100",
        "projectModuleId": "81", # 55 小岛热卖； 81 头部轮播
        "cityCode": "110100"
    }
    payload = ""
    headers = {
        'user-agent': "Dart/3.5 (dart:io)",
        'accept-encoding': "gzip",
        'platform-type': "android",
        'x-fwd-anonymousid': "d52b1f3e36d46ca0",
        'host': "api.livelab.com.cn",
        'platform-version': "3.3.1",

    }
    response = requests.request("GET", url, data=payload, headers=headers, params=params)

    print(response.text)


def get_goods():
    """
    [ /appShow/app/homepage/goods ]
    本函数由SunnyNet网络中间件生成
    """
    url = "https://api.livelab.com.cn/appShow/app/homepage/goods?goodsModuleId=83&v=0"
    payload = ""
    headers = {
        'platform-type': "android",
        'x-fwd-anonymousid': "d52b1f3e36d46ca0",
        'host': "api.livelab.com.cn",
        'platform-version': "3.3.1",
        'user-agent': "Dart/3.5 (dart:io)",
        'accept-encoding': "gzip",

    }
    response = requests.request("GET", url, data=payload, headers=headers)

    print(response.text)

def banners():
    """
    [ /appShow/app/homepage/banners ]
    本函数由SunnyNet网络中间件生成
    """
    url = "https://api.livelab.com.cn/appShow/app/homepage/banners?bannerModuleId=52"
    payload = ""
    headers = {
        'x-fwd-anonymousid': "d52b1f3e36d46ca0",
        'host': "api.livelab.com.cn",
        'platform-version': "3.3.1",
        'user-agent': "Dart/3.5 (dart:io)",
        'accept-encoding': "gzip",
        'platform-type': "android",

    }
    response = requests.request("GET", url, data=payload, headers=headers)

    print(response.text)

if __name__ == '__main__':
    banners()