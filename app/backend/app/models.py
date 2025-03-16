from pydantic import BaseModel, field_validator
from typing import List
    
class ComputerPart(BaseModel):
    name: str
    price: float
    SKU: int
    image_url: str
    link: str

class ComputerParts(BaseModel):
    message: str
    data: List[ComputerPart] = []

class CPU_response(ComputerPart):
    socket: str
    cores: int
    threads: int
    base_clock: float
    boost_clock: float
    power_consumption: str

class Memory_response(ComputerPart):
    ram_type: str
    ram_slots: int
    memory: int
    XMP_support: bool
    AMDexpo_support: bool

class Storage_response(ComputerPart):
    storage_type: str

class Motherboard_response(ComputerPart):
    case_compatibility: str
    socket: str
    ram_slots: int
    max_ram: int
    ram_type: str
    pcie4_x16: int
    pcie4_x4: int
    pcie5_slots: int


class Cooler_response(ComputerPart):
    nr_fans: int
    fan_diameter: int
    power_consumption: int

    @field_validator('power_consumption', mode='before')
    @classmethod
    def convert_length(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")  
            try:
                return int(float(v)) 
            except ValueError:
                raise ValueError("Invalid type for length, must be an integer or numeric string")
        elif isinstance(v, (int, float)):
            return int(v)  
        raise ValueError("Invalid type for length, must be an integer or numeric string")

class GPU_response(ComputerPart):
    pcie_version: int
    power_consumption: int
    length: int 

    @field_validator('length', mode='before')
    @classmethod
    def convert_length(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")  
            try:
                return int(float(v)) 
            except ValueError:
                raise ValueError("Invalid type for length, must be an integer or numeric string")
        elif isinstance(v, (int, float)):
            return int(v)  
        raise ValueError("Invalid type for length, must be an integer or numeric string")


class PSU_response(ComputerPart):
    depth: int
    power: int

class Case_response(ComputerPart):
    case_format: str
