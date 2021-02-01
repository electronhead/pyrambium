"""
These test cases run the API within each test function call, allowing API http calls
to a live and albeit short-lived Pyrambium server.

This class and the fixture, startup_and_shutdown_uvicorn rely on asynchronous processing.

Notes:

1. Running all test cases at the same time sometimes results in failures in some of the
test functions in this class. They succeed when run individually. Something to fix perhaps.
"""
import time
import pytest
from pyrambium.base.service.action import FileHeartbeat, Action
from pyrambium.base.service.scheduler import TimelyScheduler, Scheduler
from pyrambium.base.service.util import FilePathe, ResolveBody
from pyrambium.app.workbench import ApiHost
from pyrambium.base.test.fixtures import port, host, startup_and_shutdown_uvicorn
from pydantic import BaseModel
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_uvicorn_1(startup_and_shutdown_uvicorn, port, host):
    """
    test to see if uvicorn responds to http requests inside the function
    """
    async with AsyncClient(base_url=f"http://{host}:{port}/") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == 'Pyrambium API server started (unit test)'

@pytest.mark.asyncio
async def test_uvicorn_2(startup_and_shutdown_uvicorn, port, host, tmp_path):
    """
    first N lines of test_uvicorn_3
    """
    base_url = compute_base_url(host, port)
    output_file = str(tmp_path / 'output.txt')
    xtra={'port':port, 'ip_addr': host}
    action = FileHeartbeat(file=output_file, xtra=xtra)
    scheduler = TimelyScheduler(interval=1)

    saved_dir = FilePathe(path=str(tmp_path))
    response = await put(base_url=base_url, path='/mothership/saved_dir', data=saved_dir)
    assert response.status_code == 200, 'failed to set saved_dir'
    response = await get(base_url=base_url, path='/mothership/saved_dir')
    assert response.status_code == 200, 'failed to get saved_dir'
    saved_saved_dir = ResolveBody(FilePathe)(response.json())
    assert saved_saved_dir == saved_dir
    
    response = await get(base_url=base_url, path='/mothership/clear')
    assert response.status_code == 200, 'failed to get clear mothership'
    response = await get(base_url=base_url, path='/jobs/stop') # likely already stopped

    response = await put(base_url=base_url, path='/actions/foo', data=action)
    assert response.status_code == 200, f"failed to put action (foo)"
    response = await get(base_url, path='/actions/foo')
    assert response.status_code == 200, f"failed to get action (foo)"
    retrieved_action = ResolveBody(Action)(response.json())
    assert isinstance(retrieved_action, Action), str(type(retrieved_action))

    response = await put(base_url=base_url, path='/schedulers/bar', data=scheduler)
    assert response.status_code == 200, f"failed to put scheduler (bar)"
    response = await get(base_url, path='/schedulers/bar')
    assert response.status_code == 200, f"failed to get scheduler (bar)"
    retrieved_scheduler = ResolveBody(Scheduler)(response.json())
    assert isinstance(retrieved_scheduler, Scheduler), str(type(retrieved_scheduler))

@pytest.mark.asyncio
async def test_uvicorn_3(startup_and_shutdown_uvicorn, port, host, tmp_path):
    """
    first N lines of test_uvicorn_4
    """
    base_url = compute_base_url(host, port)
    output_file = str(tmp_path / 'output.txt')
    xtra={'port':port, 'ip_addr': host}
    action = FileHeartbeat(file=output_file, xtra=xtra)
    scheduler = TimelyScheduler(interval=1)

    saved_dir = FilePathe(path=str(tmp_path))
    response = await put(base_url=base_url, path='/mothership/saved_dir', data=saved_dir)
    assert response.status_code == 200, 'failed to set saved_dir'
    response = await get(base_url=base_url, path='/mothership/saved_dir')
    assert response.status_code == 200, 'failed to get saved_dir'
    saved_saved_dir = ResolveBody(FilePathe)(response.json())
    assert saved_saved_dir == saved_dir

    response = await get(base_url=base_url, path='/mothership/clear')
    assert response.status_code == 200, 'failed to get clear mothership'
    response = await get(base_url=base_url, path='/jobs/stop') # likely already stopped

    response = await put(base_url=base_url, path='/actions/foo', data=action)
    assert response.status_code == 200, f"failed to put action (foo)"
    response = await get(base_url, path='/actions/foo')
    assert response.status_code == 200, f"failed to get action (foo)"
    retrieved_action = ResolveBody(Action)(response.json())
    assert isinstance(retrieved_action, Action), str(type(retrieved_action))

    response = await put(base_url=base_url, path='/schedulers/bar', data=scheduler)
    assert response.status_code == 200, f"failed to put scheduler (bar)"
    response = await get(base_url, path='/schedulers/bar')
    assert response.status_code == 200, f"failed to get scheduler (bar)"
    retrieved_scheduler = ResolveBody(Scheduler)(response.json())
    assert isinstance(retrieved_scheduler, Scheduler), str(type(retrieved_scheduler))

    response = await get(base_url=base_url, path='/schedulers/bar/actions/foo')
    assert response.status_code == 200, f"failed to schedule action (foo) using scheduler (bar)"

    response = await get(base_url, '/jobs/count')
    assert response.status_code == 200, 'failed to retrieve job count'
    job_count = response.json()['job_count']
    assert job_count == 1, 'expecting a job count of 1'

