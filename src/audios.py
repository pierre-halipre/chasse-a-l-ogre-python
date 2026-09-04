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

from abc import ABC, abstractmethod
from music import Songs
from device import Device


class Audios(ABC):
    @abstractmethod
    def __init__(self, device: Device) -> None:
        pass

    @abstractmethod
    def need_play(self) -> bool:
        pass

    @abstractmethod
    def get_songs(self) -> Songs:
        pass


class Audio:
    def __init__(self, songs: Songs) -> None:
        self.songs = songs
        self.need_play = False

    def unset_play(self) -> None:
        self.need_play = False

    def set_play(self) -> None:
        self.need_play = True


class AudiosMenu(Audios):
    def __init__(self, device: Device) -> None:
        self.theme = Audio(device.music.menu.theme)
        self.buttons_pause = Audio(device.music.menu.buttons_pause)
        self.buttons_resume = Audio(device.music.menu.buttons_resume)

    def need_play(self) -> bool:
        return (
            self.theme.need_play or
            self.buttons_pause.need_play or
            self.buttons_resume.need_play
        )

    def get_songs(self) -> Songs:
        audio = None

        if self.theme.need_play:
            audio = self.theme
        elif self.buttons_pause.need_play:
            audio = self.buttons_pause
        else:
            audio = self.buttons_resume

        self.theme.unset_play()
        self.buttons_pause.unset_play()
        self.buttons_resume.unset_play()

        return audio.songs


class AudiosGame(Audios):
    def __init__(self, device: Device) -> None:
        self.logger_come = Audio(device.music.game.logger_come)
        self.logger_leave = Audio(device.music.game.logger_leave)
        self.friend_fall = Audio(device.music.game.friend_fall)
        self.enemy_fall = Audio(device.music.game.enemy_fall)
        self.friend_come = Audio(device.music.game.friend_come)
        self.enemy_come = Audio(device.music.game.enemy_come)

    def need_play(self) -> bool:
        return (
            self.logger_come.need_play or
            self.logger_leave.need_play or
            self.friend_fall.need_play or
            self.enemy_fall.need_play or
            self.friend_come.need_play or
            self.enemy_come.need_play
        )

    def get_songs(self) -> Songs:
        audio = None

        if self.logger_come.need_play:
            audio = self.logger_come
        elif self.logger_leave.need_play:
            audio = self.logger_leave
        elif self.friend_fall.need_play:
            audio = self.friend_fall
        elif self.enemy_fall.need_play:
            audio = self.enemy_fall
        elif self.friend_come.need_play:
            audio = self.friend_come
        else:
            audio = self.enemy_come

        self.unset_play_audio()

        return audio.songs

    def unset_play_audio(self) -> None:
        self.logger_come.unset_play()
        self.logger_leave.unset_play()
        self.friend_fall.unset_play()
        self.enemy_fall.unset_play()
        self.friend_come.unset_play()
        self.enemy_come.unset_play()
