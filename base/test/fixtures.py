"""
pytest fixtures for unit testing
"""

import random
import pytest
from pyrambium.base.service.mothership import Mothership
from pyrambium.base.service.action import FileHeartbeat
from pyrambium.base.service.scheduler import TimelyScheduler
from pyrambium.base.service.continuous import Continuous
from pyrambium.base.test.server import UvicornTestServer
from pyrambium.app import main_temp

@pytest.fixture
def friends(tmp_path):
    """ returns a tuple of useful test objects """
    def stuff():
        # want a fresh tuple from the fixture
        saved_dir = str(tmp_path)
        output_file = str(tmp_path / 'output.txt')
        mothership = Mothership(saved_dir=saved_dir)
        mothership.set_continuous(Continuous())
        action = FileHeartbeat(file=output_file)
        scheduler = TimelyScheduler(interval=1)

        return mothership, scheduler, action
    return stuff

@pytest.fixture
def port():
    """ returns a random port number in case the unit test system runs test in parallel """
    return random.randint(5001,7999)

@pytest.fixture
def host():
    """ the host used in unit tests """
    return '127.0.0.1'

@pytest.fixture
async def startup_and_shutdown_uvicorn(host, port):
    """Start server as test fixture and tear down after test"""
    uvicorn_server = UvicornTestServer(app=main_temp.app, host=host, port=port)
    await uvicorn_server.up()
    yield
    await uvicorn_server.down()

@pytest.fixture
def base_url(host, port):
    """ base url for unit test invocation of api """
    return f"http://{host}:{port}"