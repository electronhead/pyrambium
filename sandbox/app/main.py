"""
The app. 
"""
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def root():
    return 'FastAPI app started'