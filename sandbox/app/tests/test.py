import pytest
from .fixtures import port, host, startup_and_shutdown_uvicorn
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_uvicorn(startup_and_shutdown_uvicorn, port, host):
    """
    test to see if uvicorn responds to http requests inside the function
    """

    async with AsyncClient(base_url=f"http://{host}:{port}/") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert 'FastAPI app started' in response.json()