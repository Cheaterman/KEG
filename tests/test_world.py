import pytest

from keg.errors import DuplicateComponent, InvalidComponent, InvalidEntity
from keg.types import EntityId
from keg.world import World
from tests.components import Health, Position, Velocity


def test_spawn_assigns_monotonic_entity_ids() -> None:
    world = World()

    empty_entity = world.spawn()
    positioned_entity = world.spawn(Position(10))

    assert empty_entity == EntityId(1)
    assert positioned_entity == EntityId(2)
    assert world.get_component(positioned_entity, Position) == Position(10)

    with pytest.raises(InvalidComponent):
        world.get_component(empty_entity, Position)


def test_duplicate_spawn_is_rejected_without_allocating_an_id() -> None:
    world = World()

    with pytest.raises(DuplicateComponent) as caught:
        world.spawn(Position(10), Position(20))

    assert caught.value.args == ("Duplicate component types: ('Position',)",)
    assert world.spawn(Position(30)) == EntityId(1)


def test_despawn_repairs_the_swap_moved_entity_location() -> None:
    world = World()
    first = world.spawn(Position(10))
    second = world.spawn(Position(20))

    world.despawn(first)

    assert world.get_component(second, Position) == Position(20)

    with pytest.raises(InvalidEntity) as caught:
        world.get_component(first, Position)

    assert caught.value.entity == first
    assert caught.value.args == (
        'The requested entity does not exist: EntityId(1)',
    )

    world.despawn(second)

    with pytest.raises(InvalidEntity):
        world.despawn(second)


def test_get_and_set_component() -> None:
    world = World()
    entity = world.spawn(Position(10))

    assert world.get_component(entity, Position) == Position(10)

    world.set_component(entity, Position(20))
    assert world.get_component(entity, Position) == Position(20)

    with pytest.raises(InvalidComponent) as caught:
        world.get_component(entity, Health)

    assert caught.value.component_type is Health
    assert caught.value.entity == entity
    assert caught.value.args == (
        'Health is not present on EntityId(1)',
    )

    with pytest.raises(InvalidComponent):
        world.set_component(entity, Health(30))


def test_add_and_remove_component_migrate_between_populated_archetypes(
) -> None:
    world = World()
    position_only = world.spawn(Position(10))
    other_position = world.spawn(Position(20))
    positioned_velocity = world.spawn(Position(30), Velocity(40))

    world.add_component(position_only, Velocity(50))

    assert world.get_component(position_only, Position) == Position(10)
    assert world.get_component(position_only, Velocity) == Velocity(50)
    assert world.get_component(other_position, Position) == Position(20)
    assert world.get_component(positioned_velocity, Velocity) == Velocity(40)

    world.remove_component(position_only, Velocity)

    assert world.get_component(position_only, Position) == Position(10)

    with pytest.raises(InvalidComponent):
        world.get_component(position_only, Velocity)


def test_add_and_remove_component_validate_before_mutating() -> None:
    world = World()
    entity = world.spawn(Position(10))

    with pytest.raises(DuplicateComponent):
        world.add_component(entity, Position(20))

    assert world.get_component(entity, Position) == Position(10)

    with pytest.raises(InvalidComponent):
        world.remove_component(entity, Velocity)

    assert world.get_component(entity, Position) == Position(10)


def test_remove_last_component_and_add_it_back() -> None:
    world = World()
    entity = world.spawn(Position(10))

    world.remove_component(entity, Position)

    with pytest.raises(InvalidComponent):
        world.get_component(entity, Position)

    world.add_component(entity, Position(20))
    assert world.get_component(entity, Position) == Position(20)
