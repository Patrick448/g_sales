import sqlite3
import json
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger('app.db_manager')


class OrderDBManager:
    DATABASE = "orders.db"

    @classmethod
    def create_table_orders(cls):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS orders (id integer primary key, user integer, date integer, total real, items text)")
        logger.info(f"Table orders created in {cls.DATABASE} if it does not exist")
        connection.commit()
        connection.close()

    @classmethod
    def save_order(cls, user: int, date, items, total):

        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO orders (user, date, total, items) VALUES (?, ?, ?, ?)",
                       (user, date, total, json.dumps(items)))
        logger.info(f"Saving order to {cls.DATABASE}. User: {user}.")

        connection.commit()
        connection.close()

    @classmethod
    def get_all_orders(cls) -> List[Tuple]:

        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        logger.info(f"Getting all orders from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return orders

    @classmethod
    def get_all_orders_by_user(cls, user_id: int) -> List[Tuple]:

        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders WHERE user=?", (user_id,))
        orders = cursor.fetchall()

        logger.info(f"Getting all orders from {cls.DATABASE} by user {user_id}")

        connection.commit()
        connection.close()

        return orders
        

    @classmethod
    def get_order_by_date(cls, user_id: int, time_stamp: int = None, time_from: int = None, time_to: int = None) -> \
            List[Tuple]:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        if time_stamp is not None:
            cursor.execute("SELECT * FROM orders WHERE user=? AND date=?", (user_id, time_stamp))
        elif time_from is not None and time_to is not None:
            cursor.execute("SELECT * FROM orders WHERE user=? AND date>=? AND date<=?", (user_id, time_from, time_to))

        results = cursor.fetchall()

        logger.info(f'''Getting all orders from {cls.DATABASE} by user 
                    {user_id} {f'in time {time_stamp}' if time_stamp else f'from {time_from} to {time_to}'}''')
        connection.commit()
        connection.close()

        return results


    @classmethod
    def get_order_by_id(cls, user_id: int, order_id: int) -> List[Tuple]:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM orders WHERE user=? AND id=?", (user_id, order_id))
        results = cursor.fetchall()

        logger.info(f"Getting all orders from {cls.DATABASE} by user {user_id} with id {order_id}")
        connection.commit()
        connection.close()

        return results

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


class ProductDBManager:
    DATABASE = "products.db"

    @classmethod
    def create_table_products(cls):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS products (id integer primary key, name text, category integer, unit text)")
        logger.info(f"Table products created in {cls.DATABASE} if it does not exist")
        connection.commit()

        connection.close()

    @classmethod
    def create_table_available(cls):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS available (id integer, price real)")
        logger.info(f"Table available created in {cls.DATABASE} if it does not exist")
        connection.commit()
        connection.close()

    @classmethod
    def add_product(cls, name, category, unit):

        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO products (name, category, unit) VALUES (?, ?, ?)",
                       (name, category, unit))
        logger.info(f"Saving product to {cls.DATABASE}. Product: {name}")

        connection.commit()
        connection.close()

    @classmethod
    def get_product(cls, product_id: int):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()

        logger.info(f"Getting product from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return product

    @classmethod
    def get_all_products(cls) -> List[Dict]:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        products_dict_list = []

        for product in products:
            products_dict_list.append({"id": product[0],
                                       "name": product[1],
                                       "category": product[2],
                                       "unit": product[3],
                                       })

        logger.info(f"Getting all products from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return products

        return products_dict_list

    @classmethod
    def add_avilable_product(cls, id: int, price: float):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM products WHERE id=?", (id,))
        product = cursor.fetchone()

        cursor.execute("SELECT * FROM available WHERE id=?", (id,))
        available_product = cursor.fetchone()

        if product and not available_product:
            cursor.execute(f"INSERT INTO available (id, price) VALUES (?, ?)", (id, price))
            logger.info(f"Product {product[1]} inserted into available list")

        elif product:
            logger.warning(f"Failed. Product {product[1]} already inserted into available list")

        connection.commit()
        connection.close()


    @classmethod
    def get_available_products(cls) -> List[Dict]:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            """SELECT products.id, name, category, unit, price 
            FROM products JOIN available on products.id = available.id""")
        products = cursor.fetchall()

        products_dict_list = []

        for product in products:
            products_dict_list.append({"id": product[0],
                                       "name": product[1],
                                       "category": product[2],
                                       "unit": product[3],
                                       "price": product[4]
                                       })

        logger.info(f"Getting all available products from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return products

        return products_dict_list


class UserDBManager:
    DATABASE = "users.db"

    @classmethod
    def create_table_user(cls):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id integer primary key, email text, name text, level integer, password text)")
        logger.info(f"Table users created in {cls.DATABASE} if it does not exist")
        connection.commit()

        connection.close()

    @classmethod
    def add_user(cls, email: str, name: str, level: int, password: str):

        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (email, name, level, password) VALUES (?, ?, ?, ?)",
                       (email, name, level, password))
        logger.info(f"Saving user to {cls.DATABASE}. User: {email}")

        connection.commit()
        connection.close()

    @classmethod
    def get_user(cls, id: int):
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        user = cursor.fetchone()

        logger.info(f"Getting user from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return user

    @classmethod
    def get_user_by_email(cls, email: str) -> Dict:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        logger.info(f"Getting user from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return user


    @classmethod
    def get_all_users(cls) -> List[Tuple]:
        connection = sqlite3.connect(cls.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        logger.info(f"Getting all users from {cls.DATABASE}")
        connection.commit()
        connection.close()

        return users

