"""
This code in this module is used in FastAPI path code.
"""
from fastapi import status, HTTPException
from pyrambium.base.service.mothership import MothershipsLittleHelper
from pyrambium.base.service.util import Now

def return_success(dictionary:dict):
    """
    for successful returns
    """
    return dictionary

def raised_exception(text:str, exception:Exception):
    """
    for exception reporting
    """
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {'outcome':text, 'exception': str(exception), 'time':Now.s()}
    return HTTPException(status_code=status_code, detail=detail)

def get_mothership():
    """
    returns a singleton Mothership instance
    """
    return MothershipsLittleHelper.get()