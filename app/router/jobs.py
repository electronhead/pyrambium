from pyrambium.base.service.continuous import Continuous
from pyrambium.app.shared import return_success, raised_exception
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/jobs",
    tags=['Jobs']
)

@router.get('/start', status_code=status.HTTP_202_ACCEPTED)
def start_scheduled_jobs():
    try:
        assert not Continuous.get().is_running(), "should not be running when trying to start"
        Continuous.get().run_continuously()
        return return_success("started running")
    except Exception as e:
        raise raised_exception("failed to start running", e)

@router.get('/stop', status_code=status.HTTP_202_ACCEPTED)
def stop_scheduled_jobs():
    try:
        assert Continuous.get().is_running(), "should be running when trying to stop"
        Continuous.get().stop_running_continuously()
        return return_success("stopped running")
    except Exception as e:
        raise raised_exception("failed to stop running", e)

@router.get('/count', status_code=status.HTTP_202_ACCEPTED)
def job_count():
    try:
        return return_success({'job_count':Continuous.get().job_count()})
    except Exception as e:
        raise raised_exception("failed to get job count", e)