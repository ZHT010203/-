

"""
接口信息查询，获取对应的信息
两套查询思维
1：直接传入apiPath，返回id
2：传入id，返回接口信息
"""
import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


import requests
from 业务逻辑.登录 import login

#查询接口信息,返回id
def query_api_info(api_path: str, api_type_code: str = "", page_num: int = 1, page_size: int = 10):
    """
    查询接口信息
    :param api_path: 接口路径
    :param api_type_code: 接口类型编码（默认空）
    :param page_num: 页码
    :param page_size: 每页条数
    :return: [id, code] 列表
    """
    api_token = login()
    url = "http://dmp.zdsoft.local/masterapi/dpp/jobflowmaster/interface/pageList"
    headers = {
        "access-token": api_token,
        "app-code": "Index-Platform-PC",
        "Content-Type": "application/json",
        "referer": "http://dmp.zdsoft.local/"
    }
    body = {
        "apiTypeCode": api_type_code,
        "apiPath": api_path,
        "pageNum": page_num,
        "pageSize": page_size
    }
    #调用函数通过id查询接口信息
    responseId01 = requests.post(url, headers=headers, json=body)
    #获取id
    id = responseId01.json()["data"]["records"][0]["id"]
    #调用函数：通过函数来传入id，获取接口信息
    api_info = query_api_info_by_id(id, api_token)
    return api_info



#通过id查询接口信息，返回接口信息
def query_api_info_by_id(api_id: str, api_token: str = ""):
    """
    查询接口信息
    :param api_id: 接口id
    :return: 接口信息字典   
    """
    url = "http://dmp.zdsoft.local/masterapi/dpp/jobflowmaster/interface/viewDetailById"
    headers = {
        "access-token": api_token,
        "app-code": "Index-Platform-PC",
        "Content-Type": "application/json",
        "referer": "http://dmp.zdsoft.local/"
    }
    body = {
        "id": api_id
    }
    response = requests.get(url, headers=headers, params=body)
    return response.json()


if __name__ == "__main__":
    api_path = "/taskApi/openapiv3/essentialInfo/commercialRegInfo"
    api_info = query_api_info(api_path)
    print(api_info)

