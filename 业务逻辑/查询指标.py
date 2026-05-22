"""
查询指标
"""
import requests
import json

from 业务逻辑.登录 import login

def query(indexVersionCode, token=None):
    #加入token参数没有，默认token为空，并且调用登录函数获取token
    if token is None:
        token = login()

    url = "http://dmp.zdsoft.local/masterapi/dpp/jobflowmaster/index/report"
    headers = {
        "access-token": token,
        "app-code": "Index-Platform-PC",
        "referer": "http://dmp.zdsoft.local/"
    }
    #指标编码
    params = {
        "indexVersionCode": indexVersionCode
    }
    response = requests.get(url, headers=headers, params=params)
    #赋值给变量
    jieguo = response.json()
    #创建一个字典
    data = {}
    #判断是否成功
    if jieguo.get("code") == "200" and jieguo["data"].get("indexInfo"):
        #获取指标信息
        info = jieguo["data"]["indexInfo"]
        indexName = info['indexName']
        indexCode = info['indexCode']
        indexVersion = info['indexVersion']
        indexCollectMethod = info['indexCollectMethod']
        indexVersionCode = info['indexVersionCode']
        workflowUniqueCode = info['workflowUniqueCode']
        #添加到字典
        data["indexName"] = indexName
        data["indexVersion"] = indexVersion
        data["indexCollectMethod"] = indexCollectMethod
        data["indexVersionCode"] = indexVersionCode
        data["workflowUniqueCode"] = workflowUniqueCode
    #返回字典
    return data



if __name__ == "__main__":
    jieguo = query("26c0efad87124e408de77d05cf2d99ba")
    print(jieguo)
    










