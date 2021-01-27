from mothership.base.service.action import Action
import mothership.addendum.service.action
from mothership.base.service.mothership import mothership
from mothership.base.service.util import ResolveBody
from fastapi import APIRouter, status, HTTPException, Depends
from mothership.app.shared import return_success, raised_exception

router = APIRouter(
    prefix='',
    tags=['Actions']
)

# ====================
@router.get('/actions/{action_name}', status_code=status.HTTP_200_OK)
def get_action(action_name:str):
    try:
        action = mothership.get_action(action_name=action_name)
        return return_success(action.dict())
    except Exception as e:
        raise raised_exception(f"failed to retrieve the action ({action_name})", e)

@router.put('/actions/{action_name}', status_code=status.HTTP_201_CREATED)
def add_action(action_name:str, action=Depends(ResolveBody(Action))):
    try:
        assert action, f"couldn't resolve class for action ({action_name})"
        mothership.add_action(action_name=action_name, action=action)
        return return_success(f"action ({action_name}) was successfully added")
    except Exception as e:
        raise raised_exception(f"failed to add action ({action_name})", e)

@router.delete('/actions/{action_name}', status_code=status.HTTP_202_ACCEPTED)
def remove_action(action_name:str):
    try:
        mothership.remove_action(action_name=action_name)
        return return_success(f"action ({action_name}) was successfully removed")
    except Exception as e:
        raise raised_exception(f"failed to remove action ({action_name})", e)

@router.patch('/actions/{action_name}', status_code=status.HTTP_202_ACCEPTED)
def update_action(action_name:str, dictionary:dict):
    try:
        mothership.update_action(action_name=action_name, dictionary=dictionary)
        return return_success(f"action ({action_name}) was successfully updated")
    except Exception as e:
        raise raised_exception(f"failed to update action ({action_name})", e)

@router.get('/actions/{action_name}/execute', status_code=status.HTTP_200_OK)
def execute_action(action_name:str):
    try:
        result = mothership.execute_action(action_name=action_name)
        return return_success({'msg': f"action ({action_name}) was successfully executed", 'result':result})
    except Exception as e:
        raise raised_exception(f"failed to execute action ({action_name})", e)

@router.get('/actions/{action_name}/unschedule', status_code=status.HTTP_202_ACCEPTED)
def unschedule_action(action_name:str):
    try:
        mothership.unschedule_action(action_name=action_name)
        return return_success(f"action ({action_name}) was successfully unscheduled")
    except Exception as e:
        raise raised_exception(f"failed to unschedule action ({action_name})", e)

@router.get('/actions/{action_name}/reschedule', status_code=status.HTTP_202_ACCEPTED)
def reschedule_action(action_name:str):
    try:
        mothership.reschedule_action(action_name=action_name)
        return return_success(f"action ({action_name}) was successfully unscheduled")
    except Exception as e:
        raise raised_exception(f"failed to reschedule action ({action_name})", e)