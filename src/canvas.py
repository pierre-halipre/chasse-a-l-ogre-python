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
from tool import Area
from tool import Image
from rasters import RastersCanvas
from device import Device
from sprite import Sprite


class Canvas:
    def __init__(self, rasters_canvas: RastersCanvas, device: Device) -> None:
        self.x = rasters_canvas.x
        self.y = rasters_canvas.y
        self.n_w_cases = rasters_canvas.n_w_cases
        self.n_h_cases = rasters_canvas.n_h_cases

        self.sprite = Sprite(rasters_canvas)
        self.sprite.add_sheet(0, False, device)
        self.sprite.add_sheet(0, True, device)
        self.sprite.add_sheet(1, False, device)
        self.sprite.add_sheet(1, True, device)

    def is_in(self, device: Device) -> bool:
        x_event = device.event.x
        y_event = device.event.y
        w = device.graphic.sizes.to_w_cases(self.n_w_cases)
        h = device.graphic.sizes.to_h_cases(self.n_h_cases)
        x_max = self.x + w
        y_max = self.y + h

        return self.x <= x_event < x_max and self.y <= y_event < y_max

    def show(self, is_foreground: bool, device: Device) -> None:
        i_sheet_start = None

        if is_foreground:
            i_sheet_start = 0
        else:
            i_sheet_start = 2

        i_sheet_left = i_sheet_start
        i_sheet_right = i_sheet_start + 1
        ratio_left = self.get_ratio_sprite()
        ratio_right = (ratio_left + 1 / 2) % 1
        x_left = self.x
        x_middle = device.graphic.sizes.to_w_cases(Math.half(self.n_w_cases))
        x_right = x_left + x_middle
        y_top = self.y
        image_left = self.sprite.get_image(i_sheet_left, ratio_left, device)
        image_right = self.sprite.get_image(i_sheet_right, ratio_right, device)
        self.sprite.draw(image_left, x_left, y_top, device)
        self.sprite.draw(image_right, x_right, y_top, device)

    @abstractmethod
    def get_ratio_sprite(self) -> float:
        pass

    def draw_image(self, image: Image, x: int, y: int, device: Device) -> None:
        x_image = None
        y_image = None

        if x < self.x:
            x_image = self.x
        else:
            x_image = x

        if y < self.y:
            y_image = self.y
        else:
            y_image = y

        area = self.get_area(image, x, y, device)
        device.graphic.window.on_image(x_image, y_image, image, area)

    def get_area(self, image: Image, x: int, y: int, device: Device) -> Area:
        x_left = None
        x_right = None
        y_top = None
        y_bottom = None
        w_image = image.get_w()
        h_image = image.get_h()
        w = device.graphic.sizes.to_w_cases(self.n_w_cases)
        h = device.graphic.sizes.to_h_cases(self.n_h_cases)

        if x < self.x:
            x_left = self.x - x
            x_right = w_image
        elif x + w_image > self.x + w:
            x_left = 0
            x_right = self.x + w - x
        else:
            x_left = 0
            x_right = w_image

        if y < self.y:
            y_top = self.y - y
            y_bottom = h_image
        elif y + h_image > self.y + h:
            y_top = 0
            y_bottom = self.y + h - y
        else:
            y_top = 0
            y_bottom = h_image

        return image.get_area(x_left, y_top, x_right, y_bottom)
