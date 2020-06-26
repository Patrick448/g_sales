import sqlite3
import json
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger('app.db_manager')


class OrderDBManager:
    ORDERS_DATABASE = "orders.db"

    @classmethod
    def create_table_orders(cls):
        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS orders (id integer primary key, user text, date integer, total real, items text)")
        logger.info(f"Table orders created in {cls.ORDERS_DATABASE} if it does not exist")
        connection.commit()
        connection.close()

    @classmethod
    def save_order(cls, user: str, order: Dict):

        date = order["timeStamp"]
        total = order["total"]
        items_str = json.dumps(order["items"])

        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO orders (user, date, total, items) VALUES (?, ?, ?, ?)",
                       (user, date, total, items_str))
        logger.info(f"Saving order to {cls.ORDERS_DATABASE}. User: {user} Order: {order}")

        connection.commit()
        connection.close()

    @classmethod
    def get_all_orders(cls) -> List[Dict]:

        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        orders_dict_list = []

        for order in orders:
            orders_dict_list.append({"order_id": order[0],
                                     "user": order[1],
                                     "timeStamp": order[2],
                                     "total": order[3],
                                     "items": json.loads(order[4])
                                     })

        logger.info(f"Getting all orders from {cls.ORDERS_DATABASE}")
        connection.commit()
        connection.close()

        return orders_dict_list

    @classmethod
    def get_all_orders_by_user(cls, user_id: str) -> List[Dict]:

        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders WHERE user=?", (user_id,))
        orders = cursor.fetchall()

        logger.info(f"Getting all orders from {cls.ORDERS_DATABASE} by user {user_id}")

        connection.commit()
        connection.close()

        return cls.db_result_to_order_dict_list(orders)

    @classmethod
    def get_order_by_date(cls, user_id: str, time_stamp: int=None, time_from: int=None, time_to: int=None) -> List[Dict]:
        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        if time_stamp is not None:
            cursor.execute("SELECT * FROM orders WHERE user=? AND date=?", (user_id, time_stamp))
        elif time_from is not None and time_to is not None:
            cursor.execute("SELECT * FROM orders WHERE user=? AND date>=? AND date<=?", (user_id, time_from, time_to))

        results = cursor.fetchall()

        logger.info(f'''Getting all orders from {cls.ORDERS_DATABASE} by user 
                    {user_id} {f'in time {time_stamp}' if time_stamp else f'from {time_from} to {time_to}'}''')
        connection.commit()
        connection.close()

        return cls.db_result_to_order_dict_list(results)

    @classmethod
    def get_order_by_id(cls, user_id: str, order_id: int) -> List[Dict]:
        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders WHERE user=? AND id=?", (user_id, order_id))
        results = cursor.fetchall()

        logger.info(f"Getting all orders from {cls.ORDERS_DATABASE} by user {user_id} with id {order_id}")
        connection.commit()
        connection.close()

        return cls.db_result_to_order_dict_list(results)

    @staticmethod
    def db_result_to_order_dict_list(results):

        dict_list = []

        for result in results:
            dict_list.append({"order_id": result[0],
                                     "user": result[1],
                                     "timeStamp": result[2],
                                     "total": result[3],
                                     "items": json.loads(result[4])
                                     })
        return dict_list
