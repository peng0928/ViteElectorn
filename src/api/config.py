class AppSettings:
    dev = {
        "redis": {
            "host": "localhost",
            "port": 6379,
            "password": "",
            "db": 8
        },
        "mongo": {
            "host": "localhost",
            "port": 27017,
            "db": "YP",
            "log": True,
        },
    }


class MongoConfig:
    fwd_task = "Fwd-tasks"
    fwd_task_log = "Fwd-tasks-logs"


class RedisConfig:
    fwd_task = "tasks:fwd"


class DBConfig:
    mongo = MongoConfig()
    redis = RedisConfig()
