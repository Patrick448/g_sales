class Product:
    def __init__(self, product_id: int, name: str, category: int, unit: str, price: float=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.unit = unit
        self.price = price
        self.quant = None
    
    def to_dict(self):
        product_dict = {"id": self.product_id,
                        "name": self.name,
                        "category": self.category,
                        "unit": self.unit,
                        "price": self.price,
                        "quant": self.quant}
        return product_dict

    