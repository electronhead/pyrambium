"""
This module is the top of the path tree. Establishes all sub-path routers.
"""
from fastapi import FastAPI
from router import actions, schedulers, jobs, mothership

app = FastAPI()

@app.get('/')
async def root():
    return {'message':'Welcome to Pyrambium!'}

app.include_router(actions.router)
app.include_router(schedulers.router)
app.include_router(jobs.router)
app.include_router(mothership.router)
