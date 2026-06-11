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

from tool import Array
from shape import Shape


class Polygon(Array):
    def fill(self, i: int, j: int, tracks: int, lines: int) -> None:
        shape = Shape(i, j, tracks, lines)
        self.add(shape)

    def flip(self, flip_w: bool, flip_h: bool, i_max: int, j_max: int) -> None:
        for i in range(0, self.get_size(), 1):
            shape = self.get(i)

            if flip_w:
                shape.i = i_max - shape.i
            else:
                pass

            if flip_h:
                shape.j = j_max - shape.j
            else:
                pass

            shape.track = shape.get_flags_inverse(shape.track, flip_w, flip_h)
            shape.lines = shape.get_flags_inverse(shape.lines, flip_w, flip_h)
