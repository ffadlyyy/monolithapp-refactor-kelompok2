from adapters.json_file_repo import JsonFileUserRepository
from services import create_user

DATA_FILE = "users.json"


def main():
    repo = JsonFileUserRepository(DATA_FILE)

    name = input("Name: ")
    email = input("Email: ")

    try:
        user = create_user(repo, name, email)
        print(f"User created: {user}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()