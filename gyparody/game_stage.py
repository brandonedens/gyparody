# Brandon Edens
# 2010-03-22
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

from category import Category
from config import config
from text import Text


###############################################################################
## Constants
###############################################################################

MAIN_STAGE_BACKGROUND_COLOR = clutter.Color(2, 2, 2)


###############################################################################
## Classes
###############################################################################

class GameStage(clutter.Stage):

    def __init__(self, round):
        super(GameStage, self).__init__()

        logging.info('Initializing game stage.')

        # Hide the mouse cursor on this stage.
        #self.hide_cursor()

        # Set a default stage size.
        self.set_fullscreen(False)
        self.set_size(800, 600)
        self.set_user_resizable(True)

        # Set the stage background to grey.
        self.set_color(MAIN_STAGE_BACKGROUND_COLOR)

        # Connect callback listeners
        logging.info('Setting up game stage signals.')
        self.connect('fullscreen', self.on_fullscreen)
        self.connect('unfullscreen', self.on_fullscreen)

        self.box = clutter.Box(clutter.BoxLayout())
        layout = self.box.get_layout_manager()
        layout.set_vertical(False)
        spacing = int(self.get_width() * 0.01)
        layout.set_spacing(spacing)

        for category in round:
            category = Category(category)
            self.box.add(category)
            category.set_size(self.get_width() / len(round) - spacing,
                              self.get_height())

        self.add(self.box)
        self.show()

    def set_size(self, width, height):
        """
        """
        try:
            super(GameStage, self).set_size(width, height)
            layout = self.box.get_layout_manager()
            spacing = int(self.get_width() * 0.01)
            layout.set_spacing(spacing)
            children = self.box.get_children()
            for child in children:
                child.set_size(self.get_width() / len(children) - spacing,
                               self.get_height())
        except AttributeError:
            # If there is an attribute error then its most likely because
            # self.box did not exist because the stage is first
            # loading. Therefore we simply pass on this exception as during
            # loading correctly size of internals will be set.
            pass

    def on_fullscreen(self, stage):
        """
        Signal for when main game stage is fullscreened. This signal resizes
        all contained elements.
        """
        self.set_size(self.get_width(), self.get_height())

