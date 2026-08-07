from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Set as AbstractSet
from dataclasses import dataclass, field
from typing import NewType, cast

from .errors import component_names
from .types import Component, ComponentType, EntityId

RowIndex = NewType('RowIndex', int)


class InvalidRow(IndexError):
    def __init__(self, row: RowIndex, max_row: int) -> None:
        super().__init__(
            f'Row {row} is outside the valid range '
            f'0..{max_row}'
        )
        self.row = row
        self.max_row = max_row


class InvalidSignature(ValueError):
    def __init__(
        self,
        missing: AbstractSet[ComponentType],
        unexpected: AbstractSet[ComponentType],
    ) -> None:
        super().__init__(
            'Components do not match signature: '
            f'missing={component_names(missing)}, '
            f'unexpected={component_names(unexpected)}'
        )
        self.missing = missing
        self.unexpected = unexpected


@dataclass(eq=False, slots=True)
class Archetype:
    signature: frozenset[ComponentType]
    entities: list[EntityId] = field(
        default_factory=list,
        init=False,
        repr=False,
    )
    components: dict[ComponentType, list[Component]] = field(
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self.components = {
            component_type: []
            for component_type in self.signature
        }

    def _validate_row(self, row: RowIndex) -> None:
        max_row = len(self.entities) - 1

        if not (0 <= row <= max_row):
            raise InvalidRow(row, max_row)

    def append(
        self,
        entity: EntityId,
        components: Mapping[ComponentType, Component],
    ) -> RowIndex:
        signature = set(components)

        if signature != self.signature:
            missing = self.signature - signature
            unexpected = signature - self.signature
            raise InvalidSignature(missing, unexpected)

        row = RowIndex(len(self.entities))
        self.entities.append(entity)

        for component_type, component in components.items():
            self.components[component_type].append(component)

        return row

    def remove(self, row: RowIndex) -> EntityId | None:
        self._validate_row(row)

        moved_entity: EntityId | None = None
        max_row = len(self.entities) - 1

        if row != max_row:
            moved_entity = self.entities[max_row]
            self.entities[row] = moved_entity

            for component_type in self.components:
                components_table = self.components[component_type]
                components_table[row] = components_table[max_row]

        self.entities.pop()

        for component in self.components.values():
            component.pop()

        return moved_entity

    def get_component[ComponentT](
        self,
        row: RowIndex,
        component_type: type[ComponentT],
    ) -> ComponentT:
        self._validate_row(row)
        assert component_type in self.components, (
            f'{component_type.__name__} is not in {self!r}'
        )
        return cast(ComponentT, self.components[component_type][row])

    def set_component(self, row: RowIndex, component: Component) -> None:
        self._validate_row(row)
        component_type = type(component)
        assert component_type in self.components, (
            f'{component_type.__name__} is not in {self!r}'
        )
        self.components[component_type][row] = component

    def get_row(
        self,
        row: RowIndex,
    ) -> dict[ComponentType, Component]:
        self._validate_row(row)
        return {
            component_type: self.components[component_type][row]
            for component_type in self.components
        }

    def get_column(self, component_type: ComponentType) -> list[Component]:
        assert component_type in self.components, (
            f'{component_type.__name__} is not in {self!r}'
        )
        return self.components[component_type]
