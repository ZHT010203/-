"""
接口测试主文件：
1：(传入数据库构造)从读取测试用例——》造数
2：(传入apiPath + 入参）——》登录——》接口查询返回信息——》接口测试
3：——》断言——》返回结果文件

当前主文件只需要进行2、3步，造数工作在前置文件包下。
"""


import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


from 前置.读取测试用例.test_读取测试用例 import read_excel

#读取测试用例，获得apiPath + 入参+预期结果,返回的是一个数组
def read_test_cases(test_case_path: str):
    """
    读取Excel文件
    :param file_path: 文件路径
    :return:
    """
    data = read_excel(test_case_path)
    #新建一个列表
    test_case_list = []
    #新建一个字典
    test_case_dict = {}
    #获取apiPath
    for i in data:
        test_case_dict["api_Path"] = i["Path"]
        test_case_dict["接口入参"] = i["接口入参"]
        test_case_dict["预期结果"] = i["预期结果"]
        test_case_list.append(test_case_dict)



    return data



#业务逻辑层，接口测试

#后置处理，断言



if __name__ == '__main__':
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"
    data = read_test_cases(test_case_path)
    print(data)






