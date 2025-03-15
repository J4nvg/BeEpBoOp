class motherboard():
    def __init__(self,
                 brand: str,
                 case_compatibility: str,
                 socket: str,
                 chipset: str,
                 memory_slots: int,
                 max_ram: int,
                 wifi_support: bool,
                 pcie4x16_slots: int,
                 pcie3x1_slots: int,
                 m2_slots: int):
        self.brand = brand
        self.case_compatibility = case_compatibility
        self.socket = socket
        self.chipset = chipset
        self.memory_slots = memory_slots
        self.max_ram = max_ram
        self.wifi_support = wifi_support
        self.pcie4x16_slots = pcie4x16_slots
        self.pcie3x1_slots = pcie3x1_slots
        self.m2_slots = m2_slots

    def serialize(self):
        return {
            'brand': self.brand,
            'case_compatibility': self.case_compatibility,
            'socket': self.socket,
            'chipset': self.chipset,
            'memory_slots': self.memory_slots,
            'max_ram': self.max_ram, 
            'wifi_support': self.wifi_support,
            'pcie4x16_slots': self.pcie4x16_slots,
            'pcie3x1_slots': self.pcie3x1_slots,
            'm2_slots': self.m2_slots
        }