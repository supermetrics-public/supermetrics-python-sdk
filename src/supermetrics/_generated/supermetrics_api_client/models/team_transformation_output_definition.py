from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.condition_step import ConditionStep
    from ..models.function_step import FunctionStep
    from ..models.lookup_step import LookupStep


T = TypeVar("T", bound="TeamTransformationOutputDefinition")


@_attrs_define
class TeamTransformationOutputDefinition:
    """Wrapper holding the ordered transformation steps.

    Attributes:
        items (list[ConditionStep | FunctionStep | LookupStep] | Unset): The ordered pipeline of transformation steps.
            Example: [{'type': 'function', 'name': 'upper_case', 'arguments': [{'name': 'value', 'value': {'type':
            'data_source_field', 'value': 'platform'}}]}].
    """

    items: list[ConditionStep | FunctionStep | LookupStep] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.function_step import FunctionStep
        from ..models.lookup_step import LookupStep

        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item: dict[str, Any]
                if isinstance(items_item_data, FunctionStep):
                    items_item = items_item_data.to_dict()
                elif isinstance(items_item_data, LookupStep):
                    items_item = items_item_data.to_dict()
                else:
                    items_item = items_item_data.to_dict()

                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.condition_step import ConditionStep
        from ..models.function_step import FunctionStep
        from ..models.lookup_step import LookupStep

        d = dict(src_dict)
        _items = d.pop("items", UNSET)
        items: list[ConditionStep | FunctionStep | LookupStep] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:

                def _parse_items_item(data: object) -> ConditionStep | FunctionStep | LookupStep:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_transformation_step_type_0 = FunctionStep.from_dict(data)

                        return componentsschemas_transformation_step_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_transformation_step_type_1 = LookupStep.from_dict(data)

                        return componentsschemas_transformation_step_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transformation_step_type_2 = ConditionStep.from_dict(data)

                    return componentsschemas_transformation_step_type_2

                items_item = _parse_items_item(items_item_data)

                items.append(items_item)

        team_transformation_output_definition = cls(
            items=items,
        )

        team_transformation_output_definition.additional_properties = d
        return team_transformation_output_definition

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
