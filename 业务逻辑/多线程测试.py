

import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

@pytest.mark.parametrize("a,b,c", [(1,2,3),(4,5,9),(7,8,15)])
def test_multi_thread(a,b,c):
    """
    多线程测试
    :param thread_count: 线程数量
    :return:
    """
    # 测试代码
    assert a+b+c == c
    return a+b+c


def main():
    """
    主函数
    :return:
    """
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = {
            executor.submit(test_multi_thread, a, b, c): (a, b, c)
            for a, b, c in [(1,2,3),(4,5,9),(7,8,15)]
        }

        for future in as_completed(future):
            result = future.result()
            print(result)
            

    
