import pytest

from keg.types import Component, ComponentType
from keg.world import World
from tests.components import Position, Velocity


@pytest.fixture
def world() -> World:
    return World()


@pytest.fixture
def component_types() -> frozenset[ComponentType]:
    return frozenset((Position, Velocity))


@pytest.fixture
def components() -> dict[ComponentType, Component]:
    return {
        Position: Position(10),
        Velocity: Velocity(20),
    }
