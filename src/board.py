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
from timer import Timer
from sprite import Sprite
from shape import Shape
from polygon import Polygon
from layout import Layout


class Board(Layout):
    NW = 1
    W = 2
    SW = 3
    NE = 4
    E = 5
    SE = 6
    C = 7

    def __init__(self, device: Device) -> None:
        super().__init__(device.graphic.game.board, device)

        self.timer = Timer()

        self.polygon_center = Polygon()
        self.polygon_center.fill(3, 6, Shape.BOTTOM + Shape.RIGHT, Shape.NONE)
        self.polygon_center.fill(3, 7, Shape.FULL, Shape.NONE)
        self.polygon_center.fill(3, 8, Shape.FULL, Shape.NONE)
        self.polygon_center.fill(3, 9, Shape.TOP + Shape.RIGHT, Shape.NONE)
        self.polygon_center.fill(4, 6, Shape.BOTTOM + Shape.LEFT, Shape.NONE)
        self.polygon_center.fill(4, 7, Shape.FULL, Shape.NONE)
        self.polygon_center.fill(4, 8, Shape.FULL, Shape.NONE)
        self.polygon_center.fill(4, 9, Shape.TOP + Shape.LEFT, Shape.NONE)

    def get_ratio_sprite(self) -> float:
        return self.timer.get_ratio()

    def add_zones(self) -> None:
        self.zones.add(Board.NW)
        self.zones.add(Board.W)
        self.zones.add(Board.SW)
        self.zones.add(Board.NE)
        self.zones.add(Board.E)
        self.zones.add(Board.SE)

    def get_polygon(self, zone: int) -> Polygon:
        result = None

        flip_w = None
        flip_h = None

        if self.is_horizon_zone(zone):
            result = self.get_polygon_horizon()
            flip_w = not self.is_western_zone(zone)
            flip_h = False
        else:
            result = self.get_polygon_corner()
            flip_w = self.is_eastern_zone(zone)
            flip_h = self.is_southern_zone(zone)

        self.do_polygon(result, flip_w, flip_h)

        return result

    def get_polygon_horizon(self) -> Polygon:
        result = Polygon()
        result.fill(0, 4, Shape.LEFT + Shape.BOTTOM, Shape.UP + Shape.LEFT)
        result.fill(0, 5, Shape.FULL, Shape.LEFT)
        result.fill(0, 6, Shape.FULL, Shape.LEFT)
        result.fill(0, 7, Shape.FULL, Shape.LEFT)
        result.fill(0, 8, Shape.FULL, Shape.LEFT)
        result.fill(0, 9, Shape.FULL, Shape.LEFT)
        result.fill(0, 10, Shape.FULL, Shape.LEFT)
        result.fill(0, 11, Shape.LEFT + Shape.TOP, Shape.DOWN + Shape.LEFT)
        result.fill(1, 5, Shape.LEFT + Shape.BOTTOM, Shape.UP)
        result.fill(1, 6, Shape.FULL, Shape.NONE)
        result.fill(1, 7, Shape.FULL, Shape.NONE)
        result.fill(1, 8, Shape.FULL, Shape.NONE)
        result.fill(1, 9, Shape.FULL, Shape.NONE)
        result.fill(1, 10, Shape.LEFT + Shape.TOP, Shape.DOWN)
        result.fill(2, 6, Shape.LEFT + Shape.BOTTOM, Shape.UP)
        result.fill(2, 7, Shape.FULL, Shape.RIGHT)
        result.fill(2, 8, Shape.FULL, Shape.RIGHT)
        result.fill(2, 9, Shape.LEFT + Shape.TOP, Shape.DOWN)

        return result

    def get_polygon_corner(self) -> Polygon:
        result = Polygon()
        result.fill(0, 3, Shape.RIGHT + Shape.BOTTOM, Shape.DOWN)
        result.fill(0, 4, Shape.RIGHT + Shape.TOP, Shape.NONE)
        result.fill(1, 2, Shape.RIGHT + Shape.BOTTOM, Shape.DOWN)
        result.fill(1, 3, Shape.FULL, Shape.NONE)
        result.fill(1, 4, Shape.FULL, Shape.NONE)
        result.fill(1, 5, Shape.RIGHT + Shape.TOP, Shape.NONE)
        result.fill(2, 1, Shape.RIGHT + Shape.BOTTOM, Shape.DOWN)
        result.fill(2, 2, Shape.FULL, Shape.NONE)
        result.fill(2, 3, Shape.FULL, Shape.NONE)
        result.fill(2, 4, Shape.FULL, Shape.NONE)
        result.fill(2, 5, Shape.FULL, Shape.NONE)
        result.fill(2, 6, Shape.RIGHT + Shape.TOP, Shape.NONE)
        result.fill(3, 0, Shape.RIGHT + Shape.BOTTOM, Shape.DOWN + Shape.RIGHT)
        result.fill(3, 1, Shape.FULL, Shape.RIGHT)
        result.fill(3, 2, Shape.FULL, Shape.RIGHT)
        result.fill(3, 3, Shape.FULL, Shape.RIGHT)
        result.fill(3, 4, Shape.FULL, Shape.RIGHT)
        result.fill(3, 5, Shape.FULL, Shape.RIGHT)
        result.fill(3, 6, Shape.LEFT + Shape.TOP, Shape.DOWN)

        return result

    def find_zone(self, device: Device) -> int:
        result = None

        if self.is_in_polygon(self.polygon_center, device):
            result = self.get_zone_center()
        else:
            result = super().find_zone(device)

        return result

    def get_zone_center(self) -> int:
        return Board.C

    def get_i_case_zone(self, zone: int) -> int:
        result = None

        if self.is_western_zone(zone):
            if self.is_northern_zone(zone) or self.is_southern_zone(zone):
                result = 2
            else:
                result = 1
        elif self.is_northern_zone(zone) or self.is_southern_zone(zone):
            result = 4
        elif self.is_eastern_zone(zone):
            result = 5
        else:
            result = 3

        return result

    def get_j_case_zone(self, zone: int) -> int:
        result = None

        if self.is_northern_zone(zone):
            result = 3
        elif self.is_southern_zone(zone):
            result = 9
        else:
            result = 6

        return result

    def get_x_limit_zone(self, zone: int, far: bool, device: Device) -> int:
        offset = None

        if self.is_horizon_zone(zone):
            offset = 2
        else:
            offset = 1

        sign = None

        if self.is_western_zone(zone):
            sign = -1
        else:
            sign = 1

        if not far:
            offset -= 1
            sign *= -1
        else:
            pass

        i_case_zone = self.get_i_case_zone(zone)
        i_case_zone_limit = i_case_zone + offset * sign

        return self.get_x_case(i_case_zone_limit, device)

    def get_y_limit_zone(self, zone: int, far: bool, device: Device) -> int:
        offset = None
        sign = None

        if self.is_horizon_zone(zone):
            offset = 0
            sign = 0
        else:
            offset = 3

            if self.is_northern_zone(zone):
                sign = -1
            else:
                sign = 1

            if not far:
                offset -= 2
                sign *= -1
            else:
                pass

        j_case_zone = self.get_j_case_zone(zone)
        j_case_zone_limit = j_case_zone + offset * sign

        return self.get_y_case(j_case_zone_limit, device)

    def is_northern_zone(self, zone: int) -> bool:
        return zone in (Board.NW, Board.NE)

    def is_southern_zone(self, zone: int) -> bool:
        return zone in (Board.SW, Board.SE)

    def is_western_zone(self, zone: int) -> bool:
        return zone in (Board.NW, Board.W, Board.SW)

    def is_eastern_zone(self, zone: int) -> bool:
        return zone in (Board.NE, Board.E, Board.SE)

    def is_horizon_zone(self, zone: int) -> bool:
        return zone in (Board.W, Board.E)

    def get_zone_inverse(self, zone: int) -> int:
        result = None

        if zone == Board.NW:
            result = Board.SE
        elif zone == Board.W:
            result = Board.E
        elif zone == Board.SW:
            result = Board.NE
        elif zone == Board.NE:
            result = Board.SW
        elif zone == Board.E:
            result = Board.W
        else:
            result = Board.NW

        return result

    def can_draw_zone(self, zone: int, northern_zone: bool) -> bool:
        return self.is_northern_zone(zone) is northern_zone

    def fill_sprite(self, sprite: Sprite, n_acts: int, device: Device) -> None:
        size_zones = self.zones.get_size()
        half_size_zones = Math.half(size_zones)

        for act in range(0, n_acts, 1):
            j_start_sprite = act * half_size_zones

            for i in range(0, size_zones, 1):
                zone = self.zones.get(i)
                flip_w = None
                j_sprite = None

                if self.is_eastern_zone(zone):
                    flip_w = True
                    j_sprite = j_start_sprite + i - half_size_zones
                else:
                    flip_w = False
                    j_sprite = j_start_sprite + i

                sprite.add_sheet(j_sprite, flip_w, device)
