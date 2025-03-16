
from models import ComputerParts, Storage_response, CPU_response, Memory_response, Motherboard_response, Cooler_response, GPU_response, PSU_response, Case_response

import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.orm import Session
#from app.chatbot import run_initial_welcome, process_message
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from request_model import Build
from fastapi.middleware.cors import CORSMiddleware
from db.models import *

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


@app.post("/ram", response_model=ComputerParts)
def memory(build: Build):
    memory_query = select(RAM)

    if build.cpu:
        cpu_query = select(CPU).where(CPU.sku == build.cpu)
        cpu = session.scalars(cpu_query).one_or_none()
        if cpu:
            name = cpu.name.split(' ')[0]
            memory_query = memory_query.where(
                RAM.AMDexpo_support == 1
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
        SKU = ram.sku,
        image_url = ram.image_url,
        link = ram.link,
        ram_type = ram.ram_type,
        ram_slots = int(ram.ram_slots.split(' ')[0]),
        memory = int(ram.memory.split(' ')[0]),
        XMP_support = ram.XMP_support,
        AMDexpo_support = ram.AMDexpo_support
    ) for ram in rams]

    return {
        "message": "rams", 
        "data": final_list
    }


@app.post("/storage", response_model=ComputerParts)
def disk(build: Build):
    disk_query = select(Storage)

    if build.mb:
        mb_query = select(Motherboard).where(Motherboard.sku == build.mb).one()
        mb = session.scalars(mb_query).one_or_none()
        if mb:
            disk_query = disk_query.where(
                Storage.storage_type == mb.storage_type
            )
    
    disks = session.scalars(disk_query).all()

    final_list = [Storage_response(
        name = disk.name,
        price = disk.price,
        SKU = disk.sku,
        image_url = disk.image_url,
        link = disk.link,
        storage_type = disk.storage_type
    ) for disk in disks]

    return {
        "message": "storages", 
        "data": final_list
    }


@app.post("/mb", response_model=ComputerParts)
def mb(build: Build):
    mb_query = select(Motherboard)

    if build.case:
        case_query = select(Case).where(Case.sku == build.case)
        case = session.scalars(case_query).one_or_none()
        if case:
            mb_query = mb_query.where(
                Motherboard.case_compatibility == case.case_format
            )
    
    if build.cpu:
        cpu_query = select(CPU).where(CPU.sku == build.cpu)
        cpu = session.scalars(cpu_query).one_or_none()
        if cpu:
            mb_query = mb_query.where(
                Motherboard.socket == cpu.socket
            )

    if build.ram:
        ram_query = select(RAM).where(RAM.sku == build.ram)
        ram = session.scalars(ram_query).one_or_none()
        if ram:
            mb_query = mb_query.where(
                (Motherboard.ram_slots >= ram.ram_slots) | (Motherboard.max_ram >= ram.memory) | (Motherboard.ram_type == ram.ram_type)
            )
    
    if build.gpu:
        gpu_query = select(GraphicCard).where(GraphicCard.sku == build.gpu)
        gpu = session.scalars(gpu_query).one_or_none()
        if gpu:
            if gpu.pcie_version == 5:
                mb_query = mb_query.where(
                    Motherboard.pcie5_slots > 0
                )
            elif gpu.pcie_version == 4:
                mb_query = mb_query.where(
                    (Motherboard.pcie4_x16 > 0) | (Motherboard.pcie4_x4 > 0)  
                )

    mbs = session.scalars(mb_query).all()

    final_list = [Motherboard_response(
        name = mb.name,
        price = mb.price,
        SKU = mb.sku,
        image_url = mb.image_url,
        link = mb.link,
        case_compatibility = mb.case_compatibility,
        socket = mb.socket,
        ram_slots = mb.ram_slots,
        max_ram = int(mb.max_ram.split(' ')[0]),
        ram_type = mb.ram_type,
        pcie5_slots = mb.pcie5_slots,
        pcie4_x16 = mb.pcie4_x16,
        pcie4_x4 = mb.pcie4_x4
    ) for mb in mbs]
    

    return {"message": "motherboards", "data": final_list}


