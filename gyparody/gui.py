# Brandon Edens
# 2010-04-16
# Copyright (C) 2010 Brandon Edens <brandon@as220.org>
#
# This file is part of gyparody.
#
# gyparody is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gyparody is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gyparody. If not, see <http://www.gnu.org/licenses/>.
"""
"""

###############################################################################
## Imports
###############################################################################

import clutter
import logging

from config import config
from game import game
from game_board import GameBoard
from game_board import ClueSquare
from text import Text


###############################################################################
## Constants
###############################################################################

MAIN_STAGE_BACKGROUND_COLOR = clutter.Color(2, 2, 2)


###############################################################################
## Classes
###############################################################################

class CategoryOverlay(clutter.Box):
    """
    An overlay that displays category information.
    """

    def __init__(self):
        """
        """
        super(CategoryOverlay, self).__init__(clutter.BoxLayout())
        layout = self.get_layout_manager()
        layout.set_vertical(False)
        self.set_color(config.background_color)

        self.boxes = []
        for category_name in game.get_category_names():
            box = clutter.Box(clutter.BinLayout(
                clutter.BIN_ALIGNMENT_CENTER,
                clutter.BIN_ALIGNMENT_CENTER))
            rect = clutter.Rectangle()
            rect.set_color(config.square_background_color)
            box.add(rect)
            text = Text(config.category_overlay_font, category_name)
            box.add(text)
            self.add(box)

    def set_size(self, width, height):
        """
        Set the size of the category overlay which should be large enough for
        all of the 5 categories. However, the width specified here will be the
        screen size width.
        """
        super(CategoryOverlay, self).set_size(width * 5, height)
        for child in self.get_children():
            child.set_size(width, height)

    def set_text(self, text):
        """
        """
        self.box.remove(self.text)
        self.text = Text(config.category_overlay_font, text)
        self.box.add(self.text)

class ClueOverlay(clutter.Box):
    """
    An overlay for clue information.
    """

    def __init__(self):
        """
        """
        super(ClueOverlay, self).__init__(clutter.BinLayout(
            clutter.BIN_ALIGNMENT_CENTER,
            clutter.BIN_ALIGNMENT_CENTER))
        self.set_size(1, 1)
        self.set_color(config.square_background_color)
        self.text = Text('', '')

    def set_text(self, text):
        """
        """
        self.remove(self.text)
        self.text = Text(config.clue_overlay_font, text)
        self.add(self.text)

clue_overlay = ClueOverlay()

class PlayerBuzzOverlay(clutter.Box):
    """
    An overlay for player buzz in information.
    """

    def __init__(self):
        """
        """
        super(PlayerBuzzOverlay, self).__init__(clutter.BinLayout(
            clutter.BIN_ALIGNMENT_CENTER,
            clutter.BIN_ALIGNMENT_CENTER))
        self.set_color(config.square_background_color)
        self.text = Text('', '')

    def set_text(self, text):
        """
        """
        self.remove(self.text)
        self.text = Text(config.player_overlay_font, text)
        self.add(self.text)


class GUI(clutter.Stage):
    """
    """

    def __init__(self):
        super(GUI, self).__init__()

        logging.info('Initializing game gui.')

        # Set the stage background to grey.
        self.set_color(MAIN_STAGE_BACKGROUND_COLOR)

        # Connect callback listeners
        logging.info('Setting up game stage signals.')
        self.connect('destroy', clutter.main_quit)
        self.connect('key-press-event', self.on_press)
        self.connect('fullscreen', self.on_fullscreen)
        self.connect('unfullscreen', self.on_unfullscreen)
        self.connect('button-release-event', self.on_click)

        self.game_board = GameBoard()
        self.add(self.game_board)

        # Overly box for displaying clue information and answers
        self.clue_overlay = clue_overlay
        self.add(self.clue_overlay)

        # Overlay box for display category information.
        self.category_overlay = CategoryOverlay()
        self.category_overlay.set_size(self.get_width(),
                                       self.get_height())

        # Overlay box for displaying which player buzzed in.
        self.player_buzz_overlay = PlayerBuzzOverlay()
        self.player_buzz_overlay.set_size(self.get_width(),
                                          self.get_height())
        self.player_buzz_overlay.set_opacity(0)
        self.add(self.player_buzz_overlay)

        # Set a default stage size.
        self.set_fullscreen(False)
        self.set_size(800, 600)
        self.set_user_resizable(True)

        self.show()

    def on_click(self, actor, event):
        """
        """
        if type(event.source) == ClueSquare:
            clue_square = event.source
            self.clue_overlay.set_text(clue_square.clue.answer)
            self.clue_overlay.animate(clutter.LINEAR,
                                      500,
                                      'width', self.get_width(),
                                      'height', self.get_height())

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()
        elif event.keyval == clutter.keysyms.a:
            # player A rings in.
            self.player_buzz_overlay.set_opacity(255)
            self.player_buzz_overlay.set_text('Brandon')
            self.player_buzz_overlay.animate(clutter.EASE_IN_CUBIC,
                                             1000,
                                             'opacity', 0)
        elif event.keyval == clutter.keysyms.b:
            # player B rings in.
            self.player_buzz_overlay.set_opacity(255)
            self.player_buzz_overlay.set_text('Paolo')
            self.player_buzz_overlay.animate(clutter.EASE_IN_CUBIC,
                                             1000,
                                             'opacity', 0)
        elif event.keyval == clutter.keysyms.c:
            # player C rings in.
            pass
        elif event.keyval == clutter.keysyms.l:
            if self.category_overlay in self.get_children():
                self.category_overlay.animate(clutter.LINEAR,
                                              500,
                                              'x', self.category_overlay.get_x() - self.get_width())
            else:
                self.category_overlay.set_size(self.get_width(),
                                               self.get_height())
                self.category_overlay.set_x(self.get_width())
                self.add(self.category_overlay)
                self.category_overlay.animate(clutter.LINEAR,
                                              500,
                                              'x', self.category_overlay.get_x() - self.get_width())
        elif event.keyval == clutter.keysyms.f:
            # Fullscreen play area.
            self.set_fullscreen(not self.get_fullscreen())
        elif event.keyval == clutter.keysyms.t:
            self.clue_overlay.animate(clutter.LINEAR,
                                      500,
                                      'width', self.get_width(),
                                      'height', self.get_height())

    def set_size(self, width, height):
        """
        """
        try:
            super(GUI, self).set_size(width, height)
            self.game_board.set_size(width, height)
            self.category_overlay.set_size(width, height)
            self.player_buzz_overlay.set_size(width, height)
        except AttributeError:
            # If there is an attribute error then its most likely because
            # self.game_board did not exist because the stage is first
            # loading. Therefore we simply pass on this exception as during
            # loading correctly size of internals will be set.
            pass

    def on_fullscreen(self, stage):
        """
        Signal for when main game stage is fullscreened. This signal resizes
        all contained elements.
        """
        self.set_size(config.fullscreen_width, config.fullscreen_height)

    def on_unfullscreen(self, stage):
        """
        Signal for when main game stage is un-fullscreened. This signal resizes
        all contained elements.
        """
        self.set_size(config.screen_width, config.screen_height)

    def on_second(self):
        """
        Call back associated with each second.
        """
        game.on_second()

