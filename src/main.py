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

from tool import Config
from device import Device
from font import Font
from pen import Pen
from frame import Frame
from menu import Menu
from game import Game
from action import Action


Config.switch_on()
W_SCREEN = Config.get_w_screen()
H_SCREEN = Config.get_h_screen()
FRAME_RATE = Config.get_frame_rate()

device = Device(W_SCREEN, H_SCREEN, FRAME_RATE)
frame = Frame(device)
menu = Menu(device)
game = Game(device)
pen = Pen(device)
font = Font(device)
action = Action()

while device.clock.thread.run:
    refresh_time = device.clock.get_refresh_time()

    if device.clock.thread.is_tick(refresh_time):
        if device.event.is_clic():
            if device.event.kind == 1:
                action.set_quit()
            elif device.event.kind == 2:
                if frame.canvas.is_in(device):
                    action.set_zone_event(menu, game, device)
                else:
                    pass

                action.check_change_design(game, device)
            else:
                pass
        else:
            pass

        if menu.party.is_none():
            menu.reset()
        else:
            pass

        menu.update(action.zone, device)

        if menu.party.is_quit():
            action.set_quit()
        elif (
            menu.need_reset or
            (game.logger.is_end() and menu.party.is_home())
        ):
            game.reset()
            menu.need_reset = False
        elif game.logger.is_end():
            menu.party.set_end()
        else:
            pass

        if (
            (menu.party.is_home() or menu.party.is_play()) and
            not menu.need_resume
        ):
            zone = None

            if menu.party.is_home():
                zone = action.get_zone_demo(game)
            else:
                zone = action.zone

            game.update(zone, device)
        else:
            menu.need_resume = False

        if not action.need_quit:
            action.reset()

            if action.need_change():
                device.design.change()
                device.graphic.change_window(device.design)
                device.music.change_volume(device.design)
                action.counts_change = 0
            else:
                pass

            frame.show_background(device)
            game.show(pen, device)
            menu.show(pen, device)

            if not menu.party.is_play():
                game.show_greyed_out(device)

                if menu.party.is_home():
                    font.set_home(device)
                elif menu.party.is_pause():
                    font.set_pause(game.ticks, device)
                else:
                    font.set_end(game.tally.score, device)

                font.show(frame.canvas, device)
            else:
                pass

            frame.show_foreground(device)

            device.graphic.show()

            if menu.party.is_home():
                game.audios.unset_play_audio()
            else:
                pass

            game.play(device)
            menu.play(device)
        else:
            device.clock.thread.run = False
    else:
        pass

Config.switch_off()
