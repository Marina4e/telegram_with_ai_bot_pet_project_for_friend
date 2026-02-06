import os


def get_allowed_user_id() -> int | None:
    value = os.getenv("ALLOWED_USER_ID", "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def is_allowed(user_id: int) -> bool:
    allowed_id = get_allowed_user_id()
    if allowed_id is None:
        return True  # доступ відкритий для всіх
    return user_id == allowed_id
