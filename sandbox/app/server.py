from fastapi import FastAPI
import asyncio
import uvicorn
from typing import Optional, List

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

    def __init__(self, app: FastAPI, host: str, port: int):
        """Create a Uvicorn test server

        Args:
            app (FastAPI): the FastAPI app.
            host (str): the host ip.
            port (int): the port.
        """
        self._startup_done = asyncio.Event()
        super().__init__(config=uvicorn.Config(app, host=host, port=port, workers=1))

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