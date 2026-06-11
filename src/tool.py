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

import os
import sys
import math
import random
import typing
import dataclasses
import pygame


class Math:
    @staticmethod
    def abs(x: float) -> float:
        return abs(x)

    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)

    @staticmethod
    def ceil(x: float) -> int:
        return math.ceil(x)

    @staticmethod
    def round(x: float) -> int:
        result = None

        x_rest = Math.abs(x) % 1

        if (x >= 0 and x_rest < 1 / 2) or (x < 0 and x_rest >= 1 / 2):
            result = Math.floor(x)
        else:
            result = Math.ceil(x)

        return result

    @staticmethod
    def sqrt(x: int) -> float:
        return math.sqrt(x)

    @staticmethod
    def pow(x: float, e: int) -> float:
        return pow(x, e)

    @staticmethod
    def rand(m: int) -> int:
        return random.randrange(m)

    @staticmethod
    def unicode(x: str) -> int:
        return ord(x)

    @staticmethod
    def half(x: int) -> int:
        return Math.floor(x / 2)

    @staticmethod
    def max(x_1: int, x_2: int) -> int:
        result = None

        if x_1 > x_2:
            result = x_1
        else:
            result = x_2

        return result

    @staticmethod
    def min(x_1: int, x_2: int) -> int:
        result = None

        if x_1 < x_2:
            result = x_1
        else:
            result = x_2

        return result

    @staticmethod
    def distance(start: int, end: int, ratio: float) -> int:
        return start + Math.floor((end - start) * ratio)

    @staticmethod
    def is_flag(x: int, flag: int) -> bool:
        return x & flag == flag

    @staticmethod
    def has_flag(x: int, flag: int) -> bool:
        return x & flag != 0


class Path:
    @staticmethod
    def join(path_1: str, path_2: str) -> str:
        return os.path.join(path_1, path_2)

    @staticmethod
    def format(file: str, extension: str) -> str:
        return file + "." + extension

    @staticmethod
    def base() -> str:
        folder = None

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            folder = getattr(sys, "_MEIPASS")
        else:
            folder = ".."

        return Path.join(folder, "res")

    @staticmethod
    def image(path) -> str:
        return Path.format(path, "png")

    @staticmethod
    def sound(path) -> str:
        return Path.format(path, "mp3")

    @staticmethod
    def text(path) -> str:
        return Path.format(path, "txt")


class Array:
    def __init__(self) -> None:
        self.elements = []

    def get_size(self) -> int:
        return len(self.elements)

    def set(self, i: int, value: type) -> None:
        self.elements[i] = value

    def get(self, i: int) -> type:
        return self.elements[i]

    def add(self, value: type) -> None:
        self.elements.append(value)

    def clear(self) -> None:
        self.elements.clear()


class Config:
    @staticmethod
    def switch_on() -> None:
        pygame.init()

    @staticmethod
    def switch_off() -> None:
        pygame.quit()

    @staticmethod
    def get_w_screen() -> int:
        size = pygame.display.get_desktop_sizes()

        return size[0][0]

    @staticmethod
    def get_h_screen() -> int:
        size = pygame.display.get_desktop_sizes()

        return size[0][1]

    @staticmethod
    def get_frame_rate() -> int:
        return 60


@dataclasses.dataclass
class Thread:
    run: bool
    time: int

    def __init__(self) -> None:
        self.run = True
        self.time = 0

    def is_tick(self, refresh_rate: int) -> bool:
        result = False

        time = pygame.time.get_ticks()

        if time - self.time >= refresh_rate:
            result = True

            self.time = time
        else:
            pass

        return result


@dataclasses.dataclass
class Event:
    kind: int
    x: int
    y: int

    def __init__(self) -> None:
        self.kind = 0
        self.x = 0
        self.y = 0

    def is_clic(self) -> bool:
        self.kind = 0
        self.x = 0
        self.y = 0

        events = pygame.event.get()

        for i in range(0, len(events), 1):
            event = events[i]

            if event.type == pygame.QUIT:
                self.kind = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.kind = 2
                self.x = event.pos[0]
                self.y = event.pos[1]
            else:
                pass

        return self.kind != 0


@dataclasses.dataclass
class File:
    datas: Array
    cursor: int

    def __init__(self, path: str) -> None:
        self.datas = Array()
        self.cursor = 0

        with open(path, "r", -1, "us-ascii") as file:
            data = None

            while data != "":
                data = file.read(1)

                if data != "\n":
                    self.datas.add(data)
                else:
                    pass

            file.close()

    def read(self) -> str:
        data = self.datas.get(self.cursor)
        self.cursor += 1

        return data


@dataclasses.dataclass
class Area:
    rectangle: pygame.Rect

    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.rectangle = pygame.Rect(x, y, w, h)


@dataclasses.dataclass
class Image:
    drawable: pygame.Surface

    def __init__(self) -> None:
        self.drawable = None

    def load(self, path: str) -> None:
        self.drawable = pygame.image.load(path)

    def set_size(self, w: int, h: int) -> None:
        self.drawable = pygame.Surface((w, h), pygame.SRCALPHA)

    def get_w(self) -> int:
        return self.drawable.get_width()

    def get_h(self) -> int:
        return self.drawable.get_height()

    def scale(self, w: int, h: int) -> None:
        self.drawable = pygame.transform.scale(self.drawable, (w, h))

    def flip(self, flip_w: bool) -> None:
        self.drawable = pygame.transform.flip(self.drawable, flip_w, False)

    def set_greyed_out(self) -> None:
        color = pygame.Color(0, 0, 0, 51)
        self.drawable.fill(color)

    def on_window(self, x: int, y: int, image: typing.Self) -> None:
        image.drawable.blit(self.drawable, (x, y))

    def get_area(self, x: int, y: int, w: int, h: int) -> Area:
        return Area(x, y, w, h)

    def on_image(self, x: int, y: int, image: typing.Self, area: Area) -> None:
        self.drawable.blit(image.drawable, (x, y), area.rectangle)


@dataclasses.dataclass
class Window(Image):
    def __init__(self, w: int, h: int) -> None:
        super().__init__()

        self.drawable = pygame.display.set_mode((w, h))

    def draw(self) -> None:
        pygame.display.flip()
        self.drawable.fill(0)

    def set_caption(self, name: str, image: Image) -> None:
        pygame.display.set_caption(name)
        pygame.display.set_icon(image.drawable)


@dataclasses.dataclass
class Sound:
    listenable: pygame.mixer.Sound

    def __init__(self, path: str, volume: float) -> None:
        self.listenable = pygame.mixer.Sound(path)
        self.listenable.set_volume(volume)


@dataclasses.dataclass
class Channel:
    playable: pygame.mixer.Channel

    def __init__(self, n: int) -> None:
        self.playable = pygame.mixer.Channel(n)

    def play(self, sound: Sound, is_loop: bool) -> None:
        loop_value = None

        if is_loop:
            loop_value = -1
        else:
            loop_value = 0

        self.playable.play(sound.listenable, loop_value)

    def stop(self) -> None:
        self.playable.stop()

    def set_volume(self, volume: float) -> None:
        self.playable.set_volume(volume)