@pytest.mark.asyncio
async def test_uvicorn_4(startup_and_shutdown_uvicorn, port, host, tmp_path):
    """
    tests the scheduling and running of a FileHeartbeat
    """
    base_url = compute_base_url(host, port)
    output_file = str(tmp_path / 'output.txt')
    xtra={'port':port, 'ip_addr': host}
    action = FileHeartbeat(file=output_file, xtra=xtra)
    scheduler = TimelyScheduler(interval=1)

    saved_dir = FilePathe(path=str(tmp_path))
    response = await put(base_url=base_url, path='/mothership/saved_dir', data=saved_dir)
    assert response.status_code == 200, 'failed to set saved_dir'
    response = await get(base_url=base_url, path='/mothership/saved_dir')
    assert response.status_code == 200, 'failed to get saved_dir'
    saved_saved_dir = ResolveBody(FilePathe)(response.json())
    assert saved_saved_dir == saved_dir
    
    response = await get(base_url=base_url, path='/mothership/clear')
    assert response.status_code == 200, 'failed to get clear mothership'
    response = await get(base_url=base_url, path='/jobs/stop') # likely already stopped

    response = await put(base_url=base_url, path='/actions/foo', data=action)
    assert response.status_code == 200, f"failed to put action (foo)"
    response = await get(base_url, path='/actions/foo')
    assert response.status_code == 200, f"failed to get action (foo)"
    retrieved_action = ResolveBody(Action)(response.json())
    assert isinstance(retrieved_action, Action), str(type(retrieved_action))

    response = await put(base_url=base_url, path='/schedulers/bar', data=scheduler)
    assert response.status_code == 200, f"failed to put scheduler (bar)"
    response = await get(base_url, path='/schedulers/bar')
    assert response.status_code == 200, f"failed to get scheduler (bar)"
    retrieved_scheduler = ResolveBody(Scheduler)(response.json())
    assert isinstance(retrieved_scheduler, Scheduler), str(type(retrieved_scheduler))

    response = await get(base_url=base_url, path='/schedulers/bar/actions/foo')
    assert response.status_code == 200, f"failed to schedule action (foo) using scheduler (bar)"

    response = await get(base_url, '/jobs/count')
    assert response.status_code == 200, 'failed to retrieve job count'
    job_count = response.json()['job_count']
    assert job_count == 1, 'expecting a job count of 1'

    await get(base_url, '/jobs/start')
    time.sleep(4)
    await get(base_url, '/jobs/stop')
   
    lines = None
    with open(action.file, 'r') as fid:
        lines = fid.readlines()

    assert lines is not None and isinstance(lines, list) and len(lines) >= 1








def compute_base_url(host, port):
    return f"http://{host}:{port}"

async def get(base_url:str, path:str):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.get(url=path)

async def put(base_url:str, path:str, data:BaseModel):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.put(url=path, data=data.json())

async def post(base_url:str, path:str, data:BaseModel):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.post(url=path, data=data.json())

async def patch(base_url:str, path:str, data:dict=None):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.patch(url=path, data=data)

async def delete(base_url:str, path:str):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.delete(url=path)