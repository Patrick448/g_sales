import json
from typing import Dict

class Order:
    def __init__(self, order_id, user, timestamp, total, items):
        self.id = order_id
        self.user = user
        self.timestamp = timestamp
        self.total = total
        self.items = json.loads(items)

    def to_dict(self) -> Dict:
        order_dict = {'id': self.id,
                        'user': self.user,
                        'timeStamp': self.timestamp,
                        'total': self.total,
                        'items': self.items}
        return order_dict