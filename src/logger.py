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
from board import Board
from character import Character


class Logger(Character):
    HIT_GOOD = 6
    HIT_BAD = 7

    def set_hit_good(self) -> None:
        self.set_state(Logger.HIT_GOOD)

    def is_hit_good(self) -> bool:
        return self.is_state(Logger.HIT_GOOD)

    def set_hit_bad(self) -> None:
        self.set_state(Logger.HIT_BAD)

    def is_hit_bad(self) -> bool:
        return self.is_state(Logger.HIT_BAD)

    def is_hit(self) -> bool:
        return self.is_hit_good() or self.is_hit_bad()

    def update(self, device: Device) -> None:
        if self.timer.is_on():
            self.timer.update()

            if not self.timer.is_on():
                if self.is_leave():
                    self.set_out()
                else:
                    self.set_wait(device)
            else:
                pass
        else:
            pass

    def get_zone_position(self, board: Board) -> int:
        return board.get_zone_center()

    def show(self, board: Board, device: Device) -> None:
        zone_position = self.get_zone_position(board)
        x = board.get_x_zone(zone_position, device)
        y = board.get_y_zone(zone_position, device)
        self.draw(x, y, board, device)

    def can_draw(self, device: Device) -> bool:
        return (
            super().can_draw(device) and
            (not self.is_hit_bad() or not self.timer.is_blink(device))
        )

    def get_i_sheet_state(self) -> int:
        result = None

        if self.is_wait():
            result = 0
        elif self.is_hit() or self.is_come() or self.is_leave():
            result = 6
        else:
            result = 12

        return result

    def get_i_sheet_zone(self, board: Board) -> int:
        zone_sheet = board.get_zone_inverse(self.zone)

        return board.to_i_zone(zone_sheet)
