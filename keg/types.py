from typing import NewType

type Component = object
type ComponentType = type[Component]
EntityId = NewType('EntityId', int)
