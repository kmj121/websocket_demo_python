import sys

class Config:
    default_value = {
        "HOST": "0.0.0.0",
        "PORT": 8080,
        # "DSN": "https://88e518eb955c4ba3adacbc555e3c2512@sentry.17zhiliao.work/23",
        # "MONGO_URL": "s-uf64f793dee47174-pub.mongodb.rds.aliyuncs.com:3717,"
        #              "s-uf65765f25729864-pub.mongodb.rds.aliyuncs.com:3717",
        # "MONGO_USER": "newtest",
        # "MONGO_PWD": "ewezx17B",
        # "MYSQL_URL": "rm-uf6b86bk27h834tnpxo.mysql.rds.aliyuncs.com:3306",
        # "MYSQL_USER": "root",
        # "MYSQL_PWD": "root",
        # "MQ_URL": '47.111.30.45:9093,47.96.73.148:9093,47.110.148.101:9093',
        # "MQ_USER": "alikafka_pre-cn-0pp10aqvl007",
        # "MQ_PWD": "N8g1D6ojxfvFqafQfeMv5tv07qRWmH0Z",
        # "ENV": "local",
        # "TOKEN": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1Yzc4ZmZlZjEyYzVjMWUxMmJkN2RmYzAiLCJub25jZSI6IjIxMzgiLCJyb2xlIjoiUFJPRFVDRVIifQ.bVFPwvNodj1QtqFONsh0Rz4g266z5gGOdKd_mk4-3NBr9evDVIkayyzPt8xlmF8mQxXXovqFo_ApfFsiBua9KljhJn1OPpDrKubPuzLpkr-ihC_q5nYQwthaCPfNLaGRr4BeMS3dUNJmDSPJVBiumC9BSVhKavIHRZDkQZ0NkZwSaDmPIhuYta53NvHzF11GA5VOb7Htz0ztlbn2SfvgyG9ZLTM0UWNDQftCwaSya78xfvlgYS2GiMmP_31AQVimTQRrQq1hiETn1UUawl2m86XIaosuz36nDvg6J6H2cR7LIgbbCN_POvcGRYPz3AP9q-1P1NDra44ZcYoPZnJc4w"
    }

    def __init__(self):
        for i in self.default_value:
            self.__setattr__(i, self.default_value[i])

        for i in sys.argv:
            if "=" in i:
                k = i.split("=")[0].upper()
                v = i.split("=")[1]
                if v not in (None, ''):
                    self.__setattr__(k, v)

        self.__setattr__("static_grant_version", "2.0")


config = Config()

def set_static_grant_version(grant_version):
    config.__setattr__("static_grant_version", grant_version)


def get_static_grant_version():
    return config.__getattribute__("static_grant_version")
