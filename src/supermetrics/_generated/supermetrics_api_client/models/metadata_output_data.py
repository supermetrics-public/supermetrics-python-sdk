from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_output_data_functions import MetadataOutputDataFunctions
    from ..models.metadata_output_data_output_data_types import MetadataOutputDataOutputDataTypes
    from ..models.metadata_output_data_rules import MetadataOutputDataRules


T = TypeVar("T", bound="MetadataOutputData")


@_attrs_define
class MetadataOutputData:
    """Metadata for custom field transformations.

    Attributes:
        rules (MetadataOutputDataRules | Unset): Matching rules available for condition and lookup steps.
        functions (MetadataOutputDataFunctions | Unset): Wrapper holding the available transformation functions.
        field_data_types (list[str] | Unset): Field data types that can be used for transformations. Example:
            ['string.text.value'].
        output_data_types (MetadataOutputDataOutputDataTypes | Unset): Wrapper holding the available output data types.
        data_transformation_steps_limit (int | Unset): Maximum number of transformation steps allowed for the team.
            Example: 10.
    """

    rules: MetadataOutputDataRules | Unset = UNSET
    functions: MetadataOutputDataFunctions | Unset = UNSET
    field_data_types: list[str] | Unset = UNSET
    output_data_types: MetadataOutputDataOutputDataTypes | Unset = UNSET
    data_transformation_steps_limit: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rules: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        functions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.functions, Unset):
            functions = self.functions.to_dict()

        field_data_types: list[str] | Unset = UNSET
        if not isinstance(self.field_data_types, Unset):
            field_data_types = self.field_data_types

        output_data_types: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output_data_types, Unset):
            output_data_types = self.output_data_types.to_dict()

        data_transformation_steps_limit = self.data_transformation_steps_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rules is not UNSET:
            field_dict["rules"] = rules
        if functions is not UNSET:
            field_dict["functions"] = functions
        if field_data_types is not UNSET:
            field_dict["field_data_types"] = field_data_types
        if output_data_types is not UNSET:
            field_dict["output_data_types"] = output_data_types
        if data_transformation_steps_limit is not UNSET:
            field_dict["data_transformation_steps_limit"] = data_transformation_steps_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_output_data_functions import MetadataOutputDataFunctions
        from ..models.metadata_output_data_output_data_types import MetadataOutputDataOutputDataTypes
        from ..models.metadata_output_data_rules import MetadataOutputDataRules

        d = dict(src_dict)
        _rules = d.pop("rules", UNSET)
        rules: MetadataOutputDataRules | Unset
        if isinstance(_rules, Unset):
            rules = UNSET
        else:
            rules = MetadataOutputDataRules.from_dict(_rules)

        _functions = d.pop("functions", UNSET)
        functions: MetadataOutputDataFunctions | Unset
        if isinstance(_functions, Unset):
            functions = UNSET
        else:
            functions = MetadataOutputDataFunctions.from_dict(_functions)

        field_data_types = cast(list[str], d.pop("field_data_types", UNSET))

        _output_data_types = d.pop("output_data_types", UNSET)
        output_data_types: MetadataOutputDataOutputDataTypes | Unset
        if isinstance(_output_data_types, Unset):
            output_data_types = UNSET
        else:
            output_data_types = MetadataOutputDataOutputDataTypes.from_dict(_output_data_types)

        data_transformation_steps_limit = d.pop("data_transformation_steps_limit", UNSET)

        metadata_output_data = cls(
            rules=rules,
            functions=functions,
            field_data_types=field_data_types,
            output_data_types=output_data_types,
            data_transformation_steps_limit=data_transformation_steps_limit,
        )

        metadata_output_data.additional_properties = d
        return metadata_output_data

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
