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
from device import Device
from board import Board
from character import Character


class Monster(Character):
    TOUCH = 8

    def __init__(self, rank: int, board: Board, device: Device) -> None:
        super().__init__(rank, board, device)

        self.x = 0
        self.y = 0
        self.i_sheet_zone = board.get_zone_none()

    def set_touch(self) -> None:
        self.set_state(Monster.TOUCH)

    def is_touch(self) -> bool:
        return self.is_state(Monster.TOUCH)

    def is_end(self) -> bool:
        return super().is_end() or self.is_touch()

    def is_touchable(self) -> bool:
        return not self.is_end() and not self.is_fall()

    def start(self, zone: int, time_base: int, device: Device) -> None:
        super().start(zone, time_base, device)

        self.x = 0
        self.y = 0
        self.i_sheet_zone = self.zone

    def update(self, device: Device) -> None:
        if self.timer.is_on():
            self.timer.update()

            if not self.timer.is_on():
                if self.is_come():
                    self.set_wait(device)
                elif self.is_wait():
                    self.set_leave(device)
                elif self.is_leave():
                    self.set_out()
                elif self.is_fall():
                    self.set_touch()
                else:
                    pass
            else:
                pass
        else:
            pass

    def get_zone_position(self, board: Board) -> int:
        return self.zone

    def show(self, board: Board, device: Device) -> None:
        if not self.is_fall():
            zone = self.get_zone_position(board)
            x_start = board.get_x_limit_zone(zone, True, device)
            y_start = board.get_y_limit_zone(zone, True, device)
            x_end = board.get_x_zone(zone, device)
            y_end = board.get_y_zone(zone, device)
            ratio = self.get_ratio_position()
            self.x = Math.distance(x_start, x_end, ratio)
            self.y = Math.distance(y_start, y_end, ratio)
            self.i_sheet_zone = self.get_i_sheet_zone(board)
        else:
            pass

        if device.design.mode == 0:
            self.show_positions(board, device)
        else:
            self.draw(self.x, self.y, board, device)

    def show_positions(self, board: Board, device: Device) -> None:
        zone = self.get_zone_position(board)

        for position in range(0, 3, 1):
            i_case = None
            j_case = None

            if board.is_horizon_zone(zone):
                i_case = (position + 1) % 2

                if board.is_western_zone(zone):
                    i_case *= -1
                else:
                    pass

                j_case = position - 1
            else:
                i_case = (position + 2) % 2

                if board.is_western_zone(zone):
                    i_case *= -1
                else:
                    pass

                j_case = position

                if board.is_northern_zone(zone):
                    j_case -= 2
                else:
                    pass

            w = device.graphic.sizes.to_w_cases(i_case)
            h = device.graphic.sizes.to_h_cases(j_case)
            x_sprite = self.x + w
            y_sprite = self.y + h
            self.draw(x_sprite, y_sprite, board, device)

    def get_x_cherry(self, board: Board, device: Device) -> int:
        zone_start = board.get_zone_center()
        x_start = board.get_x_zone(zone_start, device)
        x_end = board.get_x_limit_zone(self.zone, True, device)
        ratio = self.timer.get_ratio()

        return Math.distance(x_start, x_end, ratio)

    def get_y_cherry(self, board: Board, device: Device) -> int:
        zone_start = board.get_zone_center()
        y_start = board.get_y_zone(zone_start, device)
        y_end = board.get_y_limit_zone(self.zone, True, device)
        ratio = self.timer.get_ratio()

        return Math.distance(y_start, y_end, ratio)

    def get_i_sheet_state(self) -> int:
        result = None

        if self.is_come() or self.is_leave():
            result = 0
        elif self.is_wait():
            result = 6
        else:
            result = 12

        return result

    def get_i_sheet_zone(self, board: Board) -> int:
        result = None

        if self.is_fall():
            result = self.i_sheet_zone
        else:
            zone = None

            if self.is_leave():
                zone = board.get_zone_inverse(self.zone)
            else:
                zone = self.zone

            result = board.to_i_zone(zone)

        return result

    @abstractmethod
    def is_enemy(self) -> bool:
        pass

    @abstractmethod
    def get_accuracy_tally(self) -> float:
        pass

    @abstractmethod
    def get_score_tally(self) -> int:
        pass
