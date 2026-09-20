from domain import validate_user, ensure_email_available, next_user_id
from ports import UserRepository


def create_user(repo: UserRepository, name, email):
    users = repo.load_all()
    user = validate_user(name, email)
    ensure_email_available(users, user["email"])

    user["id"] = next_user_id(users)
    users.append(user)
    repo.save_all(users)

    return user


def list_users(repo: UserRepository):
    return repo.load_all()