@app.post("/cooler", response_model=ComputerParts)
def cooler(build: Build):
    cooling_query = select(Cooling)
    coolers = session.scalars(cooling_query).all()

    final_list = [Cooler_response(
        name = cool.name,
        price = cool.price,
        SKU = cool.sku,
        image_url = cool.image_url,
        link = cool.link,
        nr_fans = cool.number_of_fans,
        fan_diameter = int(cool.fan_diamater.split(' ')[0]),
        power_consumption = cool.power_consumption
    ) for cool in coolers]
    return {"message": "coolers", "data": final_list}


@app.post("/gpu", response_model=ComputerParts)
def gpu(build: Build):
    gpu_query = select(GraphicCard)

    if build.mb:
        mb_query = select(Motherboard).where(Motherboard.sku == build.mb)
        mb = session.scalars(mb_query).one_or_none()
        if mb:
            if mb.pcie5_slots >= 0:
                pcie_version = 5
            elif mb.pcie4_x16 >= 0 or mb.pcie4_x4 >= 0:
                pcie_version = 4
            gpu_query = gpu_query.where(
                GraphicCard.pcie_version == pcie_version
            )
    if build.case:
        case_query = select(Case).where(Case.sku == build.case)
        case = session.scalars(case_query).one_or_none()
        if case:
            gpu_query = gpu_query.where(
                GraphicCard.length <= case.max_gpu_size
            )
    
    gpus = session.scalars(gpu_query).all()

    final_list = [GPU_response(
        name = gpu.name,
        price = gpu.price,
        SKU = gpu.sku,
        image_url = gpu.image_url,
        link = gpu.link,
        pcie_version = gpu.pcie_version,
        power_consumption = gpu.power_consumption,
        length = gpu.length
    ) for gpu in gpus]

    return {
        "message": "gpus", 
        "data": final_list
    }


@app.post("/psu", response_model=ComputerParts)
def psu(build: Build):
    psu_query = select(PSU)

    if build.gpu:
        gpu_query = select(GraphicCard).where(GraphicCard.sku == build.gpu)
        gpu = session.scalars(gpu_query).one_or_none()
        if gpu:
            psu_query = psu_query.where(
                int(PSU.power_consumption.split(' ')[0]) >= gpu.power_consumption
            )
    
    if build.cpu:
        cpu_query = select(CPU).where(CPU.sku == build.gpu)
        cpu = session.scalars(cpu_query).one_or_none()
        if cpu:
            psu_query = psu_query.where(
                int(PSU.power_consumption.split(' ')[0]) >= int(cpu.power_consumption.split(' ')[0])
            )
    
    psus = session.scalars(psu_query).all()

    final_list = [PSU_response(
        name = psu.name,
        price = psu.price,
        link = psu.link,
        SKU = psu.sku,
        image_url = psu.image_url,
        depth = psu.depth,
        power = int(psu.power.split(' ')[0])
    ) for psu in psus]


    return {"message": "psus", "data": final_list}


@app.post("/case", response_model=ComputerParts)
def case(build: Build):
    case_query = select(Case)

    if build.mb:
        mb_query = select(Motherboard).where(Motherboard.sku == sku)
        mb = session.scalars(mb_query).one_or_none()
        if mb:
            case_query = case_query.where(
                Case.case_format == mb.case_compatibility
            )

    if build.gpu:
        gpu_query = select(GraphicCard).where(GraphicCard.sku == build.gpu)
        gpu = session.scalars(gpu_query).one_or_none()
        if gpu:
            case_query = case_query.where(
                Case.max_gpu_size >= gpu.length
            )
    
    if build.psu:
        psu_query = select(PSU).where(PSU.sku == build.sku)
        psu = session.scalars(psu_query).one_or_none()
        if psu:
            case_query = case_query.where(
                (Case.max_psu_length >= psu.depth)
            )
    
    cases = session.scalars(case_query).all()

    final_list = [Case_response(
        name = case.name,
        price = case.price, 
        SKU = case.sku, 
        image_url = case.image_url,
        link = case.link,
        case_format = case.case_format,
    ) for case in cases]

    return {"message": "cases", "data": final_list}

