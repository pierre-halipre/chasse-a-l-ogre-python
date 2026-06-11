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

import abc
from tool import Array
from rasters import RastersCanvas
from device import Device
from canvas import Canvas
from polygon import Polygon


class Layout(Canvas):
    NONE = 0

    def __init__(self, rasters_canvas: RastersCanvas, device: Device) -> None:
        super().__init__(rasters_canvas, device)

        self.zones = Array()
        self.add_zones()

        self.polygons = Array()

        for i in range(0, self.zones.get_size(), 1):
            zone = self.zones.get(i)
            polygon = self.get_polygon(zone)
            self.polygons.add(polygon)

    @abc.abstractmethod
    def add_zones(self) -> None:
        pass

    @abc.abstractmethod
    def get_polygon(self, zone: int) -> Polygon:
        pass

    def do_polygon(self, polygon: Polygon, flip_w: bool, flip_h: bool) -> None:
        i_max = self.n_w_cases - 1
        j_max = self.n_h_cases - 1
        polygon.flip(flip_w, flip_h, i_max, j_max)

    def is_in_zones(self, zone: int) -> bool:
        result = False

        for i in range(0, self.zones.get_size(), 1):
            if self.zones.get(i) == zone:
                result = True
            else:
                pass

        return result

    def find_zone(self, device: Device) -> int:
        result = self.get_zone_none()

        for k in range(0, self.zones.get_size(), 1):
            zone = self.zones.get(k)
            i_zone = self.to_i_zone(zone)
            polygon = self.polygons.get(i_zone)

            if self.is_in_polygon(polygon, device):
                result = zone
            else:
                pass

        return result

    def is_in_polygon(self, polygon: Polygon, device: Device) -> bool:
        result = False

        x = device.event.x - self.x
        y = device.event.y - self.y
        i = device.graphic.sizes.to_i_case(x)
        j = device.graphic.sizes.to_j_case(y)

        for k in range(0, polygon.get_size(), 1):
            shape = polygon.get(k)

            if shape.i == i and shape.j == j and shape.is_in(x, y, device):
                result = True
            else:
                pass

        return result

    def get_zone_none(self) -> int:
        return Layout.NONE

    def to_i_zone(self, zone: int) -> int:
        result = None

        for i in range(0, self.zones.get_size(), 1):
            if self.zones.get(i) == zone:
                result = i
            else:
                pass

        return result

    def get_x_zone(self, zone: int, device: Device) -> int:
        i = self.get_i_case_zone(zone)

        return self.get_x_case(i, device)

    def get_x_case(self, i: int, device: Device) -> int:
        w = device.graphic.sizes.to_w_cases(i)

        return self.x + w

    def get_y_zone(self, zone: int, device: Device) -> int:
        j = self.get_j_case_zone(zone)

        return self.get_y_case(j, device)

    def get_y_case(self, j: int, device: Device) -> int:
        h = device.graphic.sizes.to_h_cases(j)

        return self.y + h

    @abc.abstractmethod
    def get_i_case_zone(self, zone: int) -> int:
        pass

    @abc.abstractmethod
    def get_j_case_zone(self, zone: int) -> int:
        pass
