import json
from typing import Dict

class Order:
    def __init__(self, order_id, user_id, timestamp, total, items, status=0, user_name=None):
        # TODO: fix this named and positional arguments problem/
        # the status arguments is always required, but the user_name is not/
        #  
        self.id = order_id
        self.user_id = user_id
        self.user_name = user_name
        self.timestamp = timestamp
        self.total = total
        self.items = json.loads(items)
        self.status = status

    def to_dict(self) -> Dict:
        order_dict = {'id': self.id,
                        'user_id': self.user_id,
                        'user_name': self.user_name,
                        'timeStamp': self.timestamp,
                        'total': self.total,
                        'items': self.items,
                        'status': self.status}
        return order_dict