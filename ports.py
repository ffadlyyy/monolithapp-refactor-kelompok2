from typing import Protocol


class UserRepository(Protocol):
    def load_all(self) -> list[dict]:
        ...

    def save_all(self, users: list[dict]) -> None:
        ...