from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """Machine- and human-readable detail for a failed request.

    Attributes:
        code (str): Stable, screaming-snake-case identifier for the error condition. Clients should branch on this, not
            on `message`. Common values include BAD_REQUEST, UNAUTHORIZED, FORBIDDEN, NOT_FOUND, CONFLICT_ERROR,
            PERMISSION_ERROR, UNPROCESSABLE_ENTITY, UNPROCESSABLE_CONTENT, TOO_MANY_REQUESTS, INTERNAL_SERVER_ERROR,
            DUPLICATION_FAILED, SERVICE_UNAVAILABLE; domains may define additional codes.
             Example: BAD_REQUEST.
        message (str): Short, human-readable summary of the error. Example: The request was invalid..
        description (str | Unset): Optional longer explanation specific to this occurrence. Example: The field
            'display_name' must not be empty..
    """

    code: str
    message: str
    description: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        description = d.pop("description", UNSET)

        error = cls(
            code=code,
            message=message,
            description=description,
        )

        return error
