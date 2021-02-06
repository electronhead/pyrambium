"""
These functions resolve mothership element instances from supplied dictionaries.
"""
from mothership.util import resolve_instance

def resolve_action(dictionary:dict):
    """
    make sure all modules are imported below that contain subclasses of Action
    """
    import mothership.action as action

    return resolve_instance(action.Action, dictionary)

def resolve_scheduler(dictionary:dict):
    """
    make sure all modules are imported below that contain subclasses of Scheduler
    """
    import mothership.scheduler as scheduler

    return resolve_instance(scheduler.Scheduler, dictionary)