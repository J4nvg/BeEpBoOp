from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import json
from models import CPU, Motherboard, RAM, Storage, Cooling, GraphicCard, PSU, Case

DATABASE_URL = "sqlite:///./hardware_db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

session = Session(engine)

def init_db(session: Session):
    with open("megekko_products-test.json") as f:
        data = json.load(f)
        for category in data:
            for i in range(0, 10):
                product = data[category][i]
                offer = product["offer"]
                specs = product["specs"]
                if category == "Processoren":
                    boost_clock = float(specs.get("Kloksnelheid Turbo", "0.0").split(" ")[0])
                    session.add(CPU(sku=product["sku"], name=product["name"],
                        price=offer["price"],
                        image_url=product["image"],
                        link=offer["url"],
                        socket=specs["Socket"], cores=specs["Processor Cores"], threads=specs["Processor aantal threads"], base_clock=float(specs["Processor Snelheid"].split(" ")[0]), boost_clock=boost_clock, power_consumption=specs["TDP (max)"]))

                if category == "Moederborden":
                    pcie5_slots = int(specs.get("PCI-E 5.0 x16", "0").split(" ")[0])
                    pcie4_x16 = int(specs.get("PCI-E 4.0 x16", "0").split(" ")[0])
                    pcie4_x4 = int(specs.get("PCI-E 4.0 x4", "0").split(" ")[0])
                    pcie3_x16 = int(specs.get("PCI-E 3.0 x16", "0").split(" ")[0])
                    pcie_express_x16 = int(specs.get("PCI Express x16 slots", "0").split(" ")[0])
                    pcie_express_x4 = int(specs.get("PCI Express x4 (Gen 1.x) slots", "0").split(" ")[0])

                    max_ram = specs.get("Max. Geheugen", "0")
                    if max_ram == "0":
                        max_ram = specs.get("Maximaal intern geheugen ondersteund door processor", "0")

                    session.add(Motherboard(
                        sku=product["sku"],
                        name=product["name"],
                        price=offer["price"],
                        image_url=product["image"],
                        link=offer["url"],
                        socket=specs["Socket"],
                        ram_slots=specs["Aantal geheugen slots"].split(" ")[0],
                        ram_type=specs["Geheugen type"],
                        max_ram=max_ram,
                        pcie5_slots=pcie5_slots,
                        pcie3_x16 = pcie3_x16,
                        pcie4_x16 = pcie4_x16,
                        pcie4_x4 = pcie4_x4,
                        pcie_express_x16 = pcie_express_x16,
                        pcie_express_x4 = pcie_express_x4,
                        m2_slots=specs["M.2 Slot Aantal"].split(" ")[0],
                        sata3_slots=specs["SATA-3 6Gbps"].split(" ")[0],
                        case_compatibility=specs["Form factor moederbord"]
                    ))
                if category == "Geheugen":
                    pass
                    #session.add(RAM(sku=product["sku"], ram_type=specs["type"], ram_slots=10, memory=10, XMP_support=10, AMDexpo_support=10))
                if category == "Videokaarten":
                    session.add(GraphicCard(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], pcie_version=specs["PCI Express versie"].split(" ")[1], length=specs["Lengte"].split(" ")[0], power_consumption=specs["Minimale voeding"].split(" ")[0]))
        session.commit()

init_db(session)
