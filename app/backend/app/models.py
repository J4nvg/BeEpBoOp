from pydantic import BaseModel
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

class Storage(ComputerPart):
    capacity: int
    speed: int
    cache: int
    form_factor: str

class Motherboard(ComputerPart):
    socket: str
    chipset: str
    form_factor: str
    memory_slots: int

class Cooler(ComputerPart):
    fan_rpm: int
    noise_level: int
    fan_size: int
    radiator_size: int

class GPU(ComputerPart):
    chipset: str
    memory: int
    core_clock: int
    boost_clock: int
    TDP: int

class PSU(ComputerPart):
    wattage: int
    efficiency: str
    modular: bool
    rating: str

class Case(ComputerPart):
    form_factor: str
    fans: int
    side_panel: str
    PSU: str
    radiator: str