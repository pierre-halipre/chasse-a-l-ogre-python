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

from monster import Monster


class Enemy(Monster):
    def is_enemy(self) -> bool:
        return True

    def get_accuracy_tally(self) -> float:
        step = None

        if self.is_come():
            step = 3
        elif self.is_wait():
            step = 2
        else:
            step = 1

        sign = 1
        ratio = self.timer.get_ratio()

        return (step - sign * ratio) / 3

    def get_score_tally(self) -> int:
        result = None

        if self.is_come():
            result = 3
        elif self.is_wait():
            result = 2
        elif self.is_leave():
            result = 1
        else:
            result = 0

        return result
