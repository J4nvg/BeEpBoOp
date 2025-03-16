
from models import ComputerParts, Storage, CPU_response, Memory_response, Motherboard, Cooler, GPU, PSU, Case
from chatbot import run_initial_welcome, process_message
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.orm import Session
#from app.chatbot import run_initial_welcome, process_message
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from request_model import Build
from fastapi.middleware.cors import CORSMiddleware
from db.models import *


class ChatMessage(BaseModel):
    message: str

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    cpu_query = select(CPU)

    print(f'!!!\n{build}\n!!!')
    if build.mb:    
        mb_query = select(Motherboard).where(Motherboard.sku == build.mb)
        mb = session.scalars(mb_query).one_or_none()
        if mb:
            cpu_query = cpu_query.where(CPU.socket == mb.socket)

    if build.ram:
        ram_query = select(RAM).where(RAM.sku == build.ram)
        ram = session.scalars(ram_query).one_or_none()
        if ram:
            cpu_query = cpu_query.where(
                (CPU.XMP_support == ram.XMP_support) | (CPU.AMDexpo_support == ram.AMDexpo_support)
            )
    cpus = session.scalars(cpu_query).all()
        
    final_list = [CPU_response(
            name = cpu.name,
            price = cpu.price,
            SKU = cpu.sku,
            image_url = cpu.image_url,
            link = cpu.link,
            socket = cpu.socket,
            power_consumption = cpu.power_consumption,
            cores = cpu.cores,
            threads = cpu.threads,
            base_clock = cpu.base_clock,
            boost_clock = cpu.boost_clock
        ) for cpu in cpus]

    return {
        'message': 'cpus',
        'data': final_list
    }


@app.post("/memory", response_model=ComputerParts)
def memory(build: Build):
    memory_query = select(RAM)

    if build.cpu:
        cpu_query = select(CPU).where(CPU.sku == build.cpu)
        cpu = session.scalars(cpu_query).one_or_none()
        if cpu:
            memory_query = memory_query.where(
                (RAM.XMP_support == build.XMP_support) | (RAM.AMDexpo_support == build.AMDexpo_support)
            )

    if build.mb:
        mb_query = select(Motherboard).where(Motherboard.sku == build.mb)
        mb = session.scalars(mb_query).one_or_none()
        if mb:
            memory_query = memory_query.where(
                (RAM.ram_type == mb.ram_type) | (RAM.ram_slots <= mb.ram_slots) | (RAM.memory <= mb.max_ram)
            )
    
    rams = session.scalars(memory_query).all()

    final_list = [Memory_response(
        name = ram.name,
        price = ram.price,
        SKU = ram.price,
        image_url = ram.image_url,
        link = ram.link,
        ram_type = ram.ram_type,
        ram_slots = ram.ram_slots,
        memory = ram.memory,
        XMP_support = ram.XMP_support,
        AMDexpo_support = ram.AMDexpo_support
    ) for ram in rams]

    return {
        "message": "rams", 
        "data": final_list
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

@app.get("/welcome")
def welcome():
    welcome_text = run_initial_welcome()
    return {"assistant_response": welcome_text}

@app.post("/chat")
def chat_endpoint(chat: ChatMessage):
    response_text = process_message(chat.message)
    return {"assistant_response": response_text}