"""
写入数据库的运行主文件
"""

import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from 连接数据库 import connect_db
from 前置.读取测试用例.test_读取测试用例 import read_excel
import json



def write_db():
    """
    写入数据库
    :param data: 要写入的数据
    :return:
    """
    #创建数据库对象
    conn = connect_db()
    #创建游标
    cursor = conn.cursor()
    #获取数据,返回的是[{},{}]
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"   
    data = read_excel(test_case_path)  
    #循环读取数据每一个键值对
    for itim in data:
        #获取第一个字典的数据内容
        Path = itim["Path"]
        mock_data = itim["数据库造数构造"]
        api_params = itim["接口入参"]
        api_params = json.loads(api_params)
        #获取接口入参当中的关键api_keyword
        api_keyword = api_params["keyword"]
        #执行sql语句
        sql = f"""
        insert into hubei_mock_001(api_path,api_keyword,mock_data)
        values('{Path}','{api_keyword}','{mock_data}')
        """
        #执行sql语句
        cursor.execute(sql)
        #提交事务
        conn.commit()

    #关闭数据库连接
    cursor.close()


if __name__ == '__main__':
    write_db()
    print("写入数据库完成")