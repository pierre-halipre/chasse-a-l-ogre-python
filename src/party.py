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

from state import State


class Party(State):
    HOME = 1
    PLAY = 2
    PAUSE = 3
    END = 4
    QUIT = 5

    def set_home(self) -> None:
        self.set_state(Party.HOME)

    def is_home(self) -> bool:
        return self.is_state(Party.HOME)

    def set_play(self) -> None:
        self.set_state(Party.PLAY)

    def is_play(self) -> bool:
        return self.is_state(Party.PLAY)

    def set_pause(self) -> None:
        self.set_state(Party.PAUSE)

    def is_pause(self) -> bool:
        return self.is_state(Party.PAUSE)

    def set_end(self) -> None:
        self.set_state(Party.END)

    def is_end(self) -> bool:
        return self.is_state(Party.END)

    def set_quit(self) -> None:
        self.set_state(Party.QUIT)

    def is_quit(self) -> bool:
        return self.is_state(Party.QUIT)
