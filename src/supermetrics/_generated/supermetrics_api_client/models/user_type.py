from typing import Literal, cast

UserType = Literal["user"]

USER_TYPE_VALUES: set[UserType] = {
    "user",
}


def check_user_type(value: str) -> UserType:
    if value in USER_TYPE_VALUES:
        return cast(UserType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_TYPE_VALUES!r}")
