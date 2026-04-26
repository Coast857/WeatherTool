import os
import pytest

@pytest.fixture(scope="session",autouse=True)
def set_env():
    """
    自动设置测试环境为test
    """
    os.environ["ENV"]="test"