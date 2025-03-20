import hashlib
from datetime import datetime


def md5(text: str):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def get_time(f="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(f)
