from models import ComputerPart, Storage, CPU, Memory, Motherboard, Cooler, GPU, PSU, Case

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

# Computer parts

@app.get("/cpu", response_model=ComputerPart)
def cpu():
    return {"cpu": "100%"}


@app.get("/cpu/{cpu_id}", response_model=CPU)
def cpu(cpu_id: int):
    return {"cpu": cpu_id}


@app.get("/memory", response_model=ComputerPart)
def memory():
    return {"memory": "100%"}


@app.get("/memory/{memory_id}", response_model=Memory)
def memory(memory_id: int):
    return {"memory": memory_id}


@app.get("/storage", response_model=ComputerPart)
def disk():
    return {"storage": "100%"}


@app.get("/storage/{storage_id}", response_model=Storage)
def disk(storage_id: int):
    return {"storage": storage_id}


@app.get("/mb", response_model=ComputerPart)
def mb():
    return {"mb": "100%"}


@app.get("/mb/{mb_id}", response_model=Motherboard)
def mb(mb_id: int):
    return {"mb": mb_id}


@app.get("/cooler", response_model=ComputerPart)
def cooler():
    return {"cooler": "100%"}


@app.get("/cooler/{cooler_id}", response_model=Cooler)
def cooler(cooler_id: int):
    return {"cooler": cooler_id}


@app.get("/gpu", response_model=ComputerPart)
def gpu():
    return {"gpu": "100%"}


@app.get("/gpu/{gpu_id}", response_model=GPU)
def gpu(gpu_id: int):
    return {"gpu": gpu_id}


@app.get("/psu", response_model=ComputerPart)
def psu():
    return {"psu": "100%"}


@app.get("/psu/{psu_id}", response_model=PSU)
def psu(psu_id: int):
    return {"psu": psu_id}


@app.get("/case", response_model=ComputerPart)
def case():
    return {"case": "100%"}


@app.get("/case/{case_id}", response_model=Case)
def case(case_id: int):
    return {"case": case_id}
