from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, name, level, password):
        self.id = id
        self.email = email
        self.name = name
        self.level = level
        self.password = password

    def __repr__(self):
        return f"<User: {self.name}>"

    def get_id(self):
        return self.id

    @property
    def to_dict(self):
        user_dict = {'id': self.id,
                     'email': self.email,
                     'name': self.name,
                     'level': self.level}

        return user_dict
