from collections import Counter
from collections.abc import Generator, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, assert_never, cast

from .archetype import Archetype, RowIndex
from .errors import DuplicateComponent, InvalidComponent, InvalidEntity
from .query import Query, QueryPlan, QueryPlanEntry
from .types import Component, ComponentType, EntityId


@dataclass(frozen=True, slots=True)
class _EntityLocation:
    archetype: Archetype
    row: RowIndex


@dataclass(frozen=True, slots=True)
class _PendingEntitySpawn:
    components: dict[ComponentType, Component]


@dataclass(frozen=True, slots=True)
class _PendingEntityDespawn:
    existing: bool


@dataclass(frozen=True, slots=True)
class _PendingEntityChange:
    components: dict[ComponentType, Component]


type _PendingEntityState = (
    _PendingEntitySpawn
    | _PendingEntityDespawn
    | _PendingEntityChange
)


@dataclass(eq=False, slots=True)
class World:
    _archetypes: dict[frozenset[ComponentType], Archetype] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _entity_locations: dict[EntityId, _EntityLocation] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _next_entity_id: int = field(
        default=1,
        init=False,
        repr=False,
    )
    _active_queries: set[object] = field(
        default_factory=set,
        init=False,
        repr=False,
    )
    _query_plans: dict[frozenset[ComponentType], QueryPlan] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _pending_entities: dict[EntityId, _PendingEntityState] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _open_deferrals: int = field(
        default=0,
        init=False,
        repr=False,
    )

    def _get_archetype(
        self,
        component_types: frozenset[ComponentType],
    ) -> Archetype:
        archetype = self._archetypes.get(component_types)

        if not archetype:
            archetype = Archetype(component_types)
            self._archetypes[component_types] = archetype
            get_column = archetype.get_column

            for signature, query_plan in self._query_plans.items():
                if signature <= component_types:
                    query_plan.entries.append((
                        archetype.entities,
                        {
                            component_type: get_column(component_type)
                            for component_type in signature
                        },
                    ))

        return archetype

    def _get_location(self, entity: EntityId) -> _EntityLocation:
        location = self._entity_locations.get(entity)

        if not location:
            raise InvalidEntity(entity)

        return location

    def _remove_entity(self, entity: EntityId) -> None:
        location = self._get_location(entity)
        moved_entity = location.archetype.remove(location.row)
        del self._entity_locations[entity]

        if moved_entity is not None:
            self._entity_locations[moved_entity] = _EntityLocation(
                location.archetype,
                location.row,
            )

    def _get_query_plan(
        self,
        signature: frozenset[ComponentType],
    ) -> QueryPlan:
        query_plan = self._query_plans.get(signature)

        if not query_plan:
            entries: list[QueryPlanEntry] = []

            for archetype in self._archetypes.values():
                if signature <= archetype.signature:
                    get_column = archetype.get_column
                    entries.append((
                        archetype.entities,
                        {
                            component_type: get_column(component_type)
                            for component_type in signature
                        },
                    ))

            query_plan = QueryPlan(signature, entries)
            self._query_plans[signature] = query_plan

        return query_plan

    @contextmanager
    def _query_scope(self) -> Iterator[None]:
        token = object()
        self._active_queries.add(token)

        try:
            yield
        finally:
            self._active_queries.remove(token)
            self._try_autoflush()

    def _try_autoflush(self) -> None:
        if self._active_queries or self._open_deferrals:
            return

        self.flush()

    def spawn(self, *components: Component) -> EntityId:
        components_by_type = {
            type(component): component
            for component in components
        }

        if len(components_by_type) != len(components):
            duplicate_components = {
                component_type
                for component_type, count in Counter(
                    type(component)
                    for component in components
                ).items()
                if count > 1
            }
            raise DuplicateComponent(duplicate_components)

        entity = EntityId(self._next_entity_id)
        self._next_entity_id += 1

        self._pending_entities[entity] = _PendingEntitySpawn(
            components_by_type,
        )
        self._try_autoflush()

        return entity

    def despawn(self, entity: EntityId) -> None:
        pending_entity = self._pending_entities.get(entity)

        match pending_entity:
            case None | _PendingEntityChange():
                new_pending_entity = _PendingEntityDespawn(existing=True)

            case _PendingEntitySpawn():
                new_pending_entity = _PendingEntityDespawn(existing=False)

            case _PendingEntityDespawn():
                raise InvalidEntity(entity)

            case _:  # pragma: no cover
                assert_never(pending_entity)

        self._pending_entities[entity] = new_pending_entity
        self._try_autoflush()

    def get_component[ComponentT](
        self,
        entity: EntityId,
        component_type: type[ComponentT],
    ) -> ComponentT:
        pending_entity = self._pending_entities.get(entity)

        match pending_entity:
            case (
                _PendingEntitySpawn(components)
                | _PendingEntityChange(components)
            ):
                if component_type not in components:
                    raise InvalidComponent(component_type, entity)

                return cast(ComponentT, components[component_type])

            case _PendingEntityDespawn():
                raise InvalidEntity(entity)

            case None:
                pass

            case _:  # pragma: no cover
                assert_never(pending_entity)

        location = self._get_location(entity)
        archetype = location.archetype

        if component_type not in archetype.signature:
            raise InvalidComponent(component_type, entity)

        return archetype.get_component(location.row, component_type)

    def set_component(
        self,
        entity: EntityId,
        component: Component,
    ) -> None:
        pending_entity = self._pending_entities.get(entity)
        component_type = type(component)

        match pending_entity:
            case (
                _PendingEntitySpawn(components)
                | _PendingEntityChange(components)
            ):
                if component_type not in components:
                    raise InvalidComponent(component_type, entity)

                components[component_type] = component
                return

            case _PendingEntityDespawn():
                raise InvalidEntity(entity)

            case None:
                pass

            case _:  # pragma: no cover
                assert_never(pending_entity)

        location = self._get_location(entity)
        archetype = location.archetype

        if component_type not in archetype.signature:
            raise InvalidComponent(component_type, entity)

        archetype.set_component(location.row, component)

    def add_component(
        self,
        entity: EntityId,
        component: Component,
    ) -> None:
        pending_entity = self._pending_entities.get(entity)
        component_type = type(component)

        match pending_entity:
            case None:
                location = self._get_location(entity)
                archetype = location.archetype

                if component_type in archetype.signature:
                    raise DuplicateComponent([component_type])

                components = archetype.get_row(location.row)
                components[component_type] = component
                self._pending_entities[entity] = _PendingEntityChange(
                    components,
                )

            case (
                _PendingEntitySpawn(components)
                | _PendingEntityChange(components)
            ):
                if component_type in components:
                    raise DuplicateComponent([component_type])

                components[component_type] = component

            case _PendingEntityDespawn():
                raise InvalidEntity(entity)

            case _:  # pragma: no cover
                assert_never(pending_entity)

        self._try_autoflush()

    def remove_component(
        self,
        entity: EntityId,
        component_type: ComponentType,
    ) -> None:
        pending_entity = self._pending_entities.get(entity)

        match pending_entity:
            case None:
                location = self._get_location(entity)
                archetype = location.archetype

                if component_type not in archetype.signature:
                    raise InvalidComponent(component_type, entity)

                components = location.archetype.get_row(location.row)
                components.pop(component_type)
                self._pending_entities[entity] = _PendingEntityChange(
                    components,
                )

            case (
                _PendingEntitySpawn(components)
                | _PendingEntityChange(components)
            ):
                if component_type not in components:
                    raise InvalidComponent(component_type, entity)

                components.pop(component_type)

            case _PendingEntityDespawn():
                raise InvalidEntity(entity)

            case _:  # pragma: no cover
                assert_never(pending_entity)

        self._try_autoflush()

    def query(
        self,
        component_type: ComponentType,
        *component_types: ComponentType,
    ) -> Generator[
        tuple[Sequence[Any], ...],
        None,
        None,
    ]:
        component_types = (component_type, *component_types)
        signature = frozenset(component_types)

        if len(component_types) != len(signature):
            duplicate_components = {
                component_type
                for component_type, count in Counter(component_types).items()
                if count > 1
            }
            raise DuplicateComponent(duplicate_components)

        query_plan = self._get_query_plan(signature)
        query = Query(component_types, self, query_plan)
        yield from query

    @contextmanager
    def defer_structural_changes(self) -> Iterator[None]:
        self._open_deferrals += 1

        try:
            yield
        finally:
            self._open_deferrals -= 1
            self._try_autoflush()

    def flush(self) -> None:
        if self._active_queries:
            raise RuntimeError('Cannot flush during an active query')

        for entity, pending_state in self._pending_entities.items():
            match pending_state:
                case _PendingEntitySpawn(components):
                    archetype = self._get_archetype(frozenset(components))
                    row = archetype.append(entity, components)
                    self._entity_locations[entity] = _EntityLocation(
                        archetype,
                        row,
                    )

                case _PendingEntityDespawn(existing):
                    if existing:
                        self._remove_entity(entity)

                case _PendingEntityChange(components):
                    signature = frozenset(components)
                    location = self._get_location(entity)
                    archetype = location.archetype

                    if signature == archetype.signature:
                        row = location.row
                        columns = archetype.components

                        for component_type, component in components.items():
                            columns[component_type][row] = component

                        continue

                    self._remove_entity(entity)
                    target = self._get_archetype(signature)
                    row = target.append(entity, components)
                    self._entity_locations[entity] = _EntityLocation(
                        target,
                        row,
                    )

                case _:  # pragma: no cover
                    assert_never(pending_state)

        self._pending_entities.clear()
