import pytest

from services import create_user, list_users


class InMemoryUserRepository:
    def __init__(self, users=None):
        self.users = list(users or [])

    def load_all(self):
        return list(self.users)

    def save_all(self, users):
        self.users = list(users)


def test_create_user_assigns_id_and_saves():
    repo = InMemoryUserRepository()

    user = create_user(repo, " Alice ", "ALICE@example.com")

    assert user == {"name": "Alice", "email": "alice@example.com", "id": 1}
    assert repo.users == [user]


def test_create_user_rejects_duplicate_email():
    repo = InMemoryUserRepository(
        [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
    )

    with pytest.raises(ValueError, match="Email already exists"):
        create_user(repo, "Other", "alice@example.com")

    assert len(repo.users) == 1


def test_list_users_returns_stored_users():
    stored = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
    repo = InMemoryUserRepository(stored)

    assert list_users(repo) == stored