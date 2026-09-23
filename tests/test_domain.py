import pytest

from domain import validate_user, ensure_email_available, next_user_id


def test_validate_user_normalizes_input():
    user = validate_user(" Alice ", "ALICE@example.com")

    assert user == {"name": "Alice", "email": "alice@example.com"}


def test_validate_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        validate_user("Alice", "invalid-email")


def test_validate_user_rejects_empty_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_user("   ", "alice@example.com")


def test_ensure_email_available_rejects_duplicate():
    users = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

    with pytest.raises(ValueError, match="Email already exists"):
        ensure_email_available(users, "alice@example.com")


def test_next_user_id():
    assert next_user_id([]) == 1
    assert next_user_id([{"id": 1}, {"id": 2}]) == 3

def test_ensure_email_available_accepts_unique_email():
    users = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

    ensure_email_available(users, "bob@example.com")


def test_next_user_id_with_three_users():
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]

    assert next_user_id(users) == 4