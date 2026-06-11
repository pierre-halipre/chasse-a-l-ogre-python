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
from device import Device
from layout import Layout
from pen import Pen
from audios import Audios


class Gui(abc.ABC):
    def __init__(self, layout: Layout, audios: Audios) -> None:
        self.layout = layout
        self.audios = audios

    @abc.abstractmethod
    def reset(self) -> None:
        pass

    @abc.abstractmethod
    def update(self, zone: int, device: Device) -> None:
        pass

    def show(self, pen: Pen, device: Device) -> None:
        self.layout.show(False, device)

        self.show_elements(device)

        self.layout.show(True, device)

        for i in range(0, self.layout.polygons.get_size(), 1):
            polygon = self.layout.polygons.get(i)
            pen.show(polygon, self.layout, device)

    @abc.abstractmethod
    def show_elements(self, device: Device) -> None:
        pass

    def play(self, device: Device) -> None:
        if self.audios.need_play():
            songs = self.audios.get_songs()
            songs.play(device.music)
        else:
            pass
