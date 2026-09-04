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

from abc import abstractmethod
from dataclasses import dataclass
from tool import Math
from tool import Path
from tool import Array
from tool import Image
from design import Design
from sizes import Sizes


class Rasters(Array):
    def __init__(self, n_w_cases: int, n_h_cases: int, n_sheets: int) -> None:
        super().__init__()

        self.n_w_cases = n_w_cases
        self.n_h_cases = n_h_cases
        self.n_sheets = n_sheets

    def get_w(self, sizes: Sizes) -> int:
        result = None

        w = sizes.to_w_cases(self.n_w_cases)

        if self.is_half():
            result = Math.half(w)
        else:
            result = w

        return result

    def get_h(self, sizes: Sizes) -> int:
        return sizes.to_h_cases(self.n_h_cases)

    def get_n_sprites(self, mode: int) -> int:
        result = None

        sprite_sheet = self.get(mode)

        if self.is_loop() and sprite_sheet.n_images > 1:
            result = (sprite_sheet.n_images - 1) * 2
        else:
            result = sprite_sheet.n_images

        return result

    def get_i_sprite(self, mode: int, i_image: int) -> int:
        result = None

        sprite_sheet = self.get(mode)

        if self.is_loop() and i_image >= sprite_sheet.n_images:
            result = self.get_n_sprites(mode) - i_image
        else:
            result = i_image

        return result

    def fill(self, name: str, n_images: int, design: Design) -> None:
        path_mode = design.get_path_mode_current()
        path_images = Path.join(path_mode, "images")
        path_file = Path.join(path_images, name)
        path = Path.image(path_file)
        sprite_sheet = SpriteSheet(path, n_images)
        self.add(sprite_sheet)

    def get_sprite(self, mode: int, i_sprite: int, j_sprite: int) -> Image:
        sprite_sheet = self.get(mode)
        w_sprite_sheet = sprite_sheet.get_w()
        h_sprite_sheet = sprite_sheet.get_h()
        w = Math.floor(w_sprite_sheet / sprite_sheet.n_images)
        h = Math.floor(h_sprite_sheet / self.n_sheets)

        result = Image()
        result.set_size(w, h)
        x = i_sprite * w
        y = j_sprite * h
        area = sprite_sheet.get_area(x, y, w, h)
        result.on_image(0, 0, sprite_sheet, area)

        return result

    def get_image(self, sprite: Image, flip_w: bool, sizes: Sizes) -> Image:
        sprite.flip(flip_w)
        self.scale_sprite(sprite, sizes)

        w = self.get_w(sizes)
        h = self.get_h(sizes)
        x = Math.half(w - sprite.get_w())
        y = Math.half(h - sprite.get_h())
        result = Image()
        result.set_size(w, h)
        area = sprite.get_area(0, 0, w, h)
        result.on_image(x, y, sprite, area)

        return result

    def scale_sprite(self, sprite: Image, sizes: Sizes) -> None:
        w_sprite = None
        h_sprite = None

        if self.is_zone():
            w_sprite = sizes.w_sprite
            h_sprite = sizes.h_sprite
        else:
            w_sprite = self.get_w(sizes)
            h_sprite = self.get_h(sizes)

        sprite.scale(w_sprite, h_sprite)

    @abstractmethod
    def is_half(self) -> bool:
        pass

    @abstractmethod
    def is_loop(self) -> bool:
        pass

    @abstractmethod
    def is_zone(self) -> bool:
        pass


class RastersCase(Rasters):
    def is_half(self) -> bool:
        return False

    def is_loop(self) -> bool:
        return False

    def is_zone(self) -> bool:
        return False


class RastersZone(Rasters):
    def __init__(self, n_sheets: int) -> None:
        super().__init__(2, 4, n_sheets)

    def is_half(self) -> bool:
        return False

    def is_loop(self) -> bool:
        return True

    def is_zone(self) -> bool:
        return True


class RastersCanvas(Rasters):
    def __init__(self, n_w_cases: int, n_h_cases: int, x: int, y: int) -> None:
        super().__init__(n_w_cases, n_h_cases, 2)

        self.x = x
        self.y = y

    def is_half(self) -> bool:
        return True

    def is_loop(self) -> bool:
        return True

    def is_zone(self) -> bool:
        return False


@dataclass
class SpriteSheet(Image):
    def __init__(self, path: str, n_images: int) -> None:
        super().__init__()

        self.load(path)
        self.n_images = n_images


@dataclass
class GraphicCaption:
    names: Array
    images: Array

    def __init__(self) -> None:
        self.names = Array()
        self.images = Array()

    def add(self, name: str, image: Image) -> None:
        self.names.add(name)
        self.images.add(image)


@dataclass
class GraphicFrame:
    font: RastersCase
    pen: RastersCase
    border: RastersCanvas

    def __init__(self, x: int, y: int) -> None:
        self.font = RastersCase(1, 2, 1)
        self.pen = RastersCase(1, 1, 1)
        self.border = RastersCanvas(10, 22, x, y)


@dataclass
class GraphicMenu:
    panel: RastersCanvas
    buttons: RastersZone

    def __init__(self, x: int, y: int) -> None:
        self.panel = RastersCanvas(8, 4, x, y)
        self.buttons = RastersZone(6)


@dataclass
class GraphicCharacters:
    logger: RastersZone
    zombie: RastersZone
    vampire: RastersZone
    skeleton: RastersZone
    ghost: RastersZone
    deer: RastersZone
    rabbit: RastersZone

    def __init__(self) -> None:
        self.logger = RastersZone(9)
        self.zombie = RastersZone(9)
        self.vampire = RastersZone(9)
        self.skeleton = RastersZone(9)
        self.ghost = RastersZone(9)
        self.deer = RastersZone(9)
        self.rabbit = RastersZone(9)


@dataclass
class GraphicGame:
    board: RastersCanvas
    characters: GraphicCharacters
    cherry: RastersZone
    fence: RastersCase
    greyed_out: Image

    def __init__(self, x: int, y: int) -> None:
        self.board = RastersCanvas(8, 16, x, y)
        self.characters = GraphicCharacters()
        self.cherry = RastersZone(3)
        self.fence = RastersCase(2, 4, 3)
        self.greyed_out = Image()
