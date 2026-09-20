import json
from pathlib import Path

from ports import UserRepository


class JsonFileUserRepository(UserRepository):
    def __init__(self, path):
        self.path = Path(path)

    def load_all(self):
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save_all(self, users):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(users, file, indent=2)