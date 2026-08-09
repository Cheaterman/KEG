from __future__ import annotations

from collections.abc import Iterator, Mapping
from collections.abc import Set as AbstractSet
from dataclasses import dataclass, field
from typing import Any, NewType, Protocol, cast

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


class Column[ColumnT](Protocol):
    def __getitem__(self, index: int, /) -> ColumnT:
        ...

    def __iter__(self) -> Iterator[ColumnT]:
        ...

    def __len__(self) -> int:
        ...


class MutableColumn[ColumnT](Column[ColumnT], Protocol):
    def __setitem__(self, index: int, value: ColumnT, /) -> None:
        ...

    def append(self, value: ColumnT, /) -> None:
        ...

    def pop(self) -> ColumnT:
        ...


@dataclass(eq=False, frozen=True, slots=True)
class Archetype:
    signature: frozenset[ComponentType]
    columns: dict[ComponentType, MutableColumn[Any]] = field(repr=False)
    entities: list[EntityId] = field(
        default_factory=list[EntityId],
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        column_types = self.columns.keys()

        assert self.signature == column_types, (
            'Column types do not match archetype signature: '
            f'missing={component_names(self.signature - column_types)}, '
            f'unexpected={component_names(column_types - self.signature)}'
        )

        for component_type, column in self.columns.items():
            assert not column, (
                f'Column for {component_type.__name__} is not empty at '
                f'archetype construction: size={len(column)}'
            )

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

        if signature != self.signature:  # pyright: ignore[reportUnnecessaryComparison]
            missing = self.signature - signature
            unexpected = signature - self.signature
            raise InvalidSignature(missing, unexpected)

        row = RowIndex(len(self.entities))
        self.entities.append(entity)

        for component_type, component in components.items():
            self.columns[component_type].append(component)

        return row

    def remove(self, row: RowIndex) -> EntityId | None:
        self._validate_row(row)

        moved_entity: EntityId | None = None
        max_row = len(self.entities) - 1

        if row != max_row:
            moved_entity = self.entities[max_row]
            self.entities[row] = moved_entity

            for component_type in self.columns:
                column = self.columns[component_type]
                column[row] = column[max_row]

        self.entities.pop()

        for column in self.columns.values():
            column.pop()

        return moved_entity

    def get_component[ComponentT](
        self,
        row: RowIndex,
        component_type: type[ComponentT],
    ) -> ComponentT:
        self._validate_row(row)
        assert component_type in self.columns, (
            f'{component_type.__name__} is not in {self!r}'
        )
        return cast(ComponentT, self.columns[component_type][row])

    def set_component(self, row: RowIndex, component: Component) -> None:
        self._validate_row(row)
        component_type = type(component)
        assert component_type in self.columns, (
            f'{component_type.__name__} is not in {self!r}'
        )
        self.columns[component_type][row] = component

    def get_row(
        self,
        row: RowIndex,
    ) -> dict[ComponentType, Component]:
        self._validate_row(row)
        return {
            component_type: self.columns[component_type][row]
            for component_type in self.columns
        }

    def get_column[ComponentT](
        self,
        component_type: type[ComponentT],
    ) -> Column[ComponentT]:
        assert component_type in self.columns, (
            f'{component_type.__name__} is not in {self!r}'
        )
        return self.columns[component_type]
