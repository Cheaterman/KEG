from __future__ import annotations

from collections.abc import Iterable

from .types import ComponentType, EntityId


def component_names(
    component_types: Iterable[ComponentType],
) -> tuple[str, ...]:
    return tuple(sorted(
        component_type.__name__
        for component_type in component_types
    ))


class DuplicateComponent(ValueError):
    def __init__(self, duplicate_components: Iterable[ComponentType]):
        super().__init__(
            'Duplicate component types: '
            f'{component_names(duplicate_components)}'
        )


class InvalidComponent(KeyError):
    def __init__(self, component_type: ComponentType, entity: EntityId):
        super().__init__(
            f'{component_type.__name__} is not present on '
            f'{EntityId.__name__}({entity!r})'
        )
        self.component_type = component_type
        self.entity = entity


class InvalidEntity(KeyError):
    def __init__(self, entity: EntityId):
        super().__init__(
            'The requested entity does not exist: '
            f'{EntityId.__name__}({entity!r})'
        )
        self.entity = entity
