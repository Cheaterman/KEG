from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any, Protocol

from .types import Component, ComponentType, EntityId

type QueryPlanEntry = tuple[
    Sequence[EntityId],
    dict[ComponentType, Sequence[Component]],
]


@dataclass(frozen=True, slots=True)
class QueryPlan:
    signature: frozenset[ComponentType]
    entries: list[QueryPlanEntry]


class _QueryGuardian(Protocol):
    def _query_scope(self) -> AbstractContextManager[None]: ...


@dataclass(frozen=True, slots=True)
class Query:
    component_types: tuple[ComponentType, ...]
    _world: _QueryGuardian
    _plan: QueryPlan

    def __iter__(self) -> Iterator[tuple[Sequence[Any], ...]]:
        with self._world._query_scope():
            for entities, components in self._plan.entries:
                yield (
                    entities,
                    *(
                        components[component_type]
                        for component_type in self.component_types
                    )
                )
