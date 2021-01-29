"""
This class implements a single process-based system for defining and scheduling actions local
to the python runtime (api server, testing harness). The class implements all of the potential
endpoints of a restful api and supports testing outside of the restful api implementation.

Instances of this class contain Schedulers and Actions, which can at any point be submitted to and removed from the
job scheduling mechanism of the schedule library (refer to the 'continuous' module).
"""
from pyrambium.base.service.util import PP, Dirs, resolve_instance
from pyrambium.base.service.action import Action
from pyrambium.base.service.scheduler import Scheduler
from pyrambium.addendum.service.action import Action
from pyrambium.addendum.service.scheduler import Scheduler
from pyrambium.base.service.continuous import Continuous
from pydantic import BaseModel
from threading import RLock
import pickle
import json

class Mothership(BaseModel):
    """

    Serializations of this class are stored in the local file system. When a runtime starts
    up, Mothership loads the last saved version.
    """
    actions: dict={}
    schedulers: dict={}
    schedulers_actions: dict={}
    saved_dir: str=None

    def get_actions(self):
        with Lok.lock:
            return self.actions
    def get_schedulers(self):
        with Lok.lock:
            return self.schedulers
    def get_schedulers_actions(self):
        with Lok.lock:
            return self.schedulers_actions

    def initialize(self):
        Lok.reset()
    def pprint(self):
        PP.pprint(self.dict())

    def save(self, file:str):
        with Lok.lock:
            assert self.saved_dir, 'saved_dir must be set'
            with open(self.saved_dir+file+'.pickle', 'wb') as outfile:
                pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)
            with open(self.saved_dir+file+'.json', 'w') as outfile:
                json.dump(self.json(), outfile, indent=2)
    def load(self, file:str):
        with Lok.lock:
            assert self.saved_dir, 'saved_dir must be set'
            with open(self.saved_dir+file+'.pickle', 'rb') as infile:
                return pickle.load(infile)
    def set_save_dir(self, saved_dir:str):
        self.saved_dir = saved_dir
    
    def load_current(self):
        return self.load('current')
    def save_current(self):
        with Lok.lock:
            self.save('current')

    def clear_all(self, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            schedulers_copy = self.schedulers.copy()
            for scheduler_name in schedulers_copy:
                self.remove_scheduler(scheduler_name, continuous)
            actions_copy = self.actions.copy()
            for action_name in actions_copy:
                self.remove_action(action_name, continuous)
            self.schedulers_actions.clear()
            self.save_current()

    def get_scheduled_action_count(self):
        # returns the total number of actions in the schedulers_actions dictionary
        # should be equal to the number of jobs in related Continuous instance
        with Lok.lock:
            return sum(len(action_array) for action_array in self.schedulers_actions.values())

    def add_action(self, action_name:str, action:Action):
        with Lok.lock:
            assert not action_name in self.actions, f"action ({action_name}) already exists"
            self.actions[action_name] = action
            self.save_current()
    def get_action(self, action_name:str):
        with Lok.lock:
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            return self.actions.get(action_name)
    def get_actions(self):
        with Lok.lock:
            return self.actions
    def remove_action(self, action_name:str, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            for scheduler_name in self.schedulers:
                self.unschedule_action(action_name, continuous)
                self.schedulers_actions[scheduler_name].remove(action_name)
            self.actions.pop(action_name, None)
            self.save_current()
    def update_action(self, action_name:str, dictionary:dict, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            action = self.actions.get(action_name)
            action.__dict__.update(dictionary)
            self.reschedule_action(action_name, continuous)
            self.save_current()
    def execute_action(self, action_name:str):
        with Lok.lock:
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            return self.get_action(action_name).execute()

    # schedulers
    def add_scheduler(self, scheduler_name:str, scheduler:Scheduler):
        with Lok.lock:
            assert not scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) already exists"
            self.schedulers[scheduler_name] = scheduler
            self.schedulers_actions[scheduler_name] = []
            self.save_current()
    def get_scheduler(self, scheduler_name:str):
        with Lok.lock:
            return self.schedulers.get(scheduler_name, None)
    def remove_scheduler(self, scheduler_name:str, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) does not exist"
            self.unschedule_scheduler(scheduler_name, continuous)
            self.schedulers.pop(scheduler_name)
            self.schedulers_actions[scheduler_name].clear() # pro-actively clean up. less work for GC.
            self.schedulers_actions.pop(scheduler_name)
            self.save_current()
    def update_scheduler(self, scheduler_name:str, dictionary:dict, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) does not exist"
            scheduler = self.schedulers.get(name)
            scheduler.__dict__.update(dictionary)
            self.reschedule_scheduler(scheduler_name, continuous)
            self.save_current()
    def execute_scheduler_actions(self, scheduler_name:str):
        with Lok.lock:
            assert scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) does not exist"
            result = []
            for action_name in self.schedulers_actions.get(scheduler_name, []):
                result.append(self.get_action(action_name).execute())
            return result

    # scheduling
    def schedule_action(self, scheduler_name:str, action_name:str, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) does not exist"
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            assert not action_name in self.schedulers_actions[scheduler_name]
            scheduler = self.get_scheduler(scheduler_name)
            action = self.actions.get(action_name)
            tag = self.scheduler_tag(scheduler_name, action_name)
            scheduler.schedule_action(tag, action, continuous)
            self.schedulers_actions[scheduler_name].append(action_name)
            self.save_current()
    def unschedule_action(self, action_name:str, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert action_name in self.actions, f"action ({action_name}) does not exist"
            for scheduler_name in self.schedulers_actions:
                if action_name in self.schedulers_actions[scheduler_name]:
                    tag = self.scheduler_tag(scheduler_name, action_name)
                    continuous.clear(tag)
                    self.schedulers_actions[scheduler_name].remove(action_name)
            self.save_current()
    def unschedule_scheduler(self, scheduler_name:str, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            assert scheduler_name in self.schedulers, f"scheduler ({scheduler_name}) does not exist"
            for action_name in self.schedulers_actions[scheduler_name]:
                tag = self.scheduler_tag(scheduler_name, action_name)
                continuous.clear(tag)
            self.schedulers_actions[scheduler_name].clear()
            self.save_current()
    def reschedule_all_schedulers(self, continuous:Continuous=Continuous.get()):
        with Lok.lock:
            for scheduler_name in self.schedulers_actions:
                for action_name in self.schedulers_actions[scheduler_name]:
                    tag = self.scheduler_tag(scheduler_name, action_name)
                    continuous.clear(tag)
                    scheduler = self.get_scheduler(scheduler_name)
                    action = self.actions[action_name]
                    scheduler.schedule_action(tag, action, continuous)
  
    # utility
    def scheduler_tag(self, schedule_name:str, action_name:str):
        # computes job tag for scheduler and action
        return f"{schedule_name}:{action_name}"
    @classmethod
    def instantiate_from_dict(cls, dictionary:dict={}):
        """
        converts dictionary to an Mothership instance.
        For resolution to the proper class, it's important that modules containing
        Action and Scheduler classes are imported in this module.
        """
        if len(dictionary) is 0:
            return Mothership(saved_dir=Dirs.saved_dir)
        else:
            saved_dir = dictionary['saved_dir']
            actions = dictionary['actions']
            schedulers = dictionary['schedulers']
            schedulers_actions = dictionary['schedulers_actions']
            # replace key's value for each key...
            for action_name in actions:
                actions[action_name] = resolve_instance(Action, actions[action_name])
            for scheduler_name in schedulers:
                schedulers[scheduler_name] = resolve_instance(Scheduler, schedulers[scheduler_name])
            return Mothership(
                saved_dir=saved_dir,
                actions=actions,
                schedulers=schedulers,
                schedulers_actions=schedulers_actions)

# ------------------
"""
usage:
  with Lok.lock:
    # critical section
note:
  singleton
"""
class Lok:
    lock = RLock()
    @classmethod
    def reset(cls):
        cls.lock = RLock()

class MothershipsLittleHelper:
    mothership = None
    @classmethod
    def get(cls):
        if not cls.mothership:
            cls.mothership = Mothership(saved_dir=Dirs.saved_dir())
            try:    
                cls.mothership = cls.mothership.load_current()
            except Exception as e:
                pass # TODO: log it!
            cls.mothership.initialize()
            cls.mothership.reschedule_all_schedulers()
        return cls.mothership