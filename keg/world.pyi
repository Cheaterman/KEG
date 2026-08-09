from collections.abc import Callable, Generator, Sequence
from contextlib import AbstractContextManager
from typing import Any, overload

from .archetype import Column, MutableColumn
from .types import Component, ComponentType, EntityId

class World:
    def __init__(self) -> None:
        ...

    def register_column_type[ComponentT](
        self,
        component_type: type[ComponentT],
        column_type: Callable[[], MutableColumn[ComponentT]],
    ) -> None:
        ...

    def spawn(self, *components: Component) -> EntityId:
        ...

    def despawn(self, entity: EntityId) -> None:
        ...

    def get_component[ComponentT](
        self,
        entity: EntityId,
        component_type: type[ComponentT],
    ) -> ComponentT:
        ...

    def set_component(
        self,
        entity: EntityId,
        component: Component,
    ) -> None:
        ...

    def add_component(
        self,
        entity: EntityId,
        component: Component,
    ) -> None:
        ...

    def remove_component(
        self,
        entity: EntityId,
        component_type: ComponentType,
    ) -> None:
        ...

    @overload
    def query[ComponentT](
        self,
        component_type: type[ComponentT],
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
    ]]:
        ...

    @overload
    def query[ComponentT, ComponentT2](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
    ]]:
        ...

    @overload
    def query[ComponentT, ComponentT2, ComponentT3](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
    ]]:
        ...

    @overload
    def query[ComponentT, ComponentT2, ComponentT3, ComponentT4](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
    ]]:
        ...

    @overload
    def query[ComponentT, ComponentT2, ComponentT3, ComponentT4, ComponentT5](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
        ComponentT13,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        component_type_13: type[ComponentT13],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
        Column[ComponentT13],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
        ComponentT13,
        ComponentT14,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        component_type_13: type[ComponentT13],
        component_type_14: type[ComponentT14],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
        Column[ComponentT13],
        Column[ComponentT14],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
        ComponentT13,
        ComponentT14,
        ComponentT15,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        component_type_13: type[ComponentT13],
        component_type_14: type[ComponentT14],
        component_type_15: type[ComponentT15],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
        Column[ComponentT13],
        Column[ComponentT14],
        Column[ComponentT15],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
        ComponentT13,
        ComponentT14,
        ComponentT15,
        ComponentT16,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        component_type_13: type[ComponentT13],
        component_type_14: type[ComponentT14],
        component_type_15: type[ComponentT15],
        component_type_16: type[ComponentT16],
        /
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
        Column[ComponentT13],
        Column[ComponentT14],
        Column[ComponentT15],
        Column[ComponentT16],
    ]]:
        ...

    @overload
    def query[
        ComponentT,
        ComponentT2,
        ComponentT3,
        ComponentT4,
        ComponentT5,
        ComponentT6,
        ComponentT7,
        ComponentT8,
        ComponentT9,
        ComponentT10,
        ComponentT11,
        ComponentT12,
        ComponentT13,
        ComponentT14,
        ComponentT15,
        ComponentT16,
    ](
        self,
        component_type: type[ComponentT],
        component_type_2: type[ComponentT2],
        component_type_3: type[ComponentT3],
        component_type_4: type[ComponentT4],
        component_type_5: type[ComponentT5],
        component_type_6: type[ComponentT6],
        component_type_7: type[ComponentT7],
        component_type_8: type[ComponentT8],
        component_type_9: type[ComponentT9],
        component_type_10: type[ComponentT10],
        component_type_11: type[ComponentT11],
        component_type_12: type[ComponentT12],
        component_type_13: type[ComponentT13],
        component_type_14: type[ComponentT14],
        component_type_15: type[ComponentT15],
        component_type_16: type[ComponentT16],
        /,
        *component_types: ComponentType,
    ) -> Generator[tuple[
        Sequence[EntityId],
        Column[ComponentT],
        Column[ComponentT2],
        Column[ComponentT3],
        Column[ComponentT4],
        Column[ComponentT5],
        Column[ComponentT6],
        Column[ComponentT7],
        Column[ComponentT8],
        Column[ComponentT9],
        Column[ComponentT10],
        Column[ComponentT11],
        Column[ComponentT12],
        Column[ComponentT13],
        Column[ComponentT14],
        Column[ComponentT15],
        Column[ComponentT16],
        *tuple[Column[Any], ...]
    ]]:
        ...

    def defer_structural_changes(self) -> AbstractContextManager[None]:
        ...

    def flush(self) -> None:
        ...
