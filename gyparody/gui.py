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

from game import game
from game_board import GameBoard
from game_stage import GameStage


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################

class GUI(clutter.Stage):
    """
    """

    def __init__(self):
        super(GUI, self).__init__()

        # Setup the game stage.
        self.game_stage = GameStage()

        # Setup the admin screen.
        self.connect('destroy', clutter.main_quit)
        self.connect('key-press-event', self.on_press)
        self.set_color(clutter.Color(0, 0, 0))

        self.admin_game_board = GameBoard()
        self.admin_game_board.set_size(800, 600)
        #self.admin_game_board.set_scale(0.5, 0.5)
        #self.admin_game_board.set_click_handler(foo)
        self.add(self.admin_game_board)

        self.show()

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()
        if event.keyval == clutter.keysyms.f:
            # Set game stage fullscreen or not.
            self.game_stage.set_fullscreen(not self.game_stage.get_fullscreen())
        if event.keyval == clutter.keysyms.s:
            logging.debug('scaling')
            self.admin_game_board.set_scale(0.5, 0.5)

