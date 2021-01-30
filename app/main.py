"""
This module is the top of the path tree. Establishes all sub-path routers.
"""
from fastapi import FastAPI
from router import actions, schedulers, jobs, mothership
from pyrambium.base.service.mothership import MothershipsLittleHelper
from pyrambium.base.service.continuous import Continuous
from pyrambium.app.shared import set_continuous, set_mothership

app = FastAPI()

@app.get('/')
async def root():
    return 'Pyrambium API server started'

mothership_instance = MothershipsLittleHelper.get()
continuous_instance = Continuous.get()

app.include_router(set_mothership(actions.router, mothership_instance))
app.include_router(set_mothership(schedulers.router, mothership_instance))
app.include_router(set_mothership(mothership.router, mothership_instance))
app.include_router(set_continuous(jobs.router, continuous_instance))