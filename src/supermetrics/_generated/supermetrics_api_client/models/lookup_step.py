from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.lookup_step_type import LookupStepType, check_lookup_step_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.definition_value import DefinitionValue
    from ..models.lookup_step_map import LookupStepMap


T = TypeVar("T", bound="LookupStep")


@_attrs_define
class LookupStep:
    """A transformation step that maps input values to output values using a key/value lookup table and a matching rule.

    Attributes:
        type_ (LookupStepType): Discriminator value identifying this step as a lookup step. Example: lookup.
        rule (str): The matching rule applied when looking up a value (e.g. equals). Example: equals.
        map_ (LookupStepMap): Key/value mapping table used by the lookup. Example: {'1': '2', 'a': 'b'}.
        source (DefinitionValue | Unset): A value reference used in transformation steps. Depending on `type` the value
            is read from a data-source field, taken from the previous step's output, or supplied as a static literal.
            Example: {'type': 'data_source_field', 'value': 'platform'}.
        default (DefinitionValue | Unset): A value reference used in transformation steps. Depending on `type` the value
            is read from a data-source field, taken from the previous step's output, or supplied as a static literal.
            Example: {'type': 'data_source_field', 'value': 'platform'}.
        description (None | str | Unset): Optional free-text description of the transformation step.
    """

    type_: LookupStepType
    rule: str
    map_: LookupStepMap
    source: DefinitionValue | Unset = UNSET
    default: DefinitionValue | Unset = UNSET
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        rule = self.rule

        map_ = self.map_.to_dict()

        source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        default: dict[str, Any] | Unset = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "rule": rule,
                "map": map_,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if default is not UNSET:
            field_dict["default"] = default
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.definition_value import DefinitionValue
        from ..models.lookup_step_map import LookupStepMap

        d = dict(src_dict)
        type_ = check_lookup_step_type(d.pop("type"))

        rule = d.pop("rule")

        map_ = LookupStepMap.from_dict(d.pop("map"))

        _source = d.pop("source", UNSET)
        source: DefinitionValue | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = DefinitionValue.from_dict(_source)

        _default = d.pop("default", UNSET)
        default: DefinitionValue | Unset
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = DefinitionValue.from_dict(_default)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        lookup_step = cls(
            type_=type_,
            rule=rule,
            map_=map_,
            source=source,
            default=default,
            description=description,
        )

        lookup_step.additional_properties = d
        return lookup_step

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
