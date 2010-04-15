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

from config import config
from game_board import GameBoard

###############################################################################
## Constants
###############################################################################

MAIN_STAGE_BACKGROUND_COLOR = clutter.Color(2, 2, 2)


###############################################################################
## Classes
###############################################################################

class GameStage(clutter.Stage):

    def __init__(self, model):
        super(GameStage, self).__init__()

        self.model = model

        logging.info('Initializing game stage.')

        # Hide the mouse cursor on this stage.
        self.hide_cursor()

        # Set the stage background to grey.
        self.set_color(MAIN_STAGE_BACKGROUND_COLOR)

        # Connect callback listeners
        logging.info('Setting up game stage signals.')
        self.connect('fullscreen', self.on_fullscreen)
        self.connect('unfullscreen', self.on_unfullscreen)

        self.game_board = GameBoard(self.model)

        self.add(self.game_board)

        # Set a default stage size.
        self.set_fullscreen(False)
        self.set_size(800, 600)
        self.set_user_resizable(True)

        self.show()

    def set_size(self, width, height):
        """
        """
        try:
            super(GameStage, self).set_size(width, height)
            self.game_board.set_size(width, height)
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

