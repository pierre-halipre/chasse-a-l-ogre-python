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

import abc


class State(abc.ABC):
    NONE = 0

    def __init__(self) -> None:
        self.state = State.NONE

    def set_state(self, state: int) -> None:
        self.state = state

    def is_state(self, state: int) -> bool:
        return self.state == state

    def set_none(self) -> None:
        self.set_state(State.NONE)

    def is_none(self) -> bool:
        return self.is_state(State.NONE)
