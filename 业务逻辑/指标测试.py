"""
指标测试
"""
import requests
import json

from 业务逻辑.登录 import login
from 业务逻辑.查询指标 import query

#指标测试
def test_index():
    """只登录一次，拿到Token"""
    token = login()

    """用同一个Token查指标,
    相当于，1：先查询，获得入参的一些参数，
           2：将参数转化为变量，在进行指标测试
           3：期间，tokne共用，函数“指标测试”里面调用“查询指标”的函数
    """
    jieguo = query("26c0efad87124e408de77d05cf2d99ba", token)
    #从指标信息中获取指标名称、指标版本、指标收集方法、指标版本编码、工作流编码
    indexName = jieguo["indexName"]
    indexVersion = jieguo["indexVersion"]
    indexCollectMethod = jieguo["indexCollectMethod"]
    indexVersionCode = jieguo["indexVersionCode"]
    workflowUniqueCode = jieguo["workflowUniqueCode"]
    """获取传入参数"""
    params = {
        "taxNo": "0",
        "uscCode": "0",
        "refreshcache": "true",
        "appId": "0"
    }

    #接口访问
    """
    接口访问
    """
    url = "http://dmp.zdsoft.local/masterapi/dpp/jobflowmaster/index/testexecute?_=wgxq"
    headers = {
        "access-token": token,
        "app-code": "Index-Platform-PC",
        "referer": "http://dmp.zdsoft.local/"
    }

    body = {
        "indexCollectMethod": indexCollectMethod,
        "indexName": indexName,
        "indexVersion": indexVersion,
        "indexVersionCode": indexVersionCode,
        "params": params,
        #固定的测试环境，不能改变
        "runEnv": "TEST",
        "workflowUniqueCode": workflowUniqueCode
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

if __name__ == "__main__":
    jieguo = test_index()
    print(jieguo)

