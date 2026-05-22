"""
测试：读取测试用例模块
验证能否正确从 Excel 中读取测试用例数据
"""
import pytest
import json
import pandas as pd


def read_excel(test_case_path: str):
    """
    读取Excel文件
    :param file_path: 文件路径
    :return:
    """
    data = pd.read_excel(test_case_path)
    #创建一个空列表
    test_case_list = []
    #循环读取每一行内容
    for index, row in data.iterrows():
        #每次循环创建一个新字典
        test_case_dict = {}
        test_case_dict["Path"] = row["Path"]
        test_case_dict["接口入参"] = row["接口入参"]
        test_case_dict["预期结果"] = row["预期结果"]
        test_case_dict["数据库造数构造"] = row["数据库造数构造"]
        test_case_list.append(test_case_dict)
    return test_case_list
    


#测试读取后的测试用例效果
if __name__ == '__main__':
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"
    data = read_excel(test_case_path)

    for idx, case in enumerate(data, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 #{idx}")
        print(f"{'='*60}")
        for key, val in case.items():
            if '数据库造数构造' in key and isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    print(f"{key}:")
                    print(json.dumps(parsed, indent=2, ensure_ascii=False))
                except:
                    print(f"{key}: {val}")
            else:
                print(f"{key}: {val}")
    