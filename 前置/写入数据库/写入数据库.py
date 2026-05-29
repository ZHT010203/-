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


##第二代版本
#1：批量执行sql语句
#2：防止sql注入风险，%解决

def write_db(test_case_path: str):
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
    data = read_excel(test_case_path)  
    #循环读取数据每一个键值对
    #新建一个列表
    params_list = []
    for itim in data:
        #新建一个字典
        params = {}
        #获取第一个字典的数据内容
        Path = itim["Path"]
        mock_data = itim["数据库造数构造"]
        api_params = itim["接口入参"]
        api_params = json.loads(api_params)
        #获取接口入参当中的关键api_keyword
        api_keyword = api_params["keyword"]
        #把path添加到字典中
        params["Path"] = Path
        #把api_keyword添加到字典中
        params["api_keyword"] = api_keyword
        #把mock_data添加到字典中
        params["mock_data"] = mock_data
        #把字典添加到列表中
        params_list.append(params)



    #执行sql语句
    sql = """
    insert into hubei_mock(api_path,api_keyword,mock_data)
    values(%(Path)s,%(api_keyword)s,%(mock_data)s)
    """
    #执行sql语句
    cursor.executemany(sql, params_list)
    #提交事务
    conn.commit()

    #关闭数据库连接
    cursor.close()
    conn.close()
    



if __name__ == '__main__':
    #测试用例路径
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"
    #调用写入数据库函数
    write_db(test_case_path)
    print("写入数据库完成")