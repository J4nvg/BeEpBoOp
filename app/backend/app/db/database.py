from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import json
from models import CPU, Motherboard, RAM, Storage, Cooling, GraphicCard, PSU, Case

DATABASE_URL = "sqlite:///hardware_db.db"
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
                    session.add(CPU(sku=product["sku"], name=product["name"], image_url=product["image"],
                        link=offer["url"],
                        price=offer["price"],socket=specs["Socket"], cores=specs["Processor Cores"], threads=specs["Processor aantal threads"], base_clock=float(specs["Processor Snelheid"].split(" ")[0]), boost_clock=boost_clock, power_consumption=specs["TDP (max)"]))

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
                        image_url=product["image"],
                        link=offer["url"],
                        price=offer["price"],
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
                    xmp_support = specs.get("XMP ondersteuning", False)
                    if xmp_support == "✓︎":
                        xmp_support = True
                    amd_expo_support = specs.get("AMD EXPO ondersteuning", False)
                    if amd_expo_support == "✓︎":
                        amd_expo_support = True
                    session.add(RAM(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], ram_type=specs["Geheugen Type"], ram_slots=specs["Modules (aantal)"], memory=specs["Geheugen capaciteit"], XMP_support=xmp_support, AMDexpo_support=amd_expo_support))
                if category == "Videokaarten":
                    session.add(GraphicCard(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], pcie_version=specs["PCI Express versie"].split(" ")[1], length=specs["Lengte"].split(" ")[0], power_consumption=specs["Minimale voeding"].split(" ")[0]))
                if category == "Behuizingen en meer":
                    max_fan_size_achter = specs.get("Geïnstalleerde Fans achterkant", "").split(" ")[0].replace("x", "")
                    max_fan_size_zij = specs.get("Geïnstalleerde Fans zijkant", "").split(" ")[0].replace("x", "")
                    max_fan_size_onder = specs.get("Geïnstalleerde Fans onderkant", "").split(" ")[0].replace("x", "")
                    max_fans_size = max_fan_size_achter + max_fan_size_zij + max_fan_size_onder
                    max_pump_size = specs.get("Maximum CPU cooler hoogte", "")
                    max_psu_length = specs.get("Maximum PSU lengte", "")
                    session.add(Case(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], case_format=specs["Max moederbord formaat"], max_gpu_size=specs["Maximum grafische kaart lengte"], max_pump_size=max_pump_size, max_fans_size=max_fans_size, max_psu_length=max_psu_length))
                if category == "Koeling":
                    power_consumption = specs.get("Stroomverbruik (typisch)", "0.0").split(" ")[0]
                    number_fans = specs.get("Aantal Ventilatoren", "0").split(" ")[0]
                    session.add(Cooling(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], number_of_fans=number_fans, power_consumption=power_consumption, fan_diamater=specs["Fan Diameter"]))
                if category == "SSD (Solid state drive)":
                    interface = specs.get("Interface", "")
                    storage_type = interface.split(" ")[2]
                    session.add(Storage(sku=product["sku"], name=product["name"], image_url=product["image"], link=offer["url"], price=offer["price"], storage_type=storage_type, capacity=specs["SSD Opslagcapaciteit"]))
        session.commit()

init_db(session)
