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

from tool import Math, Thread


class Clock:
    def __init__(self, frame_rate: int) -> None:
        self.thread = Thread()
        self.frame_rate = frame_rate
        self.time_animation_min = 250
        self.time_animation_max = 750
        self.time_max = 3600000

    def get_refresh_time(self) -> int:
        return Math.ceil(1000 / self.frame_rate)

    def to_ticks(self, milliseconds: int) -> int:
        return Math.ceil(milliseconds / self.get_refresh_time())

    def get_n_animations_min(self) -> int:
        return self.to_ticks(self.time_animation_min)

    def get_ticks_max(self) -> int:
        return self.to_ticks(self.time_max)
