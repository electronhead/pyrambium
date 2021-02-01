import pytest
from .. import main
from .. import server

@pytest.fixture
def port():
    """
    returns the port number used in uvicorn unit testing
    """
    return 5000

@pytest.fixture
def host():
    """
    returns the host used in uvicorn unit testing
    """
    return '127.0.0.1'

@pytest.fixture
async def startup_and_shutdown_uvicorn(host, port):
    """Start server as test fixture and tear down after test"""
    uvicorn_server = server.UvicornTestServer(app=main.app, host=host, port=port)
    await uvicorn_server.up()
    yield
    await uvicorn_server.down()