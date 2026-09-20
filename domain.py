def validate_user(name, email):
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")

    if "@" not in email:
        raise ValueError("Invalid email")

    return {
        "name": name.strip(),
        "email": email.strip().lower(),
    }


def ensure_email_available(users, email):
    if any(existing["email"] == email for existing in users):
        raise ValueError("Email already exists")


def next_user_id(users):
    return len(users) + 1