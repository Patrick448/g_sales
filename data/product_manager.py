from data.product import Product
from utils.db_manager import ProductDBManager
from typing import List

class ProductManager:
    @classmethod
    def add_product(cls, name: str, category: int, unit: str):
        ProductDBManager.add_product(name, category, unit)
    
    @classmethod
    def get_product(product_id: int) -> Product:
        raw_product = ProductDBManager.get_product(product_id)
        return Product(*raw_product)
    
    @classmethod
    def get_all_products(cls) -> List[Product]:
        raw_products = ProductDBManager.get_all_products()
        products = [Product(*raw_product) for raw_product in raw_products]
        return products
    
    @classmethod
    def add_available_product(cls, id: int, price: float):
        ProductDBManager.add_avilable_product(id, price)

    @classmethod
    def get_available_products(cls):
        raw_products = ProductDBManager.get_available_products()
        products = [Product(*raw_product) for raw_product in raw_products]
        return products
    
    @classmethod
    def delete_all_available_products(cls):
        ProductDBManager.delete_all_available_products()

    @classmethod
    def get_all_products_full(cls):
        raw_products = ProductDBManager.get_all_products_full()
        products = [Product(*raw_product) for raw_product in raw_products]
        
        return products

    
    
