from utils.db_manager import UserDBManager
from data.user import User
from typing import List


class UserManager:

    @classmethod
    def get_all_users(cls) -> List[User]:
        raw_users = UserDBManager.get_all_users()
        users = [User(*raw_user) for raw_user in raw_users]

        return users

    @classmethod
    def get_user(cls, user_id: int = None, email: str = None) -> User:
        if user_id:
            user_raw = UserDBManager.get_user(user_id)
            return User(*user_raw) if user_raw else None
        elif email:
            user_raw = UserDBManager.get_user_by_email(email)
            return User(*user_raw) if user_raw else None

        return None

    @classmethod
    def add_user(cls, email: str, name: str, level: int, password: str):
        UserDBManager.add_user(email, name, level, password)
