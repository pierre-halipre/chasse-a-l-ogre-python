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

from tool import Event
from clock import Clock
from design import Design
from text import Text
from graphic import Graphic
from music import Music


class Device:
    def __init__(self, w_screen: int, h_screen: int, frame_rate: int) -> None:
        self.design = Design()

        self.graphic = Graphic(w_screen, h_screen)
        self.text = Text()
        self.music = Music()

        self.event = Event()
        self.clock = Clock(frame_rate)

        self.graphic.fill()

        self.add_mode_0()
        self.add_mode_1()
        self.add_mode_2()
        self.add_mode_3()

        self.graphic.change_window(self.design)
        self.music.change_volume(self.design)

    def add_mode_0(self) -> None:
        self.design.folders.add("mode_0")

        self.text.fill("screen_play", self.design)

        self.graphic.add_caption("Chasse à l'ogre", self.design)

        self.graphic.frame.font.fill("printer", 41, self.design)
        self.graphic.frame.pen.fill("form", 6, self.design)
        self.graphic.frame.border.fill("frame", 1, self.design)

        self.graphic.menu.panel.fill("scroll", 1, self.design)
        self.graphic.menu.buttons.fill("items", 1, self.design)

        game = self.graphic.game
        game.board.fill("kingdom", 4, self.design)
        game.characters.logger.fill("archer", 4, self.design)
        game.characters.zombie.fill("orc_blue", 4, self.design)
        game.characters.vampire.fill("ogre_red", 4, self.design)
        game.characters.skeleton.fill("orc_red", 4, self.design)
        game.characters.ghost.fill("ogre_blue", 4, self.design)
        game.characters.deer.fill("mage_blue", 4, self.design)
        game.characters.rabbit.fill("mage_red", 4, self.design)
        game.cherry.fill("magic", 4, self.design)
        game.fence.fill("palisade", 3, self.design)

        self.music.fill(self.design)

        menu = self.music.menu
        menu.theme.fill("kingdom_theme", 1, self.design)
        menu.buttons_pause.fill("item_pause", 0.5, self.design)
        menu.buttons_resume.fill("item_resume", 0.5, self.design)

        self.music.game.logger_come.fill("archer_come", 0.5, self.design)
        self.music.game.logger_leave.fill("archer_leave", 0.5, self.design)
        self.music.game.friend_fall.fill("mage_fall", 0.25, self.design)
        self.music.game.enemy_fall.fill("orc_fall", 0.25, self.design)
        self.music.game.friend_come.fill("mage_come", 0.25, self.design)
        self.music.game.enemy_come.fill("orc_come", 0.25, self.design)

    def add_mode_1(self) -> None:
        self.design.folders.add("mode_1")

        self.text.fill("book", self.design)

        self.graphic.add_caption("Ulysse le magicien", self.design)

        self.graphic.frame.font.fill("press", 41, self.design)
        self.graphic.frame.pen.fill("cast", 6, self.design)
        self.graphic.frame.border.fill("mount", 1, self.design)

        self.graphic.menu.panel.fill("parchment", 1, self.design)
        self.graphic.menu.buttons.fill("knobs", 1, self.design)

        game = self.graphic.game
        game.board.fill("laboratory", 1, self.design)
        game.characters.logger.fill("wizard", 3, self.design)
        game.characters.zombie.fill("goblin_hair", 3, self.design)
        game.characters.vampire.fill("goblin_horn", 3, self.design)
        game.characters.skeleton.fill("goblin_helmet", 3, self.design)
        game.characters.ghost.fill("goblin_hood", 3, self.design)
        game.characters.deer.fill("child", 3, self.design)
        game.characters.rabbit.fill("old_man", 3, self.design)
        game.cherry.fill("spell", 5, self.design)
        game.fence.fill("barricade", 3, self.design)

        self.music.fill(self.design)

        menu = self.music.menu
        menu.theme.fill("laboratory_theme", 0.75, self.design)
        menu.buttons_pause.fill("knob_pause", 0.75, self.design)
        menu.buttons_resume.fill("knob_resume", 0.75, self.design)

        self.music.game.logger_come.fill("wizard_come", 0.75, self.design)
        self.music.game.logger_leave.fill("wizard_leave", 0.75, self.design)
        self.music.game.friend_fall.fill("child_fall", 0.5, self.design)
        self.music.game.enemy_fall.fill("goblin_fall", 0.5, self.design)
        self.music.game.friend_come.fill("child_come", 0.5, self.design)
        self.music.game.enemy_come.fill("goblin_come", 0.5, self.design)

    def add_mode_2(self) -> None:
        self.design.folders.add("mode_2")

        self.text.fill("scratch", self.design)

        self.graphic.add_caption("Marnie la sorcière", self.design)

        self.graphic.frame.font.fill("typography", 41, self.design)
        self.graphic.frame.pen.fill("pencil", 6, self.design)
        self.graphic.frame.border.fill("edge", 1, self.design)

        self.graphic.menu.panel.fill("shell", 1, self.design)
        self.graphic.menu.buttons.fill("toggles", 1, self.design)

        game = self.graphic.game
        game.board.fill("village", 1, self.design)
        game.characters.logger.fill("witch", 4, self.design)
        game.characters.zombie.fill("cockroach", 4, self.design)
        game.characters.vampire.fill("spirit", 4, self.design)
        game.characters.skeleton.fill("hermit_crab", 4, self.design)
        game.characters.ghost.fill("robot", 4, self.design)
        game.characters.deer.fill("owl", 4, self.design)
        game.characters.rabbit.fill("balloon", 4, self.design)
        game.cherry.fill("bobble", 2, self.design)
        game.fence.fill("hedge", 3, self.design)

        self.music.fill(self.design)

        menu = self.music.menu
        menu.theme.fill("village_theme", 0.75, self.design)
        menu.buttons_pause.fill("toggle_pause", 1, self.design)
        menu.buttons_resume.fill("toggle_resume", 1, self.design)

        self.music.game.logger_come.fill("witch_come", 0.5, self.design)
        self.music.game.logger_leave.fill("witch_leave", 0.5, self.design)
        self.music.game.friend_fall.fill("owl_fall", 0.5, self.design)
        self.music.game.enemy_fall.fill("cockroach_fall", 0.5, self.design)
        self.music.game.friend_come.fill("owl_come", 0.5, self.design)
        self.music.game.enemy_come.fill("cockroach_come", 0.5, self.design)

    def add_mode_3(self) -> None:
        self.design.folders.add("mode_3")

        self.text.fill("scripts", self.design)

        self.graphic.add_caption("Tonton le bûcheron", self.design)

        self.graphic.frame.font.fill("font", 41, self.design)
        self.graphic.frame.pen.fill("pen", 6, self.design)
        self.graphic.frame.border.fill("border", 1, self.design)

        self.graphic.menu.panel.fill("panel", 1, self.design)
        self.graphic.menu.buttons.fill("buttons", 1, self.design)

        game = self.graphic.game
        game.board.fill("board", 3, self.design)
        game.characters.logger.fill("logger", 3, self.design)
        game.characters.zombie.fill("zombie", 3, self.design)
        game.characters.vampire.fill("vampire", 3, self.design)
        game.characters.skeleton.fill("skeleton", 3, self.design)
        game.characters.ghost.fill("ghost", 3, self.design)
        game.characters.deer.fill("deer", 3, self.design)
        game.characters.rabbit.fill("Rabbit", 3, self.design)
        game.cherry.fill("cherry", 3, self.design)
        game.fence.fill("fence", 3, self.design)

        self.music.fill(self.design)

        menu = self.music.menu
        menu.theme.fill("theme", 1, self.design)
        menu.buttons_pause.fill("buttons_pause", 1, self.design)
        menu.buttons_resume.fill("buttons_resume", 1, self.design)

        self.music.game.logger_come.fill("logger_come", 1, self.design)
        self.music.game.logger_leave.fill("logger_leave", 1, self.design)
        self.music.game.friend_fall.fill("friend_fall", 1, self.design)
        self.music.game.enemy_fall.fill("enemy_fall", 1, self.design)
        self.music.game.friend_come.fill("friend_come", 1, self.design)
        self.music.game.enemy_come.fill("enemy_come", 1, self.design)
