from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import json
from models import CPU, Motherboard, RAM, Storage, Cooling, GraphicCard, PSU, Case

DATABASE_URL = "sqlite:///../hardware_db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

session = Session(engine)

def init_db(session: Session):
    with open("megekko_products-psu.json") as f:
        data = json.load(f)
        for category in data:
            for i in range(0, 10):
                product = data[category][i]
                offer = product["offer"]
                specs = product["specs"]
                depth = specs.get("Diepte", "0")
                session.add(PSU(sku=product["sku"], name=product["name"], image_url=product["image"], price=offer["price"], link=offer["url"], depth=depth.split(" ")[0], power=specs["Vermogen (continu)"]))
        session.commit()

#init_db(session)
