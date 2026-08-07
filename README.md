# KEG

**KEG is an Engine for Games.** More specifically, it is a small, typed,
archetype-based ECS for Python 3.12 and newer.

KEG does not require components to inherit from anything. A dataclass will do.
So will any other arbitrary object, although please exercise some judgment.

```python
from dataclasses import dataclass

from keg import World


@dataclass(slots=True)
class Position:
    x: float
    y: float


@dataclass(slots=True)
class Velocity:
    x: float
    y: float


world = World()
player = world.spawn(
    Position(10.0, 20.0),
    Velocity(4.0, -2.0),
)

for entities, positions, velocities in world.query(Position, Velocity):
    for row in range(len(entities)):
        position = positions[row]
        velocity = velocities[row]
        position.x += velocity.x
        position.y += velocity.y
```

## Queries return columns

A query yields one batch per matching archetype. Each batch contains the entity
IDs followed by the requested component columns, in request order:

```python
for entities, positions, velocities in world.query(Position, Velocity):
    ...
```

The sequences in a batch are aligned: `entities[row]`, `positions[row]`, and
`velocities[row]` all belong to the same entity. They expose KEG's underlying
column storage and should be treated as read-only. The component objects remain
yours to mutate.

This avoids manufacturing a tuple for every entity merely to take it apart
again in a hot loop. Queries are precisely typed for up to sixteen component
types.

An entity may contain at most one component of each exact runtime type.
Component inheritance has no special meaning to KEG.

## Structural changes

Spawning and despawning entities, or adding and removing components, can move
entities between archetypes. KEG applies those operations immediately during
ordinary use and defers them automatically while a query is being iterated.
The pending changes are committed after the last active query finishes.

You can request the same behaviour explicitly when applying a batch of changes:

```python
with world.defer_structural_changes():
    projectile = world.spawn(Position(0.0, 0.0))
    world.add_component(projectile, Velocity(12.0, 3.0))
```

Pending entities and components remain accessible through `get_component()`
and `set_component()`, while queries continue to see the committed archetype
layout until the changes are flushed.

Queries release their structural guard when exhausted or explicitly closed. If
you retain a query iterator and stop consuming it early, whether through
`break` or an exception in surrounding code, call its `close()` method so
pending structural work can be committed. Do not rely on garbage collection.

## Installation

KEG currently has no runtime dependencies:

```console
python -m pip install .
```

## Example

The bouncing-balls example uses Kivy to exercise a small position and velocity
system in a real update loop:

```console
python -m pip install -e '.[examples]'
python examples/bouncing_balls/main.py
```

## License

KEG is distributed under the MIT license.
