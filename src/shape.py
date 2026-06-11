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

from tool import Math
from device import Device


class Shape:
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 4
    RIGHT = 8
    UP = 16
    DOWN = 32
    FULL = 64

    def __init__(self, i: int, j: int, track: int, lines: int) -> None:
        self.i = i
        self.j = j
        self.track = track
        self.lines = lines

    def is_in(self, x: int, y: int, device: Device) -> bool:
        is_at_left = self.is_at_left(x, y, device)
        is_track_left = self.is_track_left()

        return (
            self.is_track_full() or
            (is_at_left and is_track_left) or
            (not is_at_left and not is_track_left)
        )

    def is_at_left(self, x: int, y: int, device: Device) -> bool:
        is_at_bottom = self.is_at_bottom(x, y, device)
        is_track_up = self.is_track_up()

        return (
            (is_at_bottom and is_track_up) or
            (not is_at_bottom and not is_track_up)
        )

    def is_at_bottom(self, x: int, y: int, device: Device) -> bool:
        w_case = device.graphic.sizes.w_case
        h_case = device.graphic.sizes.h_case
        a = None
        b = None

        if self.is_track_up():
            a = (h_case - 1) / (w_case - 1)
            b = 0
        else:
            a = (1 - h_case) / (w_case - 1)
            b = h_case - 1

        return Math.round(a * (x % w_case) + b) <= y % h_case

    def is_track_up(self) -> bool:
        return (
            self.is_track(Shape.BOTTOM + Shape.LEFT) or
            self.is_track(Shape.TOP + Shape.RIGHT)
        )

    def is_track(self, track: int) -> bool:
        return Math.is_flag(self.track, track)

    def is_track_left(self) -> bool:
        return self.is_track_full() or self.is_track(Shape.LEFT)

    def is_track_full(self) -> bool:
        return self.is_track(Shape.FULL)

    def get_flags_inverse(self, flags: int, flip_w: bool, flip_h: bool) -> int:
        flags_flip = Shape.NONE

        if flip_w and Math.has_flag(flags, Shape.LEFT + Shape.RIGHT):
            flags_flip += Shape.LEFT + Shape.RIGHT
        else:
            pass

        if flip_h and Math.has_flag(flags, Shape.TOP + Shape.BOTTOM):
            flags_flip += Shape.TOP + Shape.BOTTOM
        else:
            pass

        if (
            ((flip_w and not flip_h) or (not flip_w and flip_h)) and
            Math.has_flag(flags, Shape.UP + Shape.DOWN)
        ):
            flags_flip += Shape.UP + Shape.DOWN
        else:
            pass

        return flags ^ flags_flip
