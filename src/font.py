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
from device import Device
from sprite import Sprite
from canvas import Canvas


class Font:
    def __init__(self, device: Device) -> None:
        self.sprite = Sprite(device.graphic.frame.font)
        self.sprite.add_sheet(0, False, device)

        self.paragraph = Array()
        line = 0

        while line < 3:
            self.paragraph.add(None)
            line += 1

    def set_home(self, device: Device) -> None:
        paragraph_home = device.text.home.get(device.design.mode)

        self.paragraph.set(0, paragraph_home.get(0))
        self.paragraph.set(1, paragraph_home.get(1))
        self.paragraph.set(2, paragraph_home.get(2))

    def set_end(self, score: int, device: Device) -> None:
        device.text.set_custom_end(score, device.design)
        paragraph_end = device.text.end.get(device.design.mode)

        self.paragraph.set(0, paragraph_end.get(0))
        self.paragraph.set(1, paragraph_end.get(1))
        self.paragraph.set(2, device.text.custom)

    def set_pause(self, ticks: int, device: Device) -> None:
        milliseconds = None

        if ticks >= device.clock.get_ticks_max():
            milliseconds = 3599999
        else:
            milliseconds = ticks * device.clock.get_refresh_time()

        device.text.set_custom_pause(milliseconds, device.design)
        paragraph_pause = device.text.pause.get(device.design.mode)

        self.paragraph.set(0, paragraph_pause.get(0))
        self.paragraph.set(1, paragraph_pause.get(1))
        self.paragraph.set(2, device.text.custom)

    def show(self, canvas: Canvas, device: Device) -> None:
        for line in range(0, self.paragraph.get_size(), 1):
            sentence = self.paragraph.get(line)

            y_line = device.graphic.sizes.to_h_cases(9 + line * 3)
            y = canvas.y + y_line

            for i in range(0, sentence.get_size(), 1):
                i_sheet = 0
                unicode = sentence.get(i)
                ratio = self.get_ratio_sprite(unicode)
                image = self.sprite.get_image(i_sheet, ratio, device)

                x_word = device.graphic.sizes.to_w_cases(1 + i)
                x = canvas.x + x_word

                canvas.draw_image(image, x, y, device)

    def get_ratio_sprite(self, unicode: int) -> float:
        i_image = None

        if 48 <= unicode <= 57:
            i_image = unicode - 48
        elif 65 <= unicode <= 90:
            i_image = unicode - 55
        elif unicode == 46:
            i_image = 36
        elif unicode == 33:
            i_image = 37
        elif unicode == 58:
            i_image = 38
        elif unicode == 39:
            i_image = 39
        else:
            i_image = 40

        return i_image / 41
