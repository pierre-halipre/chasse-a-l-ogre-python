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
from tool import Array
from device import Device
from board import Board
from monster import Monster
from enemy import Enemy
from friend import Friend


class Monsters:
    def __init__(self, board: Board, device: Device) -> None:
        zombie = Enemy(0, board, device)
        vampire = Enemy(1, board, device)
        deer = Friend(2, board, device)
        skeleton = Enemy(3, board, device)
        ghost = Enemy(4, board, device)
        rabbit = Friend(5, board, device)

        self.raws = Array()
        self.raws.add(zombie)
        self.raws.add(vampire)
        self.raws.add(deer)
        self.raws.add(skeleton)
        self.raws.add(ghost)
        self.raws.add(rabbit)

        self.ranks = 0

        self.currents = Array()
        rank = 0

        while rank < 5:
            self.currents.add(None)
            rank += 1

    def reset(self) -> None:
        for i in range(0, self.currents.get_size(), 1):
            monster = self.get_raw(i)
            monster.set_none()

        self.ranks = 0

        for rank in range(0, self.currents.get_size(), 1):
            self.currents.set(rank, None)

    def get_raw(self, i: int) -> Monster:
        return self.raws.get(i)

    def get(self, rank: int) -> Monster:
        return self.currents.get(rank)

    def set(self, rank: int, monster: Monster) -> None:
        self.currents.set(rank, monster)

    def is_end(self) -> bool:
        result = True

        for rank in range(0, self.ranks, 1):
            monster = self.get(rank)

            if not monster.is_end():
                result = False
            else:
                pass

        return result

    def can_start_next(self, level: int, device: Device) -> bool:
        result = True

        threshold_min = device.clock.get_n_animations_min()
        n_touchables = 0
        rank_max = self.get_rank_max(level)

        for rank in range(0, self.ranks, 1):
            monster = self.get(rank)

            if (
                (monster.is_come() or monster.is_fall()) and
                monster.timer.counts < threshold_min
            ):
                result = False
            elif monster.is_touchable():
                n_touchables += 1

                if n_touchables >= rank_max:
                    result = False
                else:
                    pass
            else:
                pass

        return result

    def get_rank_max(self, level: int) -> int:
        return level + 1

    def get_zone_next(self, board: Board) -> int:
        result = None

        size_zones = board.zones.get_size()
        zone_start = Math.rand(size_zones)

        for i in range(zone_start, zone_start + size_zones, 1):
            zone = board.zones.get(i % size_zones)
            is_forbidden = False

            for rank in range(0, self.ranks, 1):
                monster = self.get(rank)

                if not monster.is_end() and monster.zone == zone:
                    is_forbidden = True
                else:
                    pass

            if not is_forbidden:
                result = zone
            else:
                pass

        return result

    def get_next(self, level: int) -> Monster:
        result = None

        size_raws = self.raws.get_size()
        i_start = Math.rand(size_raws)

        n_friends = self.get_n_friends()
        rank_max = self.get_rank_max(level)

        for i in range(i_start, i_start + size_raws, 1):
            monster = self.get_raw(i % size_raws)
            is_forbidden = False

            for rank in range(0, self.ranks, 1):
                if (
                    monster is self.get(rank) or
                    (
                        not monster.is_enemy() and
                        n_friends == 1 and
                        rank_max == 2
                    )
                ):
                    is_forbidden = True
                else:
                    pass

            if not is_forbidden:
                result = monster
            else:
                pass

        return result

    def get_n_friends(self) -> int:
        result = 0

        for rank in range(0, self.ranks, 1):
            monster = self.get(rank)

            if not monster.is_enemy() and monster.is_touchable():
                result += 1
            else:
                pass

        return result

    def is_attack(self, zone: int) -> bool:
        result = False

        for rank in range(0, self.ranks, 1):
            monster = self.get(rank)

            if (
                monster.is_enemy() and
                monster.is_wait() and
                monster.zone == zone
            ):
                result = True
            else:
                pass

        return result

    def show(self, northern_zone: bool, board: Board, device: Device) -> None:
        for rank in range(0, self.ranks, 1):
            monster = self.get(rank)

            if (
                not monster.is_end() and
                board.can_draw_zone(monster.zone, northern_zone)
            ):
                monster.show(board, device)
            else:
                pass
