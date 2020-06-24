import sqlite3
import json
from typing import Dict, List


class OrderDBManager:
    ORDERS_DATABASE = "orders.db"

    @classmethod
    def create_table_orders(cls):
        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS orders (id integer primary key, user text, date integer, total real, items text)")

        connection.commit()
        connection.close()

    @classmethod
    def save_order(cls, user: str, order: Dict):

        date = order["timeStamp"]
        total = order["total"]
        items_str = json.dumps(order["items"])

        connection = sqlite3.connect(cls.ORDERS_DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO orders (user, date, total, items) VALUES (?, ?, ?, ?)", (user, date, total, items_str))

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
            orders_dict_list.append({"user": order[0], "date": order[1], "total": order[2], "order": json.load(order[3])})

        connection.commit()
        connection.close()

        return orders_dict_list
