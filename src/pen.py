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
from sprite import Sprite
from shape import Shape
from polygon import Polygon
from canvas import Canvas


class Pen:
    def __init__(self, device: Device) -> None:
        rasters_case = device.graphic.frame.pen
        self.sprite = Sprite(rasters_case)

        for i_sheet in range(0, 4, 1):
            j_sprite = i_sheet
            self.sprite.add_sheet(j_sprite, False, device)

    def show(self, polygon: Polygon, canvas: Canvas, device: Device) -> None:
        for i in range(0, polygon.get_size(), 1):
            shape = polygon.get(i)
            self.draw(shape, canvas, device)

    def draw(self, shape: Shape, canvas: Canvas, device: Device) -> None:
        if shape.lines != Shape.NONE:
            sheets = self.sprite.get(device.design.mode)
            i_sheet = 0
            sheet = sheets.get(i_sheet)

            for bit in range(0, 8, 1):
                if Math.is_flag(shape.lines, Math.pow(2, bit)):
                    i_image = bit
                    image = sheet.get(i_image)
                    w = device.graphic.sizes.to_w_cases(shape.i)
                    h = device.graphic.sizes.to_h_cases(shape.j)
                    x = canvas.x + w
                    y = canvas.y + h
                    canvas.draw_image(image, x, y, device)
                else:
                    pass
        else:
            pass
