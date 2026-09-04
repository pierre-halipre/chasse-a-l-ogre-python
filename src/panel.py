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

from device import Device
from shape import Shape
from polygon import Polygon
from layout import Layout


class Panel(Layout):
    LEFT = 8
    RIGHT = 9

    def __init__(self, device: Device) -> None:
        super().__init__(device.graphic.menu.panel, device)

    def add_zones(self) -> None:
        self.zones.add(Panel.LEFT)
        self.zones.add(Panel.RIGHT)

    def get_polygon(self, zone: int) -> Polygon:
        result = Polygon()
        result.fill(0, 0, Shape.FULL, Shape.LEFT + Shape.TOP)
        result.fill(0, 1, Shape.FULL, Shape.LEFT)
        result.fill(0, 2, Shape.FULL, Shape.LEFT)
        result.fill(0, 3, Shape.FULL, Shape.LEFT + Shape.BOTTOM)
        result.fill(1, 0, Shape.FULL, Shape.TOP)
        result.fill(1, 1, Shape.FULL, Shape.NONE)
        result.fill(1, 2, Shape.FULL, Shape.NONE)
        result.fill(1, 3, Shape.FULL, Shape.BOTTOM)
        result.fill(2, 0, Shape.FULL, Shape.TOP)
        result.fill(2, 1, Shape.FULL, Shape.NONE)
        result.fill(2, 2, Shape.FULL, Shape.NONE)
        result.fill(2, 3, Shape.FULL, Shape.BOTTOM)
        result.fill(3, 0, Shape.FULL, Shape.RIGHT + Shape.TOP)
        result.fill(3, 1, Shape.FULL, Shape.RIGHT)
        result.fill(3, 2, Shape.FULL, Shape.RIGHT)
        result.fill(3, 3, Shape.FULL, Shape.RIGHT + Shape.BOTTOM)

        flip_w = not self.is_left_zone(zone)
        flip_h = False

        self.do_polygon(result, flip_w, flip_h)

        return result

    def get_ratio_sprite(self) -> float:
        return 0

    def get_i_case_zone(self, zone: int) -> int:
        result = None

        if zone == Panel.LEFT:
            result = 1
        else:
            result = 5

        return result

    def get_j_case_zone(self, zone: int) -> int:
        return 0

    def is_left_zone(self, zone: int) -> bool:
        return zone == Panel.LEFT
