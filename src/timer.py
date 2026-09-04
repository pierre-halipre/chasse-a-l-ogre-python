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


class Timer:
    def __init__(self) -> None:
        self.counts = 0
        self.threshold = 0

    def start(self, milliseconds: int, device: Device) -> None:
        self.counts = 0
        self.threshold = device.clock.to_ticks(milliseconds)

    def stop(self) -> None:
        self.counts = 0
        self.threshold = 0

    def is_on(self) -> bool:
        return self.counts < self.threshold

    def update(self) -> None:
        self.counts = self.counts + 1

    def get_ratio(self) -> float:
        return self.counts / self.threshold

    def get_ratio_inverse(self) -> float:
        return (self.threshold - 1 - self.counts) / self.threshold

    def is_blink(self, device: Device) -> bool:
        ratio = self.get_ratio()
        n_animations_min = device.clock.get_n_animations_min()
        n_blinks = Math.ceil(self.threshold * 2 / n_animations_min)

        return Math.floor(ratio * n_blinks) % 2 == 1
