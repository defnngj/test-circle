import os
import pytest

# 定义目录
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "test_dir")
REPORT_DIR = os.path.join(BASE_DIR, "test_report")


if __name__ == '__main__':
    report_file = os.path.join(REPORT_DIR, "result.html")
    pytest.main([
        "-n", "2",  # 设置2个线程
        "-v", "-s", TEST_DIR,
        "--html=" + report_file,
        ])
