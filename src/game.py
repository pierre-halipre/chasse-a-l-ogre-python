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
from sprite import Sprite
from device import Device
from board import Board
from audios import AudiosGame
from gui import Gui
from logger import Logger
from monster import Monster
from monsters import Monsters
from tally import Tally


class Game(Gui):
    def __init__(self, device: Device) -> None:
        super().__init__(Board(device), AudiosGame(device))

        self.logger = Logger(6, self.layout, device)
        self.monsters = Monsters(self.layout, device)

        self.fence = Sprite(device.graphic.game.fence)
        self.layout.fill_sprite(self.fence, 1, device)

        self.cherry = Sprite(device.graphic.game.cherry)
        self.layout.fill_sprite(self.cherry, 1, device)

        self.greyed_out = device.graphic.game.greyed_out

        self.tally = Tally()

        self.ticks = 0

    def reset(self) -> None:
        self.layout.timer.stop()

        self.logger.set_none()
        self.monsters.reset()

        self.tally.accuracy = 0
        self.tally.counts = 0
        self.tally.score = 0
        self.tally.progress = 0

        self.ticks = 0

    def update(self, zone: int, device: Device) -> None:
        if not self.is_cutscene():
            self.update_monsters(zone, device)
        else:
            pass

        self.logger.time_base = self.tally.get_time_base(device)

        if (
            not self.is_cutscene() and
            not (self.tally.is_end() and self.monsters.is_end()) and
            self.layout.is_in_zones(zone)
        ):
            self.update_logger_action(zone, device)
        else:
            self.update_logger(device)

        if not self.is_cutscene() and not self.tally.is_end():
            self.update_monsters_start(device)
        else:
            pass

        self.update_layout(device)

        self.ticks += 1

    def is_cutscene(self) -> bool:
        return (
            not self.logger.is_end() and
            (self.logger.is_come() or self.logger.is_leave())
        )

    def update_monsters(self, zone: int, device: Device) -> None:
        n_updates_tally = 0

        for rank in range(0, self.monsters.ranks, 1):
            monster = self.monsters.get(rank)

            if (
                not monster.is_end() and
                not monster.is_fall() and
                monster.zone == zone
            ):
                self.tally.update_score(monster)
                n_updates_tally += 1

                monster.set_fall(device)

                self.set_play_audio_monster(monster)
            elif not monster.is_end():
                monster.update(device)

                if monster.is_out():
                    self.tally.update_score(monster)
                    n_updates_tally += 1
                else:
                    pass
            else:
                pass

        self.tally.update_progress(n_updates_tally)

    def set_play_audio_monster(self, monster: Monster) -> None:
        audio = None

        if monster.is_enemy():
            if monster.is_come():
                audio = self.audios.enemy_come
            else:
                audio = self.audios.enemy_fall
        elif monster.is_come():
            audio = self.audios.friend_come
        else:
            audio = self.audios.friend_fall

        audio.set_play()

    def update_logger_action(self, zone: int, device: Device) -> None:
        self.logger.zone = zone
        is_hit = False

        for rank in range(0, self.monsters.ranks, 1):
            monster = self.monsters.get(rank)

            if monster.is_fall() and monster.zone == self.logger.zone:
                if monster.is_enemy():
                    self.logger.set_hit_good()
                else:
                    self.logger.set_hit_bad()

                self.logger.timer.counts = monster.timer.counts
                self.logger.timer.threshold = monster.timer.threshold
                is_hit = True
            else:
                pass

        if (
            not self.logger.is_wait() and
            not self.logger.is_fall() and
            not is_hit
        ):
            self.logger.set_wait(device)
        else:
            pass

    def update_logger(self, device: Device) -> None:
        if self.logger.is_none():
            self.logger.set_come(device)

            self.audios.logger_come.set_play()
        elif not self.logger.is_out():
            self.logger.update(device)

            if (
                self.tally.is_end() and
                self.monsters.is_end() and
                not self.logger.is_out() and
                not self.logger.is_leave()
            ):
                self.logger.set_leave(device)

                self.audios.logger_leave.set_play()
            elif self.logger.is_wait():
                for rank in range(0, self.monsters.ranks, 1):
                    monster = self.monsters.get(rank)

                    if monster.is_wait() and monster.is_enemy():
                        self.logger.set_fall(device)
                    else:
                        pass
            else:
                pass
        else:
            pass

        if self.is_cutscene():
            ratio = self.logger.get_ratio_position()
            size_zones = self.layout.zones.get_size()
            i = Math.floor(ratio * size_zones)
            self.logger.zone = self.layout.zones.get(i)
        else:
            pass

    def update_monsters_start(self, device: Device) -> None:
        level = self.tally.get_level()

        for rank in range(0, self.monsters.get_rank_max(level) + 1, 1):
            monster = self.monsters.get(rank)

            if (
                (monster is None or monster.is_end()) and
                self.monsters.can_start_next(level, device)
            ):
                zone = self.monsters.get_zone_next(self.layout)
                time_base = self.tally.get_time_base(device)
                monster = self.monsters.get_next(level)
                monster.start(zone, time_base, device)
                self.monsters.set(rank, monster)

                self.set_play_audio_monster(monster)

                if rank >= self.monsters.ranks:
                    self.monsters.ranks += 1
                else:
                    pass
            else:
                pass

    def update_layout(self, device: Device) -> None:
        if self.layout.timer.is_on():
            self.layout.timer.update()
        else:
            pass

        if not self.layout.timer.is_on():
            time_base = self.tally.get_time_base(device)
            self.layout.timer.start(time_base, device)
        else:
            pass

    def show_elements(self, device: Device) -> None:
        if not self.logger.is_end():
            self.monsters.show(True, self.layout, device)
            self.show_fence(True, device)
            self.logger.show(self.layout, device)
            self.show_fence(False, device)
            self.monsters.show(False, self.layout, device)
            self.show_cherry(device)
        else:
            pass

    def show_fence(self, northern_zone: bool, device: Device) -> None:
        i_zone_logger = self.layout.to_i_zone(self.logger.zone)

        is_cutscene = self.is_cutscene()
        is_blink = self.layout.timer.is_blink(device)

        for i in range(0, self.layout.zones.get_size(), 1):
            zone = self.layout.zones.get(i)

            is_build = self.layout.to_i_zone(zone) < i_zone_logger
            is_construct = is_build or (not is_blink and i == i_zone_logger)
            is_attack = not is_blink or not self.monsters.is_attack(zone)

            if (
                self.layout.can_draw_zone(zone, northern_zone) and
                (
                    (not is_cutscene and is_attack) or
                    (is_cutscene and is_construct)
                )
            ):
                self.draw_fence(zone, device)
            else:
                pass

    def draw_fence(self, zone: int, device: Device) -> None:
        i_sheet = self.layout.to_i_zone(zone)
        level = self.tally.get_level()
        ratio = (level - 1) / 3
        image = self.fence.get_image(i_sheet, ratio, device)

        x = self.layout.get_x_limit_zone(zone, False, device)
        y = self.layout.get_y_limit_zone(zone, False, device)

        self.fence.draw(image, x, y, device)

    def show_cherry(self, device: Device) -> None:
        for rank in range(0, self.monsters.ranks, 1):
            monster = self.monsters.get(rank)

            if monster.is_fall():
                ratio = monster.timer.get_ratio()
                zone = monster.zone
                zone_inverse = self.layout.get_zone_inverse(zone)
                i_sheet = self.layout.to_i_zone(zone_inverse)
                image = self.cherry.get_image(i_sheet, ratio, device)

                x = monster.get_x_cherry(self.layout, device)
                y = monster.get_y_cherry(self.layout, device)

                self.layout.draw_image(image, x, y, device)
            else:
                pass

    def show_greyed_out(self, device: Device) -> None:
        x = self.layout.x
        y = self.layout.y
        self.greyed_out.on_window(x, y, device.graphic.window)
