from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any, Protocol

from .archetype import Column
from .types import ComponentType, EntityId

type QueryBatch = tuple[
    Sequence[EntityId],
    *tuple[Column[Any], ...]
]

type QueryPlanEntry = tuple[
    Sequence[EntityId],
    dict[ComponentType, Column[Any]],
]


@dataclass(frozen=True, slots=True)
class QueryPlan:
    signature: frozenset[ComponentType]
    entries: list[QueryPlanEntry]


class _QueryGuardian(Protocol):
    def __call__(self) -> AbstractContextManager[None]: ...


@dataclass(frozen=True, slots=True)
class Query:
    component_types: tuple[ComponentType, ...]
    _query_guardian: _QueryGuardian
    _plan: QueryPlan

    def __iter__(self) -> Iterator[QueryBatch]:
        with self._query_guardian():
            for entities, components in self._plan.entries:
                yield (
                    entities,
                    *(
                        components[component_type]
                        for component_type in self.component_types
                    )
                )
