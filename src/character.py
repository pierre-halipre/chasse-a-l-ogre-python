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
from board import Board
from profil import Profil


class Character(Profil):
    def __init__(self, rank: int, board: Board, device: Device) -> None:
        super().__init__(rank, board, device)

        self.zone = board.get_zone_none()

    def start(self, zone: int, time_base: int, device: Device) -> None:
        self.zone = zone
        self.time_base = time_base
        self.set_come(device)

    @abc.abstractmethod
    def get_zone_position(self, board: Board) -> int:
        pass

    @abc.abstractmethod
    def show(self, board: Board, device: Device) -> None:
        pass

    def draw(self, x: int, y: int, board: Board, device: Device) -> None:
        if self.can_draw(device):
            i_sheet_state = self.get_i_sheet_state()
            i_sheet_zone = self.get_i_sheet_zone(board)
            i_sheet = i_sheet_state + i_sheet_zone
            ratio = self.get_ratio_sprite()
            image = self.sprite.get_image(i_sheet, ratio, device)
            board.draw_image(image, x, y, device)
        else:
            pass

    def can_draw(self, device: Device) -> bool:
        return not self.is_fall() or not self.timer.is_blink(device)

    @abc.abstractmethod
    def get_i_sheet_state(self) -> int:
        pass

    @abc.abstractmethod
    def get_i_sheet_zone(self, board: Board) -> int:
        pass
