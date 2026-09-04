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

from tool import Math, Path, Image, Window
from design import Design
from sizes import Sizes
from rasters import GraphicCaption, GraphicFrame, GraphicMenu, GraphicGame


class Graphic:
    def __init__(self, w_screen: int, h_screen: int) -> None:
        self.sizes = Sizes(w_screen, h_screen)

        w_window = 8 * self.sizes.w_case + 2 * self.sizes.h_case
        h_window = 22 * self.sizes.h_case
        self.window = Window(w_window, h_window)
        self.show_loading()

        self.caption = GraphicCaption()

        x_border = self.get_x_screen()
        y_border = self.get_y_screen()
        self.frame = GraphicFrame(x_border, y_border)

        x_panel = x_border + self.sizes.w_case
        y_panel = y_border + self.sizes.h_case
        self.menu = GraphicMenu(x_panel, y_panel)

        x_board = x_panel
        y_board = y_panel + 4 * self.sizes.h_case
        self.game = GraphicGame(x_board, y_board)

    def fill(self) -> None:
        w = 8 * self.sizes.w_case
        h = 16 * self.sizes.h_case
        self.game.greyed_out.set_size(w, h)
        self.game.greyed_out.set_greyed_out()

    def show_loading(self) -> None:
        image_icon = self.get_image_icon_loading()
        self.window.set_caption("Chasse à l'ogre", image_icon)

        x = 0
        w_window = self.window.get_w()
        h_window = self.window.get_h()
        y_top = Math.half(h_window - w_window)
        n_images = Math.ceil(y_top / w_window)

        image_background = self.get_image_loading("loading_background")
        image_background.scale(w_window, w_window)
        image_foreground = self.get_image_loading("loading_foreground")
        image_foreground.scale(w_window, w_window)

        for i in range(-n_images, n_images + 1, 1):
            y = y_top + i * w_window
            image_background.on_window(x, y, self.window)

            if i == 0:
                image_foreground.on_window(x, y, self.window)
            else:
                pass

        image_copyright = self.get_image_loading("loading_copyright")
        ratio = image_copyright.get_h() / image_copyright.get_w()
        h_image_copyright = Math.floor(w_window * ratio)
        image_copyright.scale(w_window, h_image_copyright)
        y = h_window - 1 - h_image_copyright
        image_copyright.on_window(x, y, self.window)

        self.show()

    def get_image_icon_loading(self) -> Image:
        image_icon = Image()
        path_base = Path.base()
        path_icon = Path.join(path_base, "icon")
        path = Path.format(path_icon, "ico")
        image_icon.load(path)

        return image_icon

    def get_image_loading(self, name: str) -> Image:
        image = Image()
        path_base = Path.base()
        path_loading = Path.join(path_base, "loading")
        path_file = Path.join(path_loading, name)
        path = Path.image(path_file)
        image.load(path)

        return image

    def add_caption(self, name: str, design: Design) -> None:
        image = Image()
        path_mode = design.get_path_mode_current()
        path_file = Path.join(path_mode, "icon")
        path = Path.image(path_file)
        image.load(path)

        self.caption.add(name, image)

    def change_window(self, design: Design) -> None:
        mode = design.mode
        name = self.caption.names.get(mode)
        image = self.caption.images.get(mode)
        self.window.set_caption(name, image)

    def get_x_screen(self) -> int:
        w_window = self.window.get_w()

        return Math.half(w_window - 10 * self.sizes.w_case)

    def get_y_screen(self) -> int:
        h_window = self.window.get_h()

        return Math.half(h_window - 22 * self.sizes.h_case)

    def show(self) -> None:
        self.window.draw()
