from pyrambium.base.service.util import PP, IP, Now, object_info, HttpVerb
from pydantic import BaseModel
from typing import Optional
import requests

class Action(BaseModel):
    """
    Actions get something done.
    """
    def execute(self, tag=None, scheduler_info:dict=None):
        """
        This method does something and returns a useful result. If
        the action's benefit is only a side-effect, then returning some status information
        would be the polite thing to do.
        """
        pass

    def info(self):
        return object_info(self)

class FileHeartbeat(Action):
    """
    This class appends status information to a file. This information can include
    a dictionary [xtra] supplied at instantiation.
    """
    file: str
    xtra: Optional[dict]=None

    def execute(self, tag=None, scheduler_info:dict=None):
        payload = ActionPayload.build(action_info=self.info(), scheduler_info=scheduler_info)
        payload['tag'] = tag if tag else 'N/A'
        if self.xtra:
            payload['xtra'] = self.xtra # dictionaries are sorted by key. Nice to have extra information at the bottom.
        with open(self.file, "a") as outfile:
            PP.pprint(payload, stream=outfile)
            outfile.write('\n')
        return {'outcome':'file appended', 'action':self.info()}
    def set_xtra(self, xtra:dict=None):
        self.xtra = xtra
        return self
    def get_xtra(self):
        return self.xtra

class SendHeartbeat(Action):
    """
    This class sends status information to a url.
    """
    url: str
    http_verb: Optional[HttpVerb]=HttpVerb.get
    xtra: Optional[dict]=None

    def execute(self, tag=None, scheduler_info:dict=None):
        payload = ActionPayload.build(action_info=self.info(), scheduler_info=scheduler_info)
        payload['tag'] = tag if tag else 'N/A'
        if self.xtra:
            payload['xtra'] = self.xtra # dictionaries are sorted by key. Nice to have extra information at the bottom.
        response = request_method()(self.url, payload)
        if response.status_code != requests.codes.ok:
            raise Exception(response)
        return response.json()
    
    def request_method():
        options = {
            HttpVerb.get:requests.get,
            HttpVerb.put:requests.put,
            HttpVerb.post:requests.post,
            HttpVerb.patch:requests.patch,
            HttpVerb.delete:requests.delete
        }
        return options[self.http_verb]

# auxilliary
   
class ActionPayload:
    """
    This class produces a status-oriented payload, including action and scheduler info.
    """
    @classmethod
    def build(cls, action_info:dict, scheduler_info:dict):
        payload = {}
        payload.update({'action_info':action_info})
        if scheduler_info:
            payload.update({'scheduler_info':scheduler_info})
        payload.update(cls.action_ip_address())
        payload.update(cls.action_time())
        return payload
    @classmethod
    def action_ip_address(cls):
        return {'action_ip_address': IP.addr}
    @classmethod
    def action_time(cls):
        return {'action_time':Now.s()}