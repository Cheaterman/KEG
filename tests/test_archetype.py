import pytest

from keg.archetype import (
    Archetype,
    InvalidRow,
    InvalidSignature,
    RowIndex,
)
from keg.types import Component, ComponentType, EntityId
from tests.components import Health, Position, Velocity


@pytest.fixture
def archetype(component_types: frozenset[ComponentType]) -> Archetype:
    return Archetype(
        component_types,
        {Position: [], Velocity: []},
    )


def test_append_and_access_components(
    archetype: Archetype,
    components: dict[ComponentType, Component],
) -> None:
    row = archetype.append(
        EntityId(1),
        components,
    )

    assert row == RowIndex(0)
    assert archetype.entities == [EntityId(1)]
    assert archetype.get_component(row, Position) is components[Position]
    assert archetype.get_row(row) == components
    assert archetype.get_column(Position) is archetype.columns[Position]

    replacement = Position(30)
    archetype.set_component(row, replacement)
    assert archetype.get_component(row, Position) is replacement


def test_append_rejects_components_that_do_not_match_signature() -> None:
    archetype = Archetype(
        frozenset((Position, Health)),
        {Position: [], Health: []},
    )

    with pytest.raises(InvalidSignature) as caught:
        archetype.append(
            EntityId(1),
            {Position: Position(10), Velocity: Velocity(20)},
        )

    assert caught.value.missing == {Health}
    assert caught.value.unexpected == {Velocity}
    assert caught.value.args == (
        (
            'Components do not match signature: '
            "missing=('Health',), unexpected=('Velocity',)"
        ),
    )
    assert archetype.entities == []
    assert archetype.columns == {Position: [], Health: []}


def test_remove_swap_moves_the_last_row(archetype: Archetype) -> None:
    first = EntityId(1)
    second = EntityId(2)
    third = EntityId(3)

    archetype.append(first, {Position: Position(1), Velocity: Velocity(10)})
    archetype.append(second, {Position: Position(2), Velocity: Velocity(20)})
    archetype.append(third, {Position: Position(3), Velocity: Velocity(30)})

    moved_entity = archetype.remove(RowIndex(1))

    assert moved_entity == third
    assert archetype.entities == [first, third]
    assert archetype.columns[Position] == [Position(1), Position(3)]
    assert archetype.columns[Velocity] == [Velocity(10), Velocity(30)]

    assert archetype.remove(RowIndex(1)) is None
    assert archetype.entities == [first]
    assert archetype.columns[Position] == [Position(1)]
    assert archetype.columns[Velocity] == [Velocity(10)]


@pytest.mark.parametrize('row', (RowIndex(-1), RowIndex(1)))
def test_invalid_row_is_rejected(
    row: RowIndex,
    archetype: Archetype,
    components: dict[ComponentType, Component],
) -> None:
    archetype.append(EntityId(1), components)

    with pytest.raises(InvalidRow) as caught:
        archetype.remove(row)

    assert caught.value.row == row
    assert caught.value.max_row == 0
    assert caught.value.args == (f'Row {row} is outside the valid range 0..0',)


def test_component_access_checks_internal_invariants(
    archetype: Archetype,
    components: dict[ComponentType, Component],
) -> None:
    row = archetype.append(EntityId(1), components)

    with pytest.raises(AssertionError, match='Health is not in Archetype'):
        archetype.get_component(row, Health)

    with pytest.raises(AssertionError, match='Health is not in Archetype'):
        archetype.set_component(row, Health(20))

    with pytest.raises(AssertionError, match='Health is not in Archetype'):
        archetype.get_column(Health)
