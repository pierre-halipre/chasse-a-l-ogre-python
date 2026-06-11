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
from layout import Layout
from menu import Menu
from character import Character
from logger import Logger
from monster import Monster
from game import Game


class Action:
    def __init__(self) -> None:
        self.zone = Layout.NONE

        self.need_quit = False

        self.counts_change = 0
        self.ticks_change = 0

    def reset(self) -> None:
        self.zone = Layout.NONE

    def set_quit(self) -> None:
        self.need_quit = True

    def check_change_design(self, game: Game, device: Device) -> None:
        if self.zone == game.layout.get_zone_center():
            clock = device.clock
            time_range = clock.time_animation_max - clock.time_animation_min
            n_counts_change = clock.to_ticks(time_range)

            if game.ticks - self.ticks_change <= n_counts_change:
                self.counts_change += 1
            else:
                self.counts_change = 1

            self.ticks_change = game.ticks
        else:
            self.counts_change = 0

    def need_change(self) -> bool:
        return self.counts_change == 3

    def set_zone_event(self, menu: Menu, game: Game, device: Device) -> None:
        layout = None

        if menu.layout.is_in(device):
            layout = menu.layout
        else:
            layout = game.layout

        self.zone = layout.find_zone(device)

    def get_zone_demo(self, game: Game) -> int:
        result = Layout.NONE

        if self.can_hit_demo(game.logger):
            monster_best = None
            n_friends = game.monsters.get_n_friends()

            for rank in range(0, game.monsters.ranks, 1):
                monster = game.monsters.get(rank)

                if (
                    self.can_fall_demo(monster, n_friends) and
                    (
                        monster_best is None or
                        monster_best.get_speed() > monster.get_speed()
                    )
                ):
                    monster_best = monster
                    result = monster.zone
                else:
                    pass
        else:
            pass

        return result

    def can_hit_demo(self, logger: Logger) -> bool:
        return (
            (logger.is_wait() and self.is_between_demo(logger)) or
            (logger.is_fall() and not self.is_between_demo(logger))
        )

    def is_between_demo(self, character: Character) -> bool:
        return (
            not self.is_begin_demo(character) and
            not self.is_finish_demo(character)
        )

    def is_begin_demo(self, character: Character) -> bool:
        return character.timer.get_ratio() < 1 / 3

    def is_finish_demo(self, character: Character) -> bool:
        return character.timer.get_ratio() >= 2 / 3

    def can_fall_demo(self, monster: Monster, n_friends: int) -> bool:
        return (
            (monster.is_enemy() or n_friends == 2) and
            (
                (monster.is_come() and self.is_finish_demo(monster)) or
                (monster.is_wait() and self.is_between_demo(monster)) or
                (monster.is_leave() and self.is_begin_demo(monster))
            )
        )
