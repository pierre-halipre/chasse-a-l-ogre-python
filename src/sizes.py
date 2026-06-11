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


class Sizes:
    def __init__(self, w_screen: int, h_screen: int) -> None:
        self.w_case = None
        self.h_case = None
        self.set_size_case(w_screen, h_screen)

        self.w_sprite = None
        self.h_sprite = None
        slope = (self.h_case - 1) / (self.w_case - 1)
        origin = self.h_case - 1
        self.set_size_sprite(slope, origin)

    def set_size_case(self, w_screen: int, h_screen: int) -> None:
        ratio_w_case = Math.sqrt(3) / 2
        ratio_h_case = 1 / 2
        ratio_w_screen = 8 * ratio_w_case + 2 * ratio_h_case
        ratio_h_screen = 22 * ratio_h_case

        diagonal_case_from_w = Math.floor(w_screen / ratio_w_screen)
        diagonal_case_from_h = Math.floor(h_screen / ratio_h_screen)
        diagonal_case = Math.min(diagonal_case_from_w, diagonal_case_from_h)

        self.w_case = Math.floor(diagonal_case * ratio_w_case * 3 / 4)
        self.h_case = Math.floor(diagonal_case * ratio_h_case * 3 / 4)

    def set_size_sprite(self, slope: float, origin: int) -> None:
        x_top_left = self.get_x_top_left_sprite(-slope, origin)
        y_top_left = self.get_y_sprite(x_top_left, -slope, origin)

        x_top_right = self.get_x_top_right_sprite(slope, 0)
        y_top_right = self.get_y_sprite(x_top_right, slope, 0)

        x_bottom_left = self.get_x_bottom_left_sprite(slope, 0)
        y_bottom_left = self.get_y_sprite(x_bottom_left, slope, 0)

        x_bottom_right = self.get_x_bottom_right_sprite(-slope, origin)
        y_bottom_right = self.get_y_sprite(x_bottom_right, -slope, origin)

        x_left = Math.max(x_top_left, x_bottom_left)
        x_right = Math.min(x_top_right, x_bottom_right)
        y_top = Math.max(y_top_left, y_top_right)
        y_bottom = Math.min(y_bottom_left, y_bottom_right) + 1

        self.w_sprite = 2 * self.w_case - x_left - (self.w_case - 1 - x_right)
        self.h_sprite = 4 * self.h_case - y_top - (self.h_case - 1 - y_bottom)

    def get_x_top_left_sprite(self, slope: float, origin: int) -> int:
        a = slope
        b = origin

        return Math.round(((self.w_case - 2 * self.h_case + b) / (1 - a)))

    def get_x_top_right_sprite(self, slope: float, origin: int) -> int:
        a = slope
        b = origin

        return Math.round((2 * self.h_case - b - 1) / (1 + a))

    def get_x_bottom_left_sprite(self, slope: float, origin: int) -> int:
        a = slope
        b = origin

        return Math.round((self.w_case - self.h_case - 1 - b) / (1 + a))

    def get_x_bottom_right_sprite(self, slope: float, origin: int) -> int:
        a = slope
        b = origin

        return Math.round((self.h_case + b) / (1 - a))

    def get_y_sprite(self, x: int, slope: float, origin: int) -> int:
        return Math.round(slope * x + origin)

    def to_w_cases(self, n: int) -> int:
        return n * self.w_case

    def to_h_cases(self, n: int) -> int:
        return n * self.h_case

    def to_i_case(self, x: int) -> int:
        return Math.floor(x / self.w_case)

    def to_j_case(self, y: int) -> int:
        return Math.floor(y / self.h_case)
