from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    value: int


@dataclass(frozen=True, slots=True)
class Velocity:
    value: int


@dataclass(frozen=True, slots=True)
class Health:
    value: int


@dataclass(frozen=True, slots=True)
class Name:
    value: str
