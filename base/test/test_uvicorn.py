"""
uvicorn test cases
"""
import time
import pytest
from pyrambium.base.service.action import FileHeartbeat
from pyrambium.base.service.scheduler import TimelyScheduler
from pyrambium.base.service.util import FilePath
from pyrambium.app.workbench import ApiServer
from pyrambium.base.test.fixtures import port, host, startup_and_shutdown_uvicorn
import requests

@pytest.mark.asyncio
def test_uvicorn(startup_and_shutdown_uvicorn, port, host, tmp_path):
    """
    testing the a scheduling of an action and running it
    """
    api_server = ApiServer(ip_addr=host, port=port)

    output_file = str(tmp_path / 'output.txt')
    xtra={'port':port, 'ip_addr': host}
    action = FileHeartbeat(file=output_file, xtra=xtra)
    scheduler = TimelyScheduler(interval=1)

    saved_dir = FilePath(path=str(tmp_path).split('/'))
    response = requests.get(f"http://{host}:{port}/")
    # api_server.set_saved_dir(saved_dir=saved_dir)
    # api_server.add_action('foo', action)
    # api_server.add_scheduler('bar', scheduler)
    # api_server.schedule_action('bar', 'foo')
    # api_server.start_scheduled_jobs()
    # time.sleep(4)
    # api_server.stop_scheduled_jobs()

    # lines = None
    # with open(action.file, 'r') as fid:
    #     lines = fid.readlines()

    # assert lines is not None and isinstance(lines, list) and len(lines) >= 1
    