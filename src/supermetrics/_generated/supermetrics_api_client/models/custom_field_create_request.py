from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_create_request_field_type import (
    CustomFieldCreateRequestFieldType,
    check_custom_field_create_request_field_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.condition_step import ConditionStep
    from ..models.custom_field_create_request_data_source_item import CustomFieldCreateRequestDataSourceItem
    from ..models.function_step import FunctionStep
    from ..models.lookup_step import LookupStep


T = TypeVar("T", bound="CustomFieldCreateRequest")


@_attrs_define
class CustomFieldCreateRequest:
    """Payload for creating a new custom field (field transformation).

    Attributes:
        display_name (str): User-facing name of the new custom field shown in the UI. Example: Spec Example Field.
        field_type (CustomFieldCreateRequestFieldType): Field kind: `dim` (dimension) or `met` (metric). Example: dim.
        data_type (str): Data type of the custom field (e.g. string.text.value, float.number.value, int.number.value,
            bool). Example: string.text.value.
        definition (list[ConditionStep | FunctionStep | LookupStep]): Ordered pipeline of transformation steps
            (function, lookup, or condition) used to compute the custom field. Example: [{'type': 'function', 'name':
            'upper_case', 'arguments': [{'name': 'value', 'value': {'type': 'data_source_field', 'value': 'platform'}}]}].
        data_source (list[CustomFieldCreateRequestDataSourceItem] | Unset): Data sources associated with the custom
            field. Each entry pairs a data source ID with an optional report type.
        description (str | Unset): Free-text description of the new custom field. Example: Temporary transformation for
            spec examples.
    """

    display_name: str
    field_type: CustomFieldCreateRequestFieldType
    data_type: str
    definition: list[ConditionStep | FunctionStep | LookupStep]
    data_source: list[CustomFieldCreateRequestDataSourceItem] | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.function_step import FunctionStep
        from ..models.lookup_step import LookupStep

        display_name = self.display_name

        field_type: str = self.field_type

        data_type = self.data_type

        definition = []
        for definition_item_data in self.definition:
            definition_item: dict[str, Any]
            if isinstance(definition_item_data, FunctionStep):
                definition_item = definition_item_data.to_dict()
            elif isinstance(definition_item_data, LookupStep):
                definition_item = definition_item_data.to_dict()
            else:
                definition_item = definition_item_data.to_dict()

            definition.append(definition_item)

        data_source: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_source, Unset):
            data_source = []
            for data_source_item_data in self.data_source:
                data_source_item = data_source_item_data.to_dict()
                data_source.append(data_source_item)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "field_type": field_type,
                "data_type": data_type,
                "definition": definition,
            }
        )
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.condition_step import ConditionStep
        from ..models.custom_field_create_request_data_source_item import CustomFieldCreateRequestDataSourceItem
        from ..models.function_step import FunctionStep
        from ..models.lookup_step import LookupStep

        d = dict(src_dict)
        display_name = d.pop("display_name")

        field_type = check_custom_field_create_request_field_type(d.pop("field_type"))

        data_type = d.pop("data_type")

        definition = []
        _definition = d.pop("definition")
        for definition_item_data in _definition:

            def _parse_definition_item(data: object) -> ConditionStep | FunctionStep | LookupStep:
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

            definition_item = _parse_definition_item(definition_item_data)

            definition.append(definition_item)

        _data_source = d.pop("data_source", UNSET)
        data_source: list[CustomFieldCreateRequestDataSourceItem] | Unset = UNSET
        if _data_source is not UNSET:
            data_source = []
            for data_source_item_data in _data_source:
                data_source_item = CustomFieldCreateRequestDataSourceItem.from_dict(data_source_item_data)

                data_source.append(data_source_item)

        description = d.pop("description", UNSET)

        custom_field_create_request = cls(
            display_name=display_name,
            field_type=field_type,
            data_type=data_type,
            definition=definition,
            data_source=data_source,
            description=description,
        )

        custom_field_create_request.additional_properties = d
        return custom_field_create_request

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
