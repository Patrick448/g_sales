import json
from typing import List, Dict


class DataManager:

    @staticmethod
    def save_order(order):
        with open('orders.json', 'r') as file:
            data_list = []
            data_list.extend(json.load(file))

        with open('orders.json', 'w') as file:
            data_list.append(order)
            json.dump(data_list, file)

    @staticmethod
    def get_all_orders():
        with open('orders.json', 'r') as file:
            data = file.read()

        return data

    @staticmethod
    def get_today_list() -> List[Dict]:
        today_list = [
            {"id": 0, "desc": "Banana", "price": "20.00"},
            {"id": 1, "desc": "Maçã", "price": "40.70"},
            {"id": 2, "desc": "Manga", "price": "50.60"},
            {"id": 3, "desc": "Laranja", "price": "25.00"},
            {"id": 4, "desc": "Batata", "price": "60.00"},
            {"id": 5, "desc": "Inhame", "price": "70.00"},
            {"id": 6, "desc": "Beterraba", "price": "30.00"},
            {"id": 7, "desc": "Cenoura", "price": "36.00"},
            {"id": 8, "desc": "Alface", "price": "2.00"},
            {"id": 9, "desc": "Couve", "price": "2.00"},
            {"id": 10, "desc": "Agrião", "price": "2.20"}]

        return today_list

