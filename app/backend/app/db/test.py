from sqlalchemy import create_engine, select
from models import *

from sqlalchemy.orm import Session

engine = create_engine('sqlite:///hardware_db.db', echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


print(f'setup complete')
session = Session(engine)
print(f'session open')
new_cpu = CPU(
    sku=2, 
    socket='AM4', 
    XMP_support=True, 
    AMDexpo_support=True, 
    power_consumption=95
)
print(f'Created new cpu {new_cpu}')
session.add(new_cpu)
print(f'Added new cpu to the session')
session.commit()
print(f'Commited new cpu to the session')

retrieved_cpu = select(CPU).where(CPU.sku == 2)
cpu = session.scalars(retrieved_cpu).one()
print(f'retrieved cpu')
print(f'-->{cpu.id, cpu.sku, cpu.socket}')
session.close()