# Brandon Edens
# 2010-03-21
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
Module defines the main game logic.
"""

###############################################################################
## Imports
###############################################################################

import clutter
import logging
import yaml

from config import config
from game_stage import GameStage


###############################################################################
## Classes
###############################################################################

class Player(object):
    def __init__(self, name):
        """
        Create a player with the given name.
        """
        self.name = name

        self.score = 0

class Game(clutter.Stage):

    def __init__(self):
        """
        """
        super(Game, self).__init__()

        logging.info('Initializing game.')

        self.mode = "round1"
        self.players = []

        # Setup the game stage.
        self.game_stage = GameStage(self.load_round())

        # Setup the admin screen.
        self.connect('destroy', clutter.main_quit)
        self.connect('key-press-event', self.on_press)
        self.set_color(clutter.Color(0, 0, 0))
        self.show()

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()
        if event.keyval == clutter.keysyms.f:
            # Set game stage fullscreen or not.
            self.game_stage.set_fullscreen(not self.game_stage.get_fullscreen())

    def add_player(self, name):
        self.players.append(Player(name))

    def load_round(self):
        """
        """
        round1_file = open(config.round_1_data, 'r')
        round1 = yaml.load(round1_file)
        round1_file.close()
        return round1


###############################################################################
## Functions
###############################################################################




