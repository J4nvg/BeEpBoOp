from app.models import ComputerParts, Storage, CPU, Memory, Motherboard, Cooler, GPU, PSU, Case
import sqlalchemy as db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import *
from db.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/item/{sku}')
def get_item_by_sku(sku: int, db: Session = Depends(get_db)):
    models = [CPU, GraphicCard, Motherboard, RAM, Storage, Cooling, Socket, Case, PSU]
    for model in models:
        item = db.query(model).filter(model.sku==sku).first()
        if item:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"Hello": "World"}

# Computer parts

@app.get("/cpu", response_model=ComputerParts)

def cpu():
    return {"message": "CPU", "data": []}


@app.get("/cpu/{cpu_id}", response_model=CPU)
def cpu(cpu_id: int):
    return {"id": cpu_id}


@app.get("/memory", response_model=ComputerParts)
def memory(db: Session = Depends(get_db)):
    return {"message": "Memory", "data": []}


@app.get("/storage", response_model=ComputerParts)
def disk(db: Session = Depends(get_db)):
    return {"name": "Storage", "data": []}


@app.get("/mb", response_model=ComputerParts)
def mb(db: Session = Depends(get_db)):
    return {"name": "Mother Board", "data": []}


@app.get("/cooler", response_model=ComputerParts)
def cooler(db: Session = Depends(get_db)):
    return {"name": "Cooler", "data": []}


@app.get("/gpu", response_model=ComputerParts)
def gpu(db: Session = Depends(get_db)):
    return {"name": "GPU", "data": []}


@app.get("/psu", response_model=ComputerParts)
def psu(db: Session = Depends(get_db)):
    return {"name": "PSU", "data": []}


@app.get("/case", response_model=ComputerParts)
def case(db: Session = Depends(get_db)):
    return {"name": "Case", "data": []}
