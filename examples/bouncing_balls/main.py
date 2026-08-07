from dataclasses import dataclass
from math import cos, sin, tau
from random import uniform

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget

from keg import EntityId, World

BALL_COUNT = 256
BALL_RADIUS_PX = 16.0
MIN_SPEED = 0.15
MAX_SPEED = 0.35
TARGET_FPS = 60.0


@dataclass(slots=True)
class Position:
    x: float
    y: float


@dataclass(slots=True)
class Velocity:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Collider:
    radius: float


class Board(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.world = World()
        self.ellipses: dict[EntityId, Ellipse] = {}
        Clock.schedule_once(self._start, 0)

    def _start(self, _dt: float) -> None:
        radius = BALL_RADIUS_PX / self.height
        board_width = self.width / self.height

        for _index in range(BALL_COUNT):
            angle = uniform(0.0, tau)
            speed = uniform(MIN_SPEED, MAX_SPEED)
            entity = self.world.spawn(
                Position(
                    uniform(radius, board_width - radius),
                    uniform(radius, 1.0 - radius),
                ),
                Velocity(speed * cos(angle), speed * sin(angle)),
                Collider(radius),
            )

            with self.canvas:
                Color(
                    uniform(0.35, 1.0),
                    uniform(0.35, 1.0),
                    uniform(0.35, 1.0),
                    1.0,
                )
                self.ellipses[entity] = Ellipse()

        self._update(0.0)
        Clock.schedule_interval(self._update, 1.0 / TARGET_FPS)

    def _update(self, dt: float) -> None:  # noqa: C901
        if self.height == 0:
            return

        board_width = self.width / self.height

        for entities, positions, velocities, colliders in self.world.query(
            Position,
            Velocity,
            Collider,
        ):
            for index in range(len(entities)):
                position = positions[index]
                velocity = velocities[index]
                radius = colliders[index].radius

                position.x += velocity.x * dt
                position.y += velocity.y * dt

                if position.x - radius < 0.0:
                    position.x = radius

                    if velocity.x < 0.0:
                        velocity.x = -velocity.x

                elif position.x + radius > board_width:
                    position.x = board_width - radius

                    if velocity.x > 0.0:
                        velocity.x = -velocity.x

                if position.y - radius < 0.0:
                    position.y = radius

                    if velocity.y < 0.0:
                        velocity.y = -velocity.y

                elif position.y + radius > 1.0:
                    position.y = 1.0 - radius

                    if velocity.y > 0.0:
                        velocity.y = -velocity.y

                diameter = radius * self.height * 2.0
                ellipse = self.ellipses[entities[index]]
                ellipse.pos = (
                    self.x + (position.x - radius) * self.height,
                    self.y + (position.y - radius) * self.height,
                )
                ellipse.size = (diameter, diameter)


class BouncingBallsApp(App):
    def build(self) -> Board:
        Window.size = (960, 600)
        return Board()


if __name__ == '__main__':
    BouncingBallsApp().run()
