"""
These functions resolve mothership element instances from supplied dictionaries.
"""
from mothership.util import resolve_instance

"""
make sure all modules that contain subclasses of Action are imported below
"""
import mothership.action as action
import mothership.actions.file_action
import mothership.actions.gpio_action

"""
make sure all modules that contain subclasses of Scheduler are imported below
"""
import mothership.scheduler as scheduler

def resolve_action(dictionary:dict):
    return resolve_instance(action.Action, dictionary)

def resolve_scheduler(dictionary:dict):
    return resolve_instance(scheduler.Scheduler, dictionary)