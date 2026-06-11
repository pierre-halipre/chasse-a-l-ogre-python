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
from device import Device
from monster import Monster


class Tally:
    def __init__(self) -> None:
        self.counts = 0
        self.accuracy = 0
        self.score = 0
        self.progress = 0
        self.progress_max = 6

    def update_score(self, monster: Monster) -> None:
        accuracy_monster = monster.get_accuracy_tally()
        sum_accuracy = self.accuracy * self.counts + accuracy_monster
        self.counts += 1
        self.accuracy = sum_accuracy / self.counts

        score_monster = monster.get_score_tally()
        self.score += Math.pow(score_monster, 2)

    def update_progress(self, n_updates: int) -> None:
        progress_update = 1 - self.accuracy
        self.progress += Math.pow(progress_update, 2) * n_updates

    def is_end(self) -> bool:
        return self.progress >= self.progress_max

    def get_level(self) -> int:
        result = None

        if self.progress < self.progress_max / 10:
            result = 1
        elif self.progress >= 6 * self.progress_max / 10:
            result = 3
        else:
            result = 2

        return result

    def get_time_base(self, device: Device) -> int:
        clock = device.clock
        time_range = clock.time_animation_max - clock.time_animation_min
        ratio = self.accuracy * self.progress / self.progress_max

        return Math.ceil(clock.time_animation_max - time_range * ratio)
