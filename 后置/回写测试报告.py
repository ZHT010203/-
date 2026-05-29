import shutil
from pathlib import Path

# 定义项目根目录（这里假设脚本在“后置”文件夹内，根目录是其父目录）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

def generate_report(actual_code, actual_msg, test_case_path: str):
    # 这里也建议把 test_case_path 转成 Path 对象，方便操作
    tc_path = Path(test_case_path)
    report_dir = _PROJECT_ROOT / "测试报告" / tc_path.name
    if not report_dir.exists():
        report_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(tc_path, report_dir / tc_path.name)
    # 注意：你原本的断言结果文件应该是想写入内容，而不是直接复制原文件吧？
    # 这里先保留你的写法，但你可能需要调整
    shutil.copy(tc_path, report_dir / f"{tc_path.stem}_断言结果.txt")

if __name__ == '__main__':
    test_case_path = r"C:\Users\Administrator\Desktop\项目代码\试一试\数宜信平台登录\测试用例\666.xlsx"
    generate_report("0000", "查询成功", test_case_path)

