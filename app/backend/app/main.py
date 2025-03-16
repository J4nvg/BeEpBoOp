from app.models import ComputerParts, Storage, CPU, Memory, Motherboard, Cooler, GPU, PSU, Case
import sqlalchemy as db
from sqlalchemy.orm import Session
from chatbot import run_initial_welcome, process_message
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Request, Body
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
    return {'message': 'JEST KURWA', 'cpu_sku': build.sku}


@app.get("/memory", response_model=ComputerParts)
def memory(build: Build):

    return {"message": "Memory", "data": []}


@app.get("/storage", response_model=ComputerParts)
def disk():
    return {"name": "Storage", "data": []}


@app.get("/mb", response_model=ComputerParts)
def mb():
    return {"name": "Mother Board", "data": []}


@app.get("/cooler", response_model=ComputerParts)
def cooler():
    return {"name": "Cooler", "data": []}


@app.get("/gpu", response_model=ComputerParts)
def gpu():
    return {"name": "GPU", "data": []}


@app.get("/psu", response_model=ComputerParts)
def psu():
    return {"name": "PSU", "data": []}


@app.get("/case", response_model=ComputerParts)
def case():
    return {"name": "Case", "data": []}

class ChatMessage(BaseModel):
    message: str

@app.get("/welcome")
def welcome():
    welcome_text = run_initial_welcome()
    return {"assistant_response": welcome_text}

@app.post("/chat")
def chat_endpoint(chat: ChatMessage):
    response_text = process_message(chat.message)
    return {"assistant_response": response_text}