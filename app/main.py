"""
This module is the top of the path tree. Establishes all sub-path routers.
"""
from fastapi import FastAPI
import uvicorn
from mothership.mothership import MothershipsLittleHelper
from mothership.continuous import Continuous
from mothership.util import Dirs
from router import actions, schedulers, mothership, jobs
from shared import set_continuous, set_mothership

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

if __name__ == "__main__":
    uvicorn.run("main.app", host="127.0.0.1", port=5000, log_level="info")