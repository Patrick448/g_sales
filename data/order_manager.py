from data.order import Order
from utils.db_manager import OrderDBManager
from typing import List

class OrderManager:
    @classmethod
    def save_order(cls, user: int, date: int, items: List, total: float):
        OrderDBManager.save_order(user, date, items, total)

    @classmethod
    def get_all_orders(cls) -> List[Order]:
        raw_orders = OrderDBManager.get_all_orders()
        orders = [Order(*raw_order) for raw_order in raw_orders]
        return orders
    
    @classmethod
    def get_all_orders_by_user(cls, user_id: int) -> List[Order]:
        raw_orders = OrderDBManager.get_all_orders_by_user(user_id)
        orders = [Order(*raw_order) for raw_order in raw_orders]
        return orders

    @classmethod
    def get_orders_by_date(cls, user_id: int, time_stamp: int = None, time_from: int = None, time_to: int = None) -> List[Order]:
        raw_orders = OrderDBManager.get_order_by_date(user_id, time_stamp, time_from, time_to)
        orders = [Order(*raw_order) for raw_order in raw_orders]
        return orders

    @classmethod
    def get_order_by_id(cls, user_id: int, order_id: int) -> Order:
        raw_order = OrderDBManager.get_order_by_id(user_id, order_id)   
        return Order(*raw_order)