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

from dataclasses import dataclass
from device import Device
from sprite import Sprite
from panel import Panel
from party import Party


@dataclass
class Buttons:
    def __init__(self, device: Device) -> None:
        self.sprite = Sprite(device.graphic.menu.buttons)

        for i_sheet in range(0, 6, 1):
            j_sprite = i_sheet
            self.sprite.add_sheet(j_sprite, False, device)

    def show(self, panel: Panel, party: Party, device: Device) -> None:
        ratio = 0

        for i in range(0, panel.zones.get_size(), 1):
            zone = panel.zones.get(i)
            i_sheet = None

            if panel.is_left_zone(zone):
                if party.is_home() or party.is_quit():
                    i_sheet = 0
                elif party.is_play():
                    i_sheet = 1
                elif party.is_pause():
                    i_sheet = 2
                else:
                    i_sheet = 3
            elif party.is_home() or party.is_quit():
                i_sheet = 5
            else:
                i_sheet = 4

            x = panel.get_x_zone(zone, device)
            y = panel.get_y_zone(zone, device)
            image = self.sprite.get_image(i_sheet, ratio, device)
            panel.draw_image(image, x, y, device)
