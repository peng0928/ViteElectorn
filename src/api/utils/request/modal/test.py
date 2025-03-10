import requests
def SunnyNetCreateRequest1():
    """
    [ /member/member/app/info ]
    本函数由SunnyNet网络中间件生成
    """
    url = "https://api.livelab.com.cn/member/member/app/info"
    payload = ""
    headers = {
        'host': "api.livelab.com.cn",
        'authorization': "Bearer eyJhbGciOiJIUzUxMiJ9.eyJjdCI6MTc0MTAxMjQzMjU3NiwibWlkIjoxNzU4ODA4NTcxMzc3NTg4MTMyLCJ0eXBlIjoiYXBwIiwiZGlkIjoiIiwia2V5IjoiTGl2ZUxhYjIwMjMifQ.ms7aH1po00KHSG0IWwF-GlSIOu4BNEskeugSDc410sNBgRXsk0RmTZ3TEZtE47MOSxIrA1zp0JIpj7X-Yr7z5Q",
        'platform-version': "3.3.1",
        'user-agent': "Dart/3.5 (dart:io)",
        'accept-encoding': "gzip",
        'platform-type': "android",
        'x-fwd-anonymousid': "",

    }
    response = requests.request("GET", url, data=payload, headers=headers)

    print(response.text)

SunnyNetCreateRequest1()