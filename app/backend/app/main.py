from app.models import ComputerParts, Storage, CPU, Memory, Motherboard, Cooler, GPU, PSU, Case

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

# Computer parts

@app.get("/cpu", response_model=ComputerParts)
def cpu():
    return {"message": "CPU", "data": []}


@app.get("/cpu/{cpu_id}", response_model=CPU)
def cpu(cpu_id: int):
    return {"id": cpu_id}


@app.get("/memory", response_model=ComputerParts)
def memory():
    return {"name": "Memory", "data": []}


@app.get("/memory/{memory_id}", response_model=Memory)
def memory(memory_id: int):
    return {"id": memory_id}


@app.get("/storage", response_model=ComputerParts)
def disk():
    return {"name": "Storage", "data": []}


@app.get("/storage/{storage_id}", response_model=Storage)
def disk(storage_id: int):
    return {"id": storage_id}


@app.get("/mb", response_model=ComputerParts)
def mb():
    return {"name": "Mother Board", "data": []}


@app.get("/mb/{mb_id}", response_model=Motherboard)
def mb(mb_id: int):
    return {"id": mb_id}


@app.get("/cooler", response_model=ComputerParts)
def cooler():
    return {"name": "Cooler", "data": []}


@app.get("/cooler/{cooler_id}", response_model=Cooler)
def cooler(cooler_id: int):
    return {"id": cooler_id}


@app.get("/gpu", response_model=ComputerParts)
def gpu():
    return {"name": "GPU", "data": []}


@app.get("/gpu/{gpu_id}", response_model=GPU)
def gpu(gpu_id: int):
    return {"id": gpu_id}


@app.get("/psu", response_model=ComputerParts)
def psu():
    return {"name": "PSU", "data": []}


@app.get("/psu/{psu_id}", response_model=PSU)
def psu(psu_id: int):
    return {"id": psu_id}


@app.get("/case", response_model=ComputerParts)
def case():
    return {"name": "Case", "data": []}


@app.get("/case/{case_id}", response_model=Case)
def case(case_id: int):
    return {"id": case_id}
