from data.order import Order
from utils.db_manager import OrderDBManager
from typing import List

class OrderManager:
    @classmethod
    def save_order(cls, user: int, date: int, items: List, total: float, status: int):
        OrderDBManager.save_order(user, date, items, total, status)

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

    @classmethod
    def get_orders(cls, order_id: int = None, user_id: int = None, user_name:str = None,  time_stamp: int = None, time_from: int = None, time_to: int = None) -> List[Order]:
        raw_orders = OrderDBManager.get_orders(order_id=order_id, time_stamp=time_stamp, user_name = user_name, time_from=time_from, time_to=time_to)
        orders = [Order(*raw_order) for raw_order in raw_orders]
        return orders