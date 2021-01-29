from pyrambium.base.service.action import Action
import pyrambium.addendum.service.action
from pyrambium.base.service.util import ResolveBody
from pyrambium.app.shared import return_success, raised_exception, get_mothership
from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix='',
    tags=['Actions']
)

@router.get('/actions/{action_name}', status_code=status.HTTP_200_OK)
def get_action(action_name:str):
    try:
        action = get_mothership().get_action(action_name=action_name)
        return return_success(action)
    except Exception as e:
        raise raised_exception(f"failed to retrieve the action ({action_name})", e)

@router.put('/actions/{action_name}', status_code=status.HTTP_201_CREATED)
def add_action(action_name:str, action=Depends(ResolveBody(Action))):
    try:
        assert action, f"couldn't resolve class for action ({action_name})"
        get_mothership().add_action(action_name=action_name, action=action)
        return return_success(f"action ({action_name}) was successfully added")
    except Exception as e:
        raise raised_exception(f"failed to add action ({action_name})", e)

@router.delete('/actions/{action_name}', status_code=status.HTTP_202_ACCEPTED)
def remove_action(action_name:str):
    try:
        get_mothership().remove_action(action_name=action_name)
        return return_success(f"action ({action_name}) was successfully removed")
    except Exception as e:
        raise raised_exception(f"failed to remove action ({action_name})", e)

@router.patch('/actions/{action_name}', status_code=status.HTTP_202_ACCEPTED)
def update_action(action_name:str, dictionary:dict):
    try:
        get_mothership().update_action(action_name=action_name, dictionary=dictionary)
        return return_success(f"action ({action_name}) was successfully updated")
    except Exception as e:
        raise raised_exception(f"failed to update action ({action_name})", e)

@router.get('/actions/{action_name}/execute', status_code=status.HTTP_200_OK)
def execute_action(action_name:str):
    try:
        result = get_mothership().execute_action(action_name=action_name)
        return return_success({'msg': f"action ({action_name}) was successfully executed", 'result':result})
    except Exception as e:
        raise raised_exception(f"failed to execute action ({action_name})", e)

@router.get('/actions/{action_name}/unschedule', status_code=status.HTTP_202_ACCEPTED)
def unschedule_action(action_name:str):
    try:
        get_mothership().unschedule_action(action_name=action_name)
        return return_success(f"action ({action_name}) was successfully unscheduled")
    except Exception as e:
        raise raised_exception(f"failed to unschedule action ({action_name})", e)