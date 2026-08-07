from collections.abc import Generator, Iterator, Sequence
from contextlib import contextmanager
from typing import Any, overload

from .types import Component, ComponentType, EntityId

class World:
    def __init__(self) -> None:
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
        Sequence[ComponentT],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
        Sequence[ComponentT13],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
        Sequence[ComponentT13],
        Sequence[ComponentT14],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
        Sequence[ComponentT13],
        Sequence[ComponentT14],
        Sequence[ComponentT15],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
        Sequence[ComponentT13],
        Sequence[ComponentT14],
        Sequence[ComponentT15],
        Sequence[ComponentT16],
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
        Sequence[ComponentT],
        Sequence[ComponentT2],
        Sequence[ComponentT3],
        Sequence[ComponentT4],
        Sequence[ComponentT5],
        Sequence[ComponentT6],
        Sequence[ComponentT7],
        Sequence[ComponentT8],
        Sequence[ComponentT9],
        Sequence[ComponentT10],
        Sequence[ComponentT11],
        Sequence[ComponentT12],
        Sequence[ComponentT13],
        Sequence[ComponentT14],
        Sequence[ComponentT15],
        Sequence[ComponentT16],
        *tuple[Sequence[Any], ...]
    ]]:
        ...

    @contextmanager
    def defer_structural_changes(self) -> Iterator[None]:
        ...

    def flush(self) -> None:
        ...
