from adapters.json_file_repo import JsonFileUserRepository


def test_load_all_returns_empty_list_when_file_missing(tmp_path):
    repo = JsonFileUserRepository(tmp_path / "users.json")

    assert repo.load_all() == []


def test_save_all_then_load_all_roundtrip(tmp_path):
    repo = JsonFileUserRepository(tmp_path / "users.json")
    users = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

    repo.save_all(users)

    assert repo.load_all() == users