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

from tool import Path, Array


class Design:
    def __init__(self) -> None:
        self.mode = 0
        self.folders = Array()

    def get_mode_current(self) -> int:
        n_modes = self.folders.get_size()

        return n_modes - 1

    def get_path_mode_current(self) -> str:
        base_path = Path.base()
        mode = self.get_mode_current()
        folder = self.folders.get(mode)

        return Path.join(base_path, folder)

    def change(self) -> None:
        mode = self.get_mode_current()
        self.mode = (self.mode + 1) % (mode + 1)
