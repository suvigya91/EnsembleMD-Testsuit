# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="type1",
        help="my option: xsede.stampede or local.localhost")

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
