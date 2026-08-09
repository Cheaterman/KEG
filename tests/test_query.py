import pytest

from keg.errors import DuplicateComponent, InvalidEntity
from keg.world import World
from tests.components import Health, Position, Velocity


def test_query_returns_matching_archetypes_as_aligned_columns(
    world: World,
) -> None:
    position_only = world.spawn(Position(10))
    positioned_velocity = world.spawn(Position(20), Velocity(30))
    world.spawn(Velocity(40))

    batches = list(world.query(Position))

    assert len(batches) == 2
    assert {
        entity: position
        for entities, positions in batches
        for entity, position in zip(entities, positions, strict=True)
    } == {
        position_only: Position(10),
        positioned_velocity: Position(20),
    }

    [(entities, velocities, positions)] = world.query(Velocity, Position)
    assert entities == [positioned_velocity]
    assert velocities == [Velocity(30)]
    assert positions == [Position(20)]


def test_cached_query_plan_tracks_new_matching_archetypes(
    world: World,
) -> None:
    first = world.spawn(Position(10))

    assert list(world.query(Position)) == [([first], [Position(10)])]
    assert list(world.query(Health)) == []

    second = world.spawn(Position(20), Velocity(30))
    world.spawn(Velocity(40))

    assert {
        entity: position
        for entities, positions in world.query(Position)
        for entity, position in zip(entities, positions, strict=True)
    } == {
        first: Position(10),
        second: Position(20),
    }
    assert list(world.query(Health)) == []


def test_query_rejects_duplicate_component_types(world: World) -> None:
    with pytest.raises(DuplicateComponent) as caught:
        list(world.query(Position, Velocity, Position, Velocity))

    assert caught.value.args == (
        "Duplicate component types: ('Position', 'Velocity')",
    )


def test_closing_query_releases_it_and_flushes_pending_changes(
    world: World,
) -> None:
    first = world.spawn(Position(10))
    query = world.query(Position)

    assert next(query) == ([first], [Position(10)])

    second = world.spawn(Position(20))
    assert all(
        second not in entities
        for entities, _positions in world.query(Position)
    )

    query.close()

    assert any(
        second in entities
        for entities, _positions in world.query(Position)
    )


def test_pending_changes_wait_for_every_active_query(world: World) -> None:
    first = world.spawn(Position(10))
    first_query = world.query(Position)
    second_query = world.query(Position)

    next(first_query)
    next(second_query)
    pending = world.spawn(Position(20))

    first_query.close()
    assert all(
        pending not in entities
        for entities, _positions in world.query(Position)
    )

    second_query.close()
    assert any(
        pending in entities
        for entities, _positions in world.query(Position)
    )
    assert world.get_component(first, Position) == Position(10)


def test_flush_is_rejected_during_an_active_query(world: World) -> None:
    world.spawn(Position(10))
    query = world.query(Position)
    next(query)

    with pytest.raises(
        RuntimeError,
        match='Cannot flush during an active query',
    ):
        world.flush()

    query.close()


def test_empty_query_still_releases_its_token(world: World) -> None:
    assert list(world.query(Position)) == []

    entity = world.spawn(Position(10))
    assert list(world.query(Position)) == [([entity], [Position(10)])]


def test_despawn_during_query_is_applied_when_query_closes(
    world: World,
) -> None:
    entity = world.spawn(Position(10))
    query = world.query(Position)
    next(query)

    world.despawn(entity)

    with pytest.raises(InvalidEntity):
        world.get_component(entity, Position)

    query.close()

    assert all(
        not entities
        for entities, _positions in world.query(Position)
    )
