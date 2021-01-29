from pyrambium.base.service.scheduler import Scheduler
import pyrambium.addendum.service.scheduler 
from pyrambium.base.service.util import ResolveBody
from pyrambium.app.shared import return_success, raised_exception, get_mothership
from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix='',
    tags=['Schedulers']
)

@router.get('/schedulers/{scheduler_name}/actions/{action_name}', status_code=status.HTTP_202_ACCEPTED)
def schedule_action(scheduler_name:str, action_name:str):
    try:
        get_mothership().schedule_action(scheduler_name=scheduler_name, action_name=action_name)
        return return_success(f"action ({action_name}) was successfully scheduled ({scheduler_name})")
    except Exception as e:
        raise raised_exception(f"failed to schedule ({scheduler_name}) action ({action_name})", e)

@router.get('/schedulers/{scheduler_name}', status_code=status.HTTP_200_OK)
def get_scheduler(scheduler_name:str):
    try:
        scheduler = get_mothership().get_scheduler(scheduler_name=scheduler_name)
        return return_success(scheduler.dict())
    except Exception as e:
        raise raised_exception(f"failed to retrieve the action ({action_name})", e)

@router.put('/schedulers/{scheduler_name}', status_code=status.HTTP_201_CREATED)
def add_scheduler(scheduler_name:str, scheduler=Depends(ResolveBody(Scheduler))):
    try:
        assert scheduler, f"couldn't resolve class for scheduler ({scheduler_name})"
        get_mothership().add_scheduler(scheduler_name=scheduler_name, scheduler=scheduler)
        return return_success(f"scheduler ({scheduler_name}) was successfully added")
    except Exception as e:
        raise raised_exception(f"failed to add scheduler ({scheduler_name})", e)

@router.delete('/schedulers/{scheduler_name}', status_code=status.HTTP_202_ACCEPTED)
def remove_scheduler(scheduler_name:str):
    try:
        get_mothership().remove_scheduler(scheduler_name=scheduler_name)
        return return_success(f"scheduler ({scheduler_name}) was successfully removed")
    except Exception as e:
        raise raised_exception(f"failed to remove scheduler ({scheduler_name})", e)

@router.patch('/schedulers/{scheduler_name}', status_code=status.HTTP_202_ACCEPTED)
def update_scheduler(scheduler_name:str, dictionary:dict):
    try:
        get_mothership().update_scheduler(scheduler_name=scheduler_name, dictionary=dictionary)
        return return_success(f"scheduler ({scheduler_name}) was successfully updated")
    except Exception as e:
        raise raised_exception(f"failed to update scheduler ({scheduler_name})", e)

@router.get('/schedulers/{scheduler_name}/execute', status_code=status.HTTP_200_OK)
def execute_scheduler_actions(scheduler_name:str):
    try:
        result = get_mothership().execute_scheduler_actions(scheduler_name=scheduler_name)
        return return_success({'msg': f"scheduler ({scheduler_name}) actions were successfully executed", 'result':result})
    except Exception as e:
        raise raised_exception(f"failed to execute scheduler ({scheduler_name}) actions", e)

@router.get('/schedulers/{scheduler_name}/unschedule', status_code=status.HTTP_202_ACCEPTED)
def unschedule_scheduler(scheduler_name:str):
    try:
        get_mothership().unschedule_scheduler(scheduler_name=scheduler_name)
        return return_success(f"scheduler ({scheduler_name}) was successfully unscheduled")
    except Exception as e:
        raise raised_exception(f"failed to unschedule scheduler ({scheduler_name})", e)

@router.get('/schedulers/reschedule_all', status_code=status.HTTP_202_ACCEPTED)
def reschedule_all_schedulers():
    try:
        get_mothership().reschedule_all_schedulers()
        return return_success("all schedulers were successfully unscheduled")
    except Exception as e:
        raise raised_exception("failed to unschedule all schedulers", e)