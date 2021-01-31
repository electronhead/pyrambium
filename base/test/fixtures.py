"""
pytest fixtures for unit testing
"""

import random
import asyncio
from typing import Optional, List
import pytest
import uvicorn
import app.main_temp as main_temp
from pyrambium.base.service.mothership import Mothership
from pyrambium.base.service.action import FileHeartbeat
from pyrambium.base.service.scheduler import TimelyScheduler
from pyrambium.base.service.continuous import Continuous

@pytest.fixture
def friends(tmp_path):
    """
    returns a tuple of useful test objects
    """
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
    """
    returns a random port number in case the unit test system runs test in parallel
    """
    return random.randint(5000,8000)

@pytest.fixture
def host():
    """
    the host used in unit tests
    """
    return '127.0.0.1'

@pytest.fixture
async def startup_and_shutdown_uvicorn(port, host):
    """
    This fixture starts a uvicorn server at first access of the fixture
    during the running of the test case and shuts down the uvicorn server
    upon exiting the test case function.
    """
    # from https://github.com/miguelgrinberg/python-socketio/issues/332
    class UvicornTestServer(uvicorn.Server):
        """Uvicorn test server

        Usage:
            @pytest.fixture
            async def start_stop_server():
                server = UvicornTestServer()
                await server.up()
                yield
                await server.down()
        """

        def __init__(self):
            """Create a Uvicorn test server
            Args:
                app (FastAPI, optional): the FastAPI app. Defaults to main.app.
                host (str, optional): the host ip. Defaults to '127.0.0.1'.
                port (int, optional): the port. Defaults to PORT.
            """
            self._startup_done = asyncio.Event()
            super().__init__(config=uvicorn.Config(app=main_temp, host=host, port=port))

        async def startup(self, sockets: Optional[List] = None) -> None:
            """Override uvicorn startup"""
            await super().startup(sockets=sockets)
            self.config.setup_event_loop()
            self._startup_done.set()

        async def up(self) -> None:
            """Start up server asynchronously"""
            self._serve_task = asyncio.create_task(self.serve())
            await self._startup_done.wait()

        async def down(self) -> None:
            """Shut down server asynchronously"""
            self.should_exit = True
            await self._serve_task

    server = UvicornTestServer()
    await server.up()
    yield
    await server.down()
