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
import dataclasses
from tool import Path
from tool import Array
from tool import Sound
from tool import Channel
from design import Design


class Music:
    def __init__(self) -> None:
        self.channels = Array()

        self.menu = MusicMenu()
        self.game = MusicGame()

        self.volume_max = 1 / 2

    def fill(self, design: Design) -> None:
        mode = design.get_mode_current()
        self.channels.add(Channel(mode))

    def change_volume(self, design: Design) -> None:
        for mode in range(0, self.channels.get_size(), 1):
            channel = self.channels.get(mode)
            volume = None

            if mode == design.mode:
                volume = self.volume_max
            else:
                volume = 0

            channel.set_volume(volume)


class Songs(Array):
    def fill(self, name: str, volume: float, design: Design) -> None:
        path_mode = design.get_path_mode_current()
        path_sounds = Path.join(path_mode, "sounds")
        path_file = Path.join(path_sounds, name)
        path = Path.sound(path_file)
        sound = Sound(path, volume)
        self.add(sound)

    def play(self, music: Music) -> None:
        for mode in range(0, self.get_size(), 1):
            channel = music.channels.get(mode)
            channel.stop()
            sound = self.get(mode)
            is_loop = self.is_loop()
            channel.play(sound, is_loop)

    @abc.abstractmethod
    def is_loop(self) -> bool:
        pass


class SongsBase(Songs):
    def is_loop(self) -> bool:
        return False


class SongsLoop(Songs):
    def is_loop(self) -> bool:
        return True


@dataclasses.dataclass
class MusicMenu:
    theme: SongsLoop
    buttons_pause: SongsBase
    buttons_resume: SongsBase

    def __init__(self):
        self.theme = SongsLoop()
        self.buttons_pause = SongsBase()
        self.buttons_resume = SongsBase()


@dataclasses.dataclass
class MusicGame:
    logger_come = SongsBase
    logger_leave = SongsBase
    friend_fall = SongsBase
    enemy_fall = SongsBase
    friend_come = SongsBase
    enemy_come = SongsBase

    def __init__(self):
        self.logger_come = SongsBase()
        self.logger_leave = SongsBase()
        self.friend_fall = SongsBase()
        self.enemy_fall = SongsBase()
        self.friend_come = SongsBase()
        self.enemy_come = Songs()
