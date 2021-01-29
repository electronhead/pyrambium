from pyrambium.base.service.scheduler import Scheduler
from pyrambium.base.service.action import Action
from pydantic import BaseModel
import requests

class ApiServer(BaseModel):
    ip_addr:str
    port:int=8000

    # /mothership
    def get_mothership_dict(self):
        return self.get(f"/mothership")
    def clear_mothership(self):
        return self.get(f"/mothership/clear")
    def save_mothership(self):
        return self.get(f"/mothership//save")
    def retrieve_mothership(self, file:str):
        return self.get(f"/mothership//retrieve/{file}")

    # /actions
    def get_action(self, action_name:str):
        return self.get(f"/actions/{action_name}")
    def add_action(self, action_name:str, action:Action):
        return self.put(f"/actions/{action_name}", action)
    def remove_action(self, action_name:str):
        return self.delete(f"/actions/{action_name}")
    def update_action(self, action_name:str, dictionary:dict):
        return self.patch(f"/actions/{action_name}", dictionary)
    def execute_action(self, action_name:str):
        return self.get(f"/actions/{action_name}/execute")
    def unschedule_action(self, action_name:str):
        return self.get(f"/actions/{action_name}/unschedule")

    # /schedulers
    def schedule_action(self, scheduler_name:str, action_name:str):
        return self.get(f"/schedulers/{scheduler_name}/actions/{action_name}")
    def get_scheduler(self, scheduler_name:str):
        return self.get(f"/schedulers/{scheduler_name}")
    def add_scheduler(self, scheduler_name:str, scheduler:Scheduler):
        return self.put(f"/schedulers/{scheduler_name}", scheduler)
    def remove_scheduler(self, scheduler_name:str):
        return self.delete(f"/schedulers/{scheduler_name}")
    def add_scheduler(self, scheduler_name:str, dictionary:dict):
        return self.patch(f"/schedulers/{scheduler_name}", dictionary)
    def execute_scheduler_actions(self, scheduler_name:str):
        return self.get(f"/schedulers/{scheduler_name}/execute")
    def unschedule_scheduler(self, scheduler_name:str):
        return self.delete(f"/schedulers/{scheduler_name}/unschedule")
    def reschedule_all_schedulers(self):
        return self.delete(f"/schedulers/reschedule_all")

    # /jobs
    def start_scheduled_jobs(self):
        return self.get(f"/jobs/start")
    def stop_scheduled_jobs(self):
        return self.get(f"/jobs/stop")
    def job_count(self):
        return self.get(f"/jobs/count")

    # verbs
    def get(self, path:str):
        return self.perform(requests.get, path)
    def put(self, path:str, data:BaseModel):
        return self.perform_base_model(requests.put, path, data)
    def post(self, path:str, data:BaseModel):
        return self.perform_base_model(requests.post, path, data)
    def patch(self, path:str, data:dict):
        return self.perform(requests.patch, path, data)
    def delete(self, path:str):
        return self.perform(requests.delete, path)

    def perform(self, verb, path, data=None):
        cmd = f"http://{self.ip_addr}:{self.port}{path}"
        response = verb(cmd, data)
        return response.json()
    def perform_base_model(self, verb, path, data=BaseModel):
        cmd = f"http://{self.ip_addr}:{self.port}{path}"
        response = verb(cmd, data.json())
        return response.json()
    
class Workbench(BaseModel):
    servers:dict={}
    def add_server(self, name:str, server:ApiServer):
        self.servers[name] = server
    def get_server(self, name:str):
        return self.servers.get(name, None)
    def get_servers(self):
        return list(self.servers.values())
    def count(self):
        return len(self.servers)