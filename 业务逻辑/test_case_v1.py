"""
接口测试主文件（并发版）：
1：(传入数据库构造)从读取测试用例——》造数
2：(传入apiPath + 入参）——》登录——》接口查询返回信息——》接口测试
3：——》断言——》返回结果文件

使用线程池（ThreadPoolExecutor）实现多接口并行执行。
"""

import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from 前置.读取测试用例.test_读取测试用例 import read_excel
from 业务逻辑.接口测试 import test_api
from 后置.断言 import assert_api_response

# ==================== 线程安全的统计 ====================
_lock = threading.Lock()
_stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}


def run_single_case(case, index):
    """
    执行单条测试用例（线程安全，可被多线程同时调用）
    """
    path = case["Path"]
    params = json.loads(case["接口入参"])

    # 预期结果处理
    raw_expected = case["预期结果"]
    if not isinstance(raw_expected, str):
        expected = None
    else:
        expected = json.loads(raw_expected)

    status = ""
    error_msg = ""

    try:
        response = test_api(path, params)
        if expected is None:
            status = "跳过"
        else:
            assert_api_response(response, expected)
            status = "通过"
    except Exception as e:
        status = "失败"
        error_msg = str(e)

    # 线程安全计数
    with _lock:
        _stats["total"] += 1
        if status == "通过":
            _stats["passed"] += 1
        elif status == "失败":
            _stats["failed"] += 1
        else:
            _stats["skipped"] += 1

    return {
        "index": index,
        "path": path,
        "params": params,
        "status": status,
        "error": error_msg,
    }


def main():
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"
    data = read_excel(test_case_path)

    # ===== 核心：并发数，改这个数字就行 =====
    max_workers = 5  # 同时跑5条用例

    print(f"共 {len(data)} 条用例，启动 {max_workers} 个线程并发执行...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        # 一次性提交所有任务
        futures = {
            pool.submit(run_single_case, case, i): i
            for i, case in enumerate(data, 1)
        }
        # 谁先完成就先输出谁
        for future in as_completed(futures):
            result = future.result()
            icon = {"通过": "✅", "失败": "❌", "跳过": "⏭"}.get(result["status"], "?")
            print(f"【用例 {result['index']:>2}】{result['path']} {icon} {result['status']}")
            if result["error"]:
                print(f"        错误: {result['error']}")

    print(f"\n{'='*50}")
    print(f"总计: {_stats['total']} | 通过: {_stats['passed']} | 失败: {_stats['failed']} | 跳过: {_stats['skipped']}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()