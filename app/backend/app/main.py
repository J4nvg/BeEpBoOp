from app.models import ComputerParts, Storage, CPU, Memory, Motherboard, Cooler, GPU, PSU, Case
import sqlalchemy as db
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.models import *
from app.request_model import Build

app = FastAPI()

engine = create_engine('sqlite:///hardware_db.db', echo=True)
session = Session(engine)

@app.get('/item/{sku}')
def get_item_by_sku(request: Request, sku: int):
    models = [CPU, GraphicCard, Motherboard, RAM, Storage, Cooling, Socket, Case, PSU]
    for model in models:
        item = db.query(model).filter(model.sku==sku).first()
        if item:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/")
def root():
    return {"Hello": "World"}

# Computer parts

@app.post("/cpu", response_model=ComputerParts)
def cpu(build: Build):
    for item, present in build:
        if present:
            print(item,present)
        else:
            print(f'{item} not here')
        
    return {
        'message': 'cpus',
        'data': []
    }


@app.post("/memory", response_model=ComputerParts)
def memory(build: Build):
    return {
        "message": "memories", 
        "data": []
    }


@app.get("/storage", response_model=ComputerParts)
def disk():
    return {"name": "storages", "data": []}


@app.get("/mb", response_model=ComputerParts)
def mb():
    return {"name": "motherboards", "data": []}


@app.get("/cooler", response_model=ComputerParts)
def cooler():
    return {"name": "coolers", "data": []}


@app.get("/gpu", response_model=ComputerParts)
def gpu():
    return {"name": "gpus", "data": []}


@app.get("/psu", response_model=ComputerParts)
def psu():
    return {"name": "psus", "data": []}


@app.get("/case", response_model=ComputerParts)
def case():
    return {"name": "cases", "data": []}
