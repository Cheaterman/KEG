import pytest

from keg.errors import DuplicateComponent, InvalidComponent, InvalidEntity
from keg.types import EntityId
from keg.world import World
from tests.components import Health, Position, Velocity


def test_spawn_assigns_monotonic_entity_ids(world: World) -> None:
    empty_entity = world.spawn()
    positioned_entity = world.spawn(Position(10))

    assert empty_entity == EntityId(1)
    assert positioned_entity == EntityId(2)
    assert world.get_component(positioned_entity, Position) == Position(10)

    with pytest.raises(InvalidComponent):
        world.get_component(empty_entity, Position)


def test_duplicate_spawn_is_rejected_without_allocating_an_id(
    world: World,
) -> None:
    with pytest.raises(DuplicateComponent) as caught:
        world.spawn(Position(10), Position(20))

    assert caught.value.args == ("Duplicate component types: ('Position',)",)
    assert world.spawn(Position(30)) == EntityId(1)


def test_register_column_type_is_used_for_new_archetypes(
    world: World,
) -> None:
    class PositionColumn(list[Position]):
        pass

    world.register_column_type(Position, PositionColumn)
    position_only = world.spawn(Position(10))
    positioned_velocity = world.spawn(Position(20), Velocity(30))

    [
        (position_only_entities, position_only_positions),
        (positioned_velocity_entities, positioned_velocity_positions),
    ] = world.query(Position)
    assert position_only_entities == [position_only]
    assert isinstance(position_only_positions, PositionColumn)
    assert position_only_positions == [Position(10)]
    assert positioned_velocity_entities == [positioned_velocity]
    assert isinstance(positioned_velocity_positions, PositionColumn)
    assert positioned_velocity_positions == [Position(20)]

    with pytest.raises(ValueError):
        world.register_column_type(Position, PositionColumn)


def test_despawn_repairs_the_swap_moved_entity_location(
    world: World,
) -> None:
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


def test_invalid_despawn_does_not_leave_pending_state(world: World) -> None:
    invalid_entity = EntityId(999)

    with pytest.raises(InvalidEntity):
        world.despawn(invalid_entity)

    assert world.spawn() == EntityId(1)


def test_get_and_set_component(world: World) -> None:
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
    world: World,
) -> None:
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


def test_add_and_remove_component_validate_before_mutating(
    world: World,
) -> None:
    entity = world.spawn(Position(10))

    with pytest.raises(DuplicateComponent):
        world.add_component(entity, Position(20))

    assert world.get_component(entity, Position) == Position(10)

    with pytest.raises(InvalidComponent):
        world.remove_component(entity, Velocity)

    assert world.get_component(entity, Position) == Position(10)


def test_remove_last_component_and_add_it_back(world: World) -> None:
    entity = world.spawn(Position(10))

    world.remove_component(entity, Position)

    with pytest.raises(InvalidComponent):
        world.get_component(entity, Position)

    world.add_component(entity, Position(20))
    assert world.get_component(entity, Position) == Position(20)
