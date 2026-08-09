import pytest

from keg.errors import DuplicateComponent, InvalidComponent, InvalidEntity
from keg.world import World
from tests.components import Health, Name, Position, Velocity


def test_pending_spawn_supports_component_changes(world: World) -> None:
    with world.defer_structural_changes():
        entity = world.spawn(Position(10))
        assert world.get_component(entity, Position) == Position(10)

        world.set_component(entity, Position(20))
        world.add_component(entity, Velocity(30))
        world.remove_component(entity, Velocity)

        with pytest.raises(DuplicateComponent):
            world.add_component(entity, Position(40))

        with pytest.raises(InvalidComponent):
            world.remove_component(entity, Health)

        with pytest.raises(InvalidComponent):
            world.get_component(entity, Health)

        with pytest.raises(InvalidComponent):
            world.set_component(entity, Health(50))

        assert list(world.query(Position)) == []

    assert world.get_component(entity, Position) == Position(20)
    assert list(world.query(Position)) == [([entity], [Position(20)])]


def test_spawn_then_despawn_cancels_the_entity(world: World) -> None:
    with world.defer_structural_changes():
        entity = world.spawn(Position(10))
        world.despawn(entity)

        with pytest.raises(InvalidEntity):
            world.despawn(entity)

    with pytest.raises(InvalidEntity):
        world.get_component(entity, Position)

    assert list(world.query(Position)) == []


def test_pending_change_can_return_to_the_original_signature(
    world: World,
) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.add_component(entity, Velocity(20))
        world.set_component(entity, Position(30))
        world.remove_component(entity, Velocity)

    assert world.get_component(entity, Position) == Position(30)
    assert list(world.query(Velocity)) == []


def test_remove_then_add_resynchronizes_the_existing_column(
    world: World,
) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.remove_component(entity, Position)
        world.add_component(entity, Position(20))

    assert world.get_component(entity, Position) == Position(20)


def test_pending_change_migrates_when_signature_remains_changed(
    world: World,
) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.add_component(entity, Velocity(20))

    assert world.get_component(entity, Position) == Position(10)
    assert world.get_component(entity, Velocity) == Velocity(20)


def test_pending_change_validates_before_mutating(world: World) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.add_component(entity, Velocity(20))

        with pytest.raises(DuplicateComponent):
            world.add_component(entity, Velocity(30))

        with pytest.raises(InvalidComponent):
            world.remove_component(entity, Health)

        assert world.get_component(entity, Position) == Position(10)
        assert world.get_component(entity, Velocity) == Velocity(20)


def test_pending_despawn_rejects_further_operations(world: World) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.despawn(entity)

        with pytest.raises(InvalidEntity):
            world.get_component(entity, Position)

        with pytest.raises(InvalidEntity):
            world.set_component(entity, Position(20))

        with pytest.raises(InvalidEntity):
            world.add_component(entity, Velocity(30))

        with pytest.raises(InvalidEntity):
            world.remove_component(entity, Position)

        with pytest.raises(InvalidEntity):
            world.despawn(entity)


def test_despawn_discards_an_existing_pending_change(world: World) -> None:
    entity = world.spawn(Position(10))

    with world.defer_structural_changes():
        world.add_component(entity, Velocity(20))
        world.despawn(entity)

    with pytest.raises(InvalidEntity):
        world.get_component(entity, Position)


def test_manual_flush_is_allowed_inside_a_deferral(world: World) -> None:
    with world.defer_structural_changes():
        entity = world.spawn(Position(10))
        world.flush()

        assert list(world.query(Position)) == [
            ([entity], [Position(10)]),
        ]


def test_nested_deferrals_flush_only_after_the_outer_context(
    world: World,
) -> None:
    with world.defer_structural_changes():
        with world.defer_structural_changes():
            entity = world.spawn(Position(10))

        assert list(world.query(Position)) == []

    assert list(world.query(Position)) == [([entity], [Position(10)])]


def test_deferral_flushes_when_the_context_body_raises(world: World) -> None:
    entity = None

    with (
        pytest.raises(RuntimeError, match='system failed'),
        world.defer_structural_changes(),
    ):
        entity = world.spawn(Name('bomb'))
        raise RuntimeError('system failed')

    assert entity
    assert world.get_component(entity, Name) == Name('bomb')
