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
from panel import Panel
from audios import AudiosMenu
from gui import Gui
from party import Party
from buttons import Buttons


class Menu(Gui):
    def __init__(self, device: Device) -> None:
        super().__init__(Panel(device), AudiosMenu(device))

        self.party = Party()

        self.buttons = Buttons(device)

        self.need_reset = False
        self.need_resume = False

    def reset(self) -> None:
        self.party.set_home()

        self.need_reset = True
        self.need_resume = False

        self.audios.theme.set_play()

    def update(self, zone: int, device: Device) -> None:
        if self.layout.is_in_zones(zone):
            is_left_zone = self.layout.is_left_zone(zone)

            if is_left_zone:
                if self.party.is_play():
                    self.party.set_pause()

                    self.audios.buttons_pause.set_play()
                else:
                    if self.party.is_pause():
                        self.need_resume = True

                        self.audios.buttons_resume.set_play()
                    else:
                        self.need_reset = True

                    self.party.set_play()
            elif self.party.is_home():
                self.party.set_quit()
            else:
                self.party.set_home()

                self.need_reset = True

                self.audios.theme.set_play()
        else:
            pass

    def show_elements(self, device: Device) -> None:
        self.buttons.show(self.layout, self.party, device)
