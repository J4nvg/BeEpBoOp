class CPU():
    def __init__(self,
                brand: str,
                series: str,
                model: str,
                speed: float,
                clock_speed: float,
                cores: int,
                integrated_graphics: str,
                ean_number: int,
                vendor_code: str):
        self.brand = brand
        self.series = series
        self.model = model
        self.speed = speed
        self.clock_speed = clock_speed
        self.cores = cores
        self.integrated_graphics = integrated_graphics
        self.ean_number = ean_number
        self.vendor_code = vendor_code
    
    def serialize(self):
        return {
            'brand': self.brand,
            'series': self.series,
            'model': self.model,
            'speed': self.speed,
            'clock_speed': self.clock_speed,
            'cores': self.cores, 
            'integrated_graphics': self.integrated_graphics,
            'ean_number': self.ean_number, 
            'vendor_code': self.vendor_code
        }
