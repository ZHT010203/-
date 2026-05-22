
#解决导入路径找不到的问题
import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import requests
import json

from 业务逻辑.登录 import login
from 业务逻辑.接口查询 import query_api_info


def test_api(api_path: str, input_params: dict):
    """
    参数化接口测试：只需传入 apiPath + 入参，自动查询接口信息并测试
    :param api_path: 接口路径，如 "/taskApi/openapiv3/essentialInfo/commercialRegInfo"
    :param input_params: 入参字典，如 {"keyword": "k000000n6666620"}
    :return: 接口测试结果
    """
    # 第1步：通过 apiPath 查询接口信息（自动获取 id、bodyData、headData、queryData）
    api_info = query_api_info(api_path)
    api_data = api_info["data"]

    # 第2步：登录拿 token
    token = login()

    # 第3步：构造接口测试请求
    url = "http://dmp.zdsoft.local/masterapi/dpp/jobflowmaster/interface/test"
    # 构造请求头
    headers = {
        "access-token": token,
        "app-code": "Index-Platform-PC",
        "referer": "http://dmp.zdsoft.local/"
    }
    """
    构造入参
    """
    # 从接口查询结果中提取 bodyData 模板，转成 {"参数名": "参数值"} 的简单字典
    body_data_list = json.loads(api_data["bodyData"])
    body_data_dict = {}

    for param in body_data_list:
        param_name = param["paramName"]
        # 如果用户传了这个参数，就用用户的值；否则用默认值
        if param_name in input_params:
            body_data_dict[param_name] = input_params[param_name]
        else:
            body_data_dict[param_name] = param.get("paramDefaultValue", "")

    # 从接口查询结果中提取 headData 和 queryData，直接透传
    #关于head_data的处理，不用处理，直接json化就行了，因为就需要这个完整的。
    head_data = json.loads(api_data["headData"]) if api_data["headData"] else []
    #关于query_data的处理，不用处理，直接json化就行了，因为就需要这个完整的。
    query_data = json.loads(api_data["queryData"]) if api_data["queryData"] else []

    # 构造最终请求体
    body = {
        "id": api_data["id"],
        "envCode": "TEST",
        "bodyData": json.dumps(body_data_dict, ensure_ascii=False),
        "queryData": query_data,
        "headData": head_data
    }

    # 第4步：发送请求
    response = requests.post(url, headers=headers, json=body)
    return response.json()


if __name__ == "__main__":
    # 只需要传 apiPath + 入参，就能自动跑通！
    result = test_api(
        api_path="/taskApi/openapiv3/essentialInfo/commercialRegInfo",
        input_params={
  "keyword": "k000000n6666620",
  "requestld": "",
  "dfTraceld": "",
  "calld": ""
}
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
