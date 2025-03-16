from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///../hardware_db.db', echo=True)
    
class Base(DeclarativeBase):
    pass

class CPU(Base):
    __tablename__ = 'cpus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''MOTHERBOARD'''
    socket: Mapped[str]
    '''PSU (WATTS)'''
    power_consumption: Mapped[int]
    cores: Mapped[int]
    threads: Mapped[int]
    base_clock: Mapped[float]
    boost_clock: Mapped[float]

class GraphicCard(Base):
    __tablename__ = 'gpus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name:  Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''MOTHERBOARD'''
    pcie_version: Mapped[int]
    '''PSU (WATTS)'''
    power_consumption: Mapped[int]
    '''LENGTH (MMS)'''
    length: Mapped[int]

class Motherboard(Base):
    __tablename__ = 'motherboards'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''CASE'''
    case_compatibility: Mapped[str]
    '''CPU'''
    socket: Mapped[str]
    '''RAM'''
    ram_slots: Mapped[int]
    max_ram: Mapped[int]
    ram_type: Mapped[str]
    '''GPU (other)'''
    pcie4_x16: Mapped[int]
    pcie4_x4: Mapped[int]
    pcie3_x16: Mapped[int]
    pcie_express_x16: Mapped[int]
    pcie_express_x4: Mapped[int]
    pcie5_slots: Mapped[int]
    '''STORAGE'''
    m2_slots: Mapped[int]
    sata3_slots: Mapped[int]

class RAM(Base):
    __tablename__ = 'rams'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
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
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''MOTHERBOARD'''
    storage_type: Mapped[str]
    capacity: Mapped[int]

cooling_socket_rel = Table(
    'cooling_socket',
    Base.metadata,
    Column('cooling_id', Integer, ForeignKey('coolings.id'), ),
    Column('socket_id', Integer, ForeignKey('sockets.id'), )
)

class Cooling(Base):
    __tablename__ = 'coolings'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
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
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''MOTHERBOARD'''
    case_format: Mapped[str]
    '''GPU (MMS)'''
    max_gpu_size: Mapped[int]
    '''COOLING (MMS)'''
    max_pump_size: Mapped[int]
    max_fans_size: Mapped[int]
    '''PSU (MMS)'''
    max_psu_length: Mapped[int]

class PSU(Base):
    __tablename__ = 'psus'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    price: Mapped[float]
    link: Mapped[str]
    image_url: Mapped[str]
    '''CASE (MMS)'''
    depth: Mapped[int]
    '''EVERYTHING'''
    power: Mapped[int]

#Base.metadata.create_all(engine)