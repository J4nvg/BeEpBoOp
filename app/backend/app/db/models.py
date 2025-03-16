from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite+pysqlite:///hardware_db.db', echo=True)
    
class Base(DeclarativeBase):
    pass

class CPU(Base):
    __tablename__ = 'cpus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''MOTHERBOARD'''
    socket: Mapped[str]
    '''RAM'''
    XMP_support: Mapped[bool]
    AMDexpo_support: Mapped[bool]
    '''PSU (WATTS)'''
    power_consumption: Mapped[int] 

class GraphicCard(Base):
    __tablename__ = 'gpus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''MOTHERBOARD'''
    pcie_version: Mapped[float]
    '''PSU (WATTS)'''
    power_consumption: Mapped[int]
    '''LENGTH (MMS)'''
    length: Mapped[int]

class Motherboard(Base):
    __tablename__ = 'motherboards'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''CASE'''
    case_compatibility: Mapped[str]
    '''CPU'''
    socket: Mapped[str]
    '''RAM'''
    ram_slots: Mapped[int]
    max_ram: Mapped[int]
    ram_type: Mapped[str]
    '''GPU (other)'''
    pcie5_slots: Mapped[int]
    pcie4_slots: Mapped[int]
    pcie3_slots: Mapped[int]
    '''STORAGE'''
    m2_slots: Mapped[int]
    sata3_slots: Mapped[int]

class RAM(Base):
    __tablename__ = 'rams'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''MOTHERBOARD'''
    ram_type: Mapped[str]
    ram_slots: Mapped[int]
    memory: Mapped[int]
    '''CPU'''
    XMP_support: Mapped[bool]
    AMDexpo_support: Mapped[bool]

class Storage(Base):
    __tablename__ = 'storages'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''MOTHERBOARD'''
    storage_type: Mapped[str]

cooling_socket_rel = Table(
    'cooling_socket', 
    Base.metadata,
    Column('cooling_id', Integer, ForeignKey('coolings.id'), ),
    Column('socket_id', Integer, ForeignKey('sockets.id'), )
)

class Cooling(Base):
    __tablename__ = 'coolings'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''CASE'''
    number_of_fans: Mapped[int]
    fan_diamater: Mapped[int] #(MMS)
    '''PSU (WATTS)'''
    power_consumption: Mapped[int]
    '''SOCKETS'''
    sockets = relationship('Socket', secondary=cooling_socket_rel, back_populates='coolings')    

class Socket(Base):
    __tablename__ = 'sockets'
    id: Mapped[int] = mapped_column(primary_key=True)
    '''MOTHERBOARD'''
    socket_type: Mapped[str]
    '''COOLINGS'''
    coolings = relationship('Cooling', secondary=cooling_socket_rel, back_populates='sockets')    

class Case(Base):
    __tablename__ = 'cases'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''MOTHERBOARD'''
    case_format: Mapped[str]
    '''GPU (MMS)'''
    max_gpu_size: Mapped[int]
    '''COOLING (MMS)'''
    max_pump_size: Mapped[int]
    max_fans_size: Mapped[int]
    '''PSU (MMS)'''
    max_psu_lenght: Mapped[int]

class PSU(Base):
    __tablename__ = 'psus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True)
    '''CASE (MMS)'''
    depth: Mapped[int]
    '''EVERYTHING'''
    power: Mapped[int]


Base.metadata.create_all(engine)
