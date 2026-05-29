import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import pymysql
from config import load_config


def connect_db():
    cfg = load_config()
    db = cfg["database"]
    conn = pymysql.connect(
        host=db["host"],
        user=db["user"],
        password=db["password"],
        database=db["database"]
    )
    return conn


#通过统计数据条数来验证连接的是不是对应的数据库，
# 别连接错误了，会违反权限
#当前是dmp_mock数据库hubei_mock表。
def main():
    conn = connect_db()
    cursor = conn.cursor()
    #执行sql语句，查询多少条数据
    sql = """
    select count(*) from hubei_mock
    """
    cursor.execute(sql)
    #获取查询结果
    result = cursor.fetchone()
    #打印查询结果
    print(result)

if __name__ == '__main__':
    main()

