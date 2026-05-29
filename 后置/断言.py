"""
得到接口返回结果
断言接口返回结果是否预期结果
"""

import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))



import json
from 后置.回写测试报告 import generate_report

def assert_api_response(response: dict, expected: dict):
    """
    断言接口返回结果是否符合预期
    :param response: test_api() 返回的完整响应（字典）
    :param expected:  预期结果字典，如 {"code": "0000", "msg": "查询成功"}
    """
    if expected is None:
        return  # 无预期结果，跳过断言

    # 真正的业务返回在 data.resultDetail 里，它是一个 JSON 字符串
    #返回接口访问后的内容
    result_detail_str = response["data"]["resultDetail"]
    if not result_detail_str:
        raise AssertionError(f"resultDetail为空，无法断言")
    #将str，注意，字典里面的{}json内容是一个str，需要转化为字典
    result_detail = json.loads(result_detail_str)

    #新建一个列表
    assert_results = []
    # 断言 code — 精确匹配
    if "code" in expected and "msg" in expected:
        actual_code = result_detail.get("code")
        assert_results.append(actual_code)
        assert actual_code == expected["code"]
    #断言msg是否包含预期结果
        actual_msg = result_detail.get("msg", "")
        assert_results.append(actual_msg)
        assert expected["msg"] in actual_msg
        #调用函数，将断言结果写入对应的测试用例文件中
        try:
            generate_report(actual_code, actual_msg)
        except Exception:
            pass  # 报告生成不影响断言结果









if __name__ == '__main__':
    assert_api_response()