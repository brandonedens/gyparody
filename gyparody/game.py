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


###############################################################################
## Constants
###############################################################################

# Global variable that tracks if we're in round1, round2, or final jeopardy.
GAME_STATE = 'round1'


###############################################################################
## Classes
###############################################################################

class Player(object):

    def __init__(self, name, score=0):
        """
        Create a player with the given name.
        """
        self.name = name
        self.score = score

    def marshall(self):
        """
        """
        data = {}
        data['name'] = self.name
        data['score'] = self.score
        return data

class Clue(object):

    def __init__(self, answer, question, value, state='unanswered'):
        """
        """
        # Answer state is one of:
        # unanswered, answered, selected, question
        self.state = state
        self.value = value
        self.answer = answer
        self.question = question

    def __str__(self):
        """
        """
        if self.state == 'answered':
            return ""
        elif self.state == 'unanswered':
            return "$%d" % self.value
        elif self.state == 'selected':
            return self.answer
        elif self.state == 'question':
            return self.question

    def get_value(self):
        """
        Get the value of this clue.
        """
        return "$%d" % self.value

    def get_answer(self):
        """
        Getting the clue answer.
        """
        return self.answer

    def marshall(self):
        """
        """
        data = {}
        data['state'] = self.state
        data['value'] = self.value
        data['answer'] = self.answer
        data['question'] = self.question
        return data

class Category(object):

    def __init__(self, name, category_data):
        """
        """
        self.clues = []
        self.name = name
        for i in xrange(len(category_data)):
            clue_data = category_data[i]
            if GAME_STATE == 'round1':
                clue = Clue(clue_data['answer'],
                            clue_data['question'],
                            (200 * (i + 1)))
            elif GAME_STATE == 'round2':
                clue = Clue(clue_data['answer'],
                                clue_data['question'],
                                (400 * (i + 1)))
            self.clues.append(clue)

    def __str__(self):
        """
        """
        text = "%s\n" % self.name
        for clue in self.clues:
            text += "%s\n" % clue
        return text

    def get_name(self):
        return self.name

    def get_clues(self):
        return self.clues

    def marshall(self):
        """
        """
        data = {}
        clue_list = []
        for clue in self.clues:
            clue_list.append(clue.marshall())
        data[self.name] = clue_list
        return data

class Game(object):

    def __init__(self):
        """
        """
        super(Game, self).__init__()

        self.players = []

        round1_file = open(config.round_1_data, 'r')
        round_data = yaml.load(round1_file)
        round1_file.close()

        self.categories = []
        for category_data in round_data:
            name = category_data.keys()[0]
            data = category_data[name]
            self.categories.append(
                Category(name, data))

    def add_player(self, name):
        self.players.append(Player(name))

    def save(self):
        """
        Save the current state of the game to disk.
        """
        fh = open(config.save_filename, 'w')
        yaml.dump(self.marshall(), fh)
        fh.close()

    def marshall(self):
        """
        Convert game into basic python data for saving.
        """
        data = {}
        data['mode'] = self.mode
        player_data = []
        for player in self.players:
            player_data.append(player.marshall())
        data['players'] = player_data
        tmp = []
        for category in self.categories:
            tmp.append(category.mashall())
        data['round'] = tmp
        return data

    def unmarshall(self, data):
        """
        """
        GAME_MODE = data['mode']
        self.players = []
        for player_data in data['players']:
            self.players.append(Player(player_data['name'],
                                       player_data['score']))

        self.round = Round(data['round'])

    def load(self, filename):
        """
        Load the game from the given filename.
        """
        fh = open(filename, 'r')
        data = yaml.load(fh)
        fh.close()
        self.unmarshall(data)

    def get_categories(self):
        """
        Return the round's categories.
        """
        return self.categories

    def get_category_names(self):
        """
        Return a list of the category names.
        """
        names = []
        for category in self.categories:
            names.append(category.get_name())
        return names

    def on_second(self):
        """
        Game tick on asecond.
        """
        pass


###############################################################################
## Statements
###############################################################################

game = Game()

