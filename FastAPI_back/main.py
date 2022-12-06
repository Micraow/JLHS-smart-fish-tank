import os, sys

p = os.path.abspath('.')
sys.path.insert(1, p)
from fastapi import FastAPI
from FastAPI_back.client import *

run()

app = FastAPI()


@app.get("/")
def read_root():
    return {"OK"}