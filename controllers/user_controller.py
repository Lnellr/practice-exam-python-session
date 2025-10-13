from models.user import User

class UserController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_user(self, username, email, role) -> int:
        user = User(username, email, role)
        return self.db.add_user(user)

    def get_user(self, user_id) -> User | None:
        return self.db.get_user_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.db.get_all_users()

    def update_user(self, user_id, **kwargs) -> bool:
        return self.db.update_user(user_id, **kwargs)

    def delete_user(self, user_id) -> bool:
        return self.db.delete_user(user_id)

    def get_user_tasks(self, user_id) -> list:
        return self.db.get_tasks_by_user(user_id)