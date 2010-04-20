# Paolo DePetrillo
# 2010-04-13
# Copyright (C) 2010 Paolo DePetrillo <paolod@gmail.com>
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
import gobject
import logging

from config import config
from game import game
from text import Text

###############################################################################
## Classes
###############################################################################

class Square(clutter.Box):

    def __init__(self, font, text):
        super(Square, self).__init__(
            clutter.BinLayout(clutter.BIN_ALIGNMENT_CENTER,
                              clutter.BIN_ALIGNMENT_CENTER))
        super(Square, self).set_color(config.square_background_color)
        self.text = Text(font, text)
        self.add(self.text)

    def set_color(self, color):
        """
        Set the color of the square text.
        """
        self.text.set_color(color)

    def set_size(self, width, height):
        """
        """
        super(Square, self).set_size(width, height)
        self.text.set_size(width, height)
        layout = self.get_layout_manager()
        layout.set_alignment(self.text,
                             clutter.BIN_ALIGNMENT_CENTER,
                             clutter.BIN_ALIGNMENT_CENTER)

    def set_text(self, font, text):
        """
        """
        self.remove(self.text)
        self.text = Text(font, text)
        self.text.set_size(self.get_width(), self.get_height())
        scale_x, scale_y = self.get_scale()
        self.text.set_scale(scale_x, scale_y)
        self.add(self.text)

class ClueSquare(Square):

    def __init__(self, clue):
        self.clue = clue
        super(ClueSquare, self).__init__(config.clue_value_font, clue)
        self.set_color(config.clue_value_color)

        self.set_reactive(True)
        self.connect('button-release-event', self.on_click)
        self.connect('paint', self.on_paint)

    def on_paint(self, actor):
        if self.clue.state == 'unanswered':
            self.set_text(config.clue_value_font, self.clue.get_value())
            self.set_color(config.clue_value_color)
        elif self.clue.state == 'selected':
            self.set_text(config.clue_font, '')

    def on_click(self, actor, event):
        """
        """
        logging.debug("Clue square click! state = %s" % self.clue.state)
        if self.clue.state == 'unanswered':
            self.clue.state = 'selected'
            logging.debug("Clue answer = %s" % self.clue.get_answer())
            self.set_text('', '')

class CategoryColumn(clutter.Box):

    def __init__(self, category):
        super(CategoryColumn, self).__init__(clutter.BoxLayout())
        self.category = category

        layout = self.get_layout_manager()
        layout.set_vertical(True)
        spacing = int(self.get_width() * 0.01)
        layout.set_spacing(spacing)

        name_square = Square(config.category_font, category.get_name())
        self.add(name_square)

        for clue in category.get_clues():
            clue_square = ClueSquare(clue)
            self.add(clue_square)

    def set_size(self, width, height):
        """
        """
        super(CategoryColumn, self).set_size(width, height)
        spacing = int(height * 0.01)
        layout = self.get_layout_manager()
        layout.set_spacing(spacing)
        children = self.get_children()
        for child in children:
            child.set_size(width, (height / len(children)) - spacing)

class GameBoard(clutter.Box):
    def __init__(self):
        super(GameBoard, self).__init__(clutter.BoxLayout())

        layout = self.get_layout_manager()
        layout.set_vertical(False)
        spacing = int(self.get_width() * 0.01)
        layout.set_spacing(spacing)

        categories = game.get_categories()
        for category in categories:
            category_column = CategoryColumn(category)
            category_column.set_size(
                self.get_width() / len(categories) - spacing,
                self.get_height()
                )
            self.add(category_column)

    def set_size(self, width, height):
        """
        """
        try:
            super(GameBoard, self).set_size(width, height)
            layout = self.get_layout_manager()
            spacing = int(self.get_width() * 0.01)
            layout.set_spacing(spacing)
            children = self.get_children()
            for child in children:
                child.set_size(self.get_width() / len(children) - spacing,
                               self.get_height())
        except AttributeError:
            # If there is an attribute error then its most likely because
            # self.game_board did not exist because the stage is first
            # loading. Therefore we simply pass on this exception as during
            # loading correctly size of internals will be set.
            pass

