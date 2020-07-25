import json
from typing import Dict

class Order:
    def __init__(self, order_id, user_id, timestamp, total, items, user_name=None):
        self.id = order_id
        self.user_id = user_id
        self.user_name = user_name
        self.timestamp = timestamp
        self.total = total
        self.items = json.loads(items)

    def to_dict(self) -> Dict:
        order_dict = {'id': self.id,
                        'user_id': self.user_id,
                        'user_name': self.user_name,
                        'timeStamp': self.timestamp,
                        'total': self.total,
                        'items': self.items}
        return order_dict