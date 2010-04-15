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
from game_board import GameBoard
from game_stage import GameStage
from model import Model


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

        self.model = Model()
        self.model.round = self.load_round()

        # Setup the game stage.
        self.game_stage = GameStage(self.model)

        # Setup the admin screen.
        self.connect('destroy', clutter.main_quit)
        self.connect('key-press-event', self.on_press)
        self.set_color(clutter.Color(0, 0, 0))

        # Draw administrative controls
        # Setup player name input box
        self.player_setup = clutter.Box(clutter.BoxLayout())
        self.add(self.player_setup)
        layout = self.player_setup.get_layout_manager()
        layout.set_vertical(True)
        player_label = clutter.Text('', 'player1: ')
        player_label.set_color(clutter.Color(250, 250, 250))
        self.player_setup.add(player_label)
        player1_name = clutter.Text('', 'John Doe')
        player1_name.set_color(clutter.Color(250, 250, 250))
        player1_name.set_editable(True)
        self.player_setup.add(player1_name)
        player_label = clutter.Text('', 'player2: ')
        player_label.set_color(clutter.Color(250, 250, 250))
        self.player_setup.add(player_label)
        player_label = clutter.Text('', 'player3: ')
        player_label.set_color(clutter.Color(250, 250, 250))
        self.player_setup.add(player_label)

        self.admin_game_board = GameBoard(self.model)
        self.admin_game_board.set_size(800, 600)
        self.admin_game_board.set_scale(0.5, 0.5)
        self.player_setup.add(self.admin_game_board)
        def foo(x):
            print x.get_answer_numbers()
            self.model.select_answer(x.get_answer_numbers())
        self.admin_game_board.set_click_handler(foo)

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




