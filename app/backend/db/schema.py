from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 

engine = create_engine("sqlite:///hardware_parts.db", echo=True)
Base = declarative_base()

class CPU(Base):
    __tablename__ = 'cpus'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Socket -> MOTHERBOARD
    socket = Column(String)
    # Support -> RAM
    XMP_support = Column(Boolean)
    AMDexpo_support = Column(Boolean)
    # Power Consumption -> PSU
    power_consumption = Column(Integer)

class GraphicCard(Base):
    __tablename__ = 'gpus'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # PCI-E Version -> Motherboard 
    pcie_version = Column(Float)
    # Power Consumption -> PSU
    power_consumption = Column(Integer)
    # Length (mms) -> CASE
    length = Column(Integer)

class Motherboard(Base):
    __tablename__ = 'motherboards'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Case format -> CASE
    case_compatibility = Column(String)
    # Socket -> CPU
    socket = Column(String)
    # Info for -> RAM
    ram_slots = Column(Integer)
    max_ram = Column(Integer)
    ram_type = Column(String)
    # Nr of PCI-E slots -> GPU (other possibly)
    pcie5_slots = Column(Integer)
    pcie4_slots = Column(Integer)
    pcie3_slots = Column(Integer)
    # Storage slots -> STORAGE
    m2_slots = Column(Integer)
    sata3_slots = Column(Integer)

class RAM(Base):
    __tablename__ = 'rams'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Type of RAM -> MOTHERBOAD
    ram_type = Column(String)
    # Number of occupied slots -> MOTHERBOARD
    ram_slots = Column(Integer)
    # Amount of RAM (gb) -> MOTHERBOARD
    total_memory = Column(Integer) 
    # XMP support -> CPU
    XMP_support = Column(Boolean)
    # AMD EXPO support -> CPU
    AMDexpo_support = Column(Boolean)

class Storage(Base):
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Type of storage -> MOTHERBOARd
    storage_type = Column(String)


cooling_socket_association = Table(
    'cooling_socket', 
    Base.metadata,
    Column('cooling_id', Integer, ForeignKey('coolings.id'), ),
    Column('socket_id', Integer, ForeignKey('sockets.id'), )
)

class Cooling(Base):
    __tablename__ = 'coolings'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Number of fans -> CASE
    fans_number = Column(Integer)
    # Radiator size -> CASE
    radiator_size = Column(Integer)
    # Power consumption -> PSU
    power_consumption = Column(Integer)
    sockets = relationship('Socket', secondary=cooling_socket_association, back_populates='coolers') 


class Socket(Base):
    __tablename__ = 'sockets'
    id = Column(Integer, primary_key=True)
    # Type of supported socket -> MOTHERBOARD
    socket_type = Column(String)
    coolers = relationship('Cooling', secondary=cooling_socket_association, back_populates='sockets') 


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Case format -> MOTHERBOARD
    case_format = Column(String)
    # Max GPU size -> GPU
    max_gpu_size = Column(Integer)
    # Max pump size -> COOLING
    max_pump_size = Column(Integer)
    # Max fans size -> COOLING
    max_fans_size = Column(Integer)
    # Max PSU lenght -> PSU
    max_psu_length = Column(Integer)


class PSU(Base):
    __tablename__ = 'psus'
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    # Depth of the psu -> CASE
    length = Column(Integer)
    # Powers -> EVERYTHING
    power = Column(Integer)

# Create the table
Base.metadata.create_all(engine)
