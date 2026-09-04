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

from tool import Math, Array, Image
from device import Device
from rasters import Rasters


class Sprite(Array):
    def __init__(self, rasters: Rasters) -> None:
        super().__init__()

        self.rasters = rasters
        mode = 0

        while mode < self.rasters.get_size():
            self.add(Array())
            mode += 1

    def add_sheet(self, j_sprite: int, flip_w: bool, device: Device) -> None:
        sizes = device.graphic.sizes

        for mode in range(0, self.get_size(), 1):
            sheet = Array()
            sheets = self.get(mode)
            sheets.add(sheet)

            for i_image in range(0, self.rasters.get_n_sprites(mode), 1):
                i_sprite = self.rasters.get_i_sprite(mode, i_image)
                sprite = self.rasters.get_sprite(mode, i_sprite, j_sprite)
                image = self.rasters.get_image(sprite, flip_w, sizes)
                sheet.add(image)

    def get_image(self, i_sheet: int, ratio: float, device: Device) -> Image:
        sheets = self.get(device.design.mode)
        sheet = sheets.get(i_sheet)
        n_images = sheet.get_size()
        i_image = Math.floor(n_images * ratio)

        return sheet.get(i_image)

    def draw(self, image: Image, x: int, y: int, device: Device) -> None:
        image.on_window(x, y, device.graphic.window)
