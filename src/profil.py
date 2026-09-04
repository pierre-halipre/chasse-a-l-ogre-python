"""Copyright 2026 Pierre Halipré

This file is part of Chasse à l'ogre.

Chasse à l'ogre is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Chasse à l'ogre is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Chasse à l'ogre. If not, see <https://www.gnu.org/licenses/>.
"""

from abc import abstractmethod
from tool import Math
from device import Device
from board import Board
from sprite import Sprite
from state import State
from timer import Timer


class Profil(State):
    COME = 1
    WAIT = 2
    LEAVE = 3
    OUT = 4
    FALL = 5
    SPEED_FALL = 7 / 7

    def __init__(self, rank: int, board: Board, device: Device) -> None:
        super().__init__()

        if rank == 0:
            self.speed_walk = 13 / 7
            self.speed_wait = 17 / 7
            rasters_zone = device.graphic.game.characters.zombie
        elif rank == 1:
            self.speed_walk = 12 / 7
            self.speed_wait = 18 / 7
            rasters_zone = device.graphic.game.characters.vampire
        elif rank == 2:
            self.speed_walk = 9 / 7
            self.speed_wait = 15 / 7
            rasters_zone = device.graphic.game.characters.deer
        elif rank == 3:
            self.speed_walk = 11 / 7
            self.speed_wait = 19 / 7
            rasters_zone = device.graphic.game.characters.skeleton
        elif rank == 4:
            self.speed_walk = 10 / 7
            self.speed_wait = 20 / 7
            rasters_zone = device.graphic.game.characters.ghost
        elif rank == 5:
            self.speed_walk = 8 / 7
            self.speed_wait = 16 / 7
            rasters_zone = device.graphic.game.characters.rabbit
        else:
            self.speed_walk = 21 / 7
            self.speed_wait = 14 / 7
            rasters_zone = device.graphic.game.characters.logger

        self.sprite = Sprite(rasters_zone)
        board.fill_sprite(self.sprite, 3, device)

        self.timer = Timer()
        self.time_base = 0

    def set_none(self) -> None:
        super().set_none()

        self.timer.stop()

    def set_come(self, device: Device) -> None:
        self.set_state(Profil.COME)
        time = self.get_time()
        self.timer.start(time, device)

    def is_come(self) -> bool:
        return self.is_state(Profil.COME)

    def set_wait(self, device: Device) -> None:
        self.set_state(Profil.WAIT)
        time = self.get_time()
        self.timer.start(time, device)

    def is_wait(self) -> bool:
        return self.is_state(Profil.WAIT)

    def set_leave(self, device: Device) -> None:
        self.set_state(Profil.LEAVE)
        time = self.get_time()
        self.timer.start(time, device)

    def is_leave(self) -> bool:
        return self.is_state(Profil.LEAVE)

    def set_out(self) -> None:
        self.set_state(Profil.OUT)

    def is_out(self) -> bool:
        return self.is_state(Profil.OUT)

    def set_fall(self, device: Device) -> None:
        self.set_state(Profil.FALL)
        time = self.get_time()
        self.timer.start(time, device)

    def is_fall(self) -> bool:
        return self.is_state(Profil.FALL)

    def is_end(self) -> bool:
        return self.is_none() or self.is_out()

    def get_time(self) -> int:
        speed = self.get_speed()
        time = Math.ceil(speed * self.time_base)
        n_animations = Math.round(speed)
        time_animation = Math.ceil(time / n_animations)

        return n_animations * time_animation

    def get_speed(self) -> float:
        result = None

        if self.is_come() or self.is_leave():
            result = self.speed_walk
        elif self.is_wait():
            result = self.speed_wait
        else:
            result = Profil.SPEED_FALL

        return result

    @abstractmethod
    def update(self, device: Device) -> None:
        pass

    def get_ratio_position(self) -> float:
        result = None

        if self.is_come():
            result = self.timer.get_ratio()
        elif self.is_leave():
            result = self.timer.get_ratio_inverse()
        else:
            result = 1

        return result

    def get_ratio_sprite(self) -> float:
        result = None

        if self.is_fall():
            half_threshold = Math.round(self.timer.threshold / 2)

            if self.timer.counts < half_threshold:
                result = self.timer.get_ratio()
            else:
                result = half_threshold / self.timer.threshold
        else:
            n_animations = Math.round(self.get_speed())
            threshold = Math.ceil(self.timer.threshold / n_animations)
            result = (self.timer.counts % threshold) / threshold

        return result
