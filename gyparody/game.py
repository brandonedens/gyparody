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

import time
import clutter
import logging
import yaml

from config import config
from game_buttons import game_buttons


###############################################################################
## Globals
###############################################################################

is_round_2 = [False]

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

    def __init__(self, answer, question, value, state='unanswered', dailydouble=False):
        """
        """
        # Answer state is one of:
        # unanswered, answered, selected, question
        self.state = state
        self.value = value
        self.answer = answer
        self.question = question
        self.dailydouble = dailydouble

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

    def get_type(self):
        """
        Getting the clue type.
        """
        if type(self.answer) != dict:
            return 'text'

        try:
            self.answer['image']
            return 'image'
        except KeyError:
            pass
        try:
            self.answer['video']
            return 'video'
        except KeyError:
            pass
        try:
            self.answer['audio']
            return 'audio'
        except KeyError:
            pass

    def is_daily_double(self):
        return self.dailydouble

    def marshall(self):
        """
        """
        data = {}
        data['state'] = self.state
        data['value'] = self.value
        data['answer'] = self.answer
        data['question'] = self.question
        data['dailydouble'] = self.dailydouble
        return data

class Category(object):

    def __init__(self, name, category_data):
        """
        """
        self.clues = []
        self.name = name
        for i in xrange(len(category_data)):
            clue_data = category_data[i]
            dd = clue_data.has_key('dailydouble')
            if not is_round_2[0]: # round 1
                clue = Clue(clue_data['answer'],
                            clue_data['question'],
                            (200 * (i + 1)),
                            dailydouble=dd)
            else: # round 2
                clue = Clue(clue_data['answer'],
                                clue_data['question'],
                                (400 * (i + 1)),
                                dailydouble=dd)
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

class FinalRound(object):
    """
    """

    def __init__(self, final_round_data):
        """
        """
        self.category = final_round_data.keys()[0]
        self.answer = final_round_data[self.category]['answer']
        self.question = final_round_data[self.category]['question']

class Game(object):
    IDLE = 'IDLE'
    DISPLAY_CLUE = 'DISPLAY_CLUE'
    DISPLAY_QUESTION = 'DISPLAY_QUESTION'
    FINAL_ROUND = 'FINAL_ROUND'
    FINAL_ROUND_WAGER = 'FINAL_ROUND_WAGER'
    FINAL_ROUND_CLUE = 'FINAL_ROUND_CLUE'
    FINAL_ROUND_QUESTION = 'FINAL_ROUND_QUESTION'
    AWAIT_BUZZ = 'AWAIT_BUZZ'
    AWAIT_ANSWER = 'AWAIT_ANSWER'
    DAILY_DOUBLE_AWAIT_WAGER = 'DAILY_DOUBLE_AWAIT_WAGER'

    def __init__(self):
        """
        """
        super(Game, self).__init__()

        self.players = [
            Player(config.player_a_name),
            Player(config.player_b_name),
            Player(config.player_c_name),
        ]

        self.load_round('round1')

        self.state = self.IDLE
        self.timeout_start = None
        self.timeout_beep = False
        self.final_round = None
        self.flash_player_name = False
        self.flash_player_score = False
        self.flash_daily_double = False
        self.clear_daily_double = False
        self.update_game_board = False
        self.wager = 0

        self.load_final_round()

    def load_round(self, round_name):
        self.current_round = round_name
        if self.current_round == 'round1':
            filename = config.round_1_data
            is_round_2[0] = False
        elif self.current_round == 'round2':
            filename = config.round_2_data
            is_round_2[0] = True
        else:
            logging.error('unknown round')
        round_file = open(filename, 'r')
        round_data = yaml.load(round_file)
        round_file.close()

        self.categories = []
        for category_data in round_data:
            name = category_data.keys()[0]
            data = category_data[name]
            self.categories.append(
                Category(name, data))

    def load_final_round(self):
        """
        Load the final round data into the game.
        """
        filename = config.final_round
        fh = open(filename, 'r')
        final_round_data = yaml.load(fh)
        fh.close()
        self.final_round = FinalRound(final_round_data)


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

    def get_players(self):
        """
        Return the player objects.
        """
        return self.players

    def on_tick(self):
        """
        Game tick.
        """
        if self.state == self.AWAIT_BUZZ:
            # Check the buzz timeout if there is one set.
            if self.timeout_start != None:
                if time.time() - self.timeout_start > config.await_buzz_timeout:
                    self.timeout_beep = True
                    # Disable all lit players.
                    game_buttons.reset_player_lights()
                    self.state = self.DISPLAY_QUESTION
        elif self.state == self.AWAIT_ANSWER:
            # Check the answer timeout if there is one set.
            if self.timeout_start != None:
                if time.time() - self.timeout_start > config.await_answer_timeout:
                    # Just beep and let host select correct / incorrect
                    self.timeout_beep = True
                    self.timeout_start = None
        # Update the player lights
        game_buttons.send_players()

    def buzz(self, player_index):
        """
        Player buzzer pressed. player_index is 0, 1, or 2
        """
        if self.state == self.DISPLAY_CLUE:
            # Player buzzed in too early, store the earliest time their buzzer can be used
            self.buzzer_lockouts[player_index] = time.time() + config.buzzer_lockout_time
            logging.debug("Locking out player %d" % player_index)
            return

        if self.state != self.AWAIT_BUZZ:
            logging.error("Cannot buzz in, not in AWAIT_BUZZ")
            return

        if player_index in self.buzzed_players:
            logging.error("Cannot buzz in, player already buzzed in")
            return

        if self.buzzer_lockouts.has_key(player_index) and self.buzzer_lockouts[player_index] > time.time():
            logging.debug("Cannot buzz in, locked out for buzzing early")
            return

        logging.debug("Going to AWAIT_ANSWER state")
        # Note this is the current player answering the question
        self.buzzed_player = player_index
        # Light that player's buzzer.
        game_buttons.player_set(player_index, True)
        # Note this player buzzed in so they can't buzz in again
        self.buzzed_players.append(player_index)
        # Update the current timeout start to reflect the number of seconds a
        # player has to resond with a question to the given answer.
        self.timeout_start = time.time()
        # Record the time of the buzz-in for timeout
        self.flash_player_name = True
        self.state = self.AWAIT_ANSWER

    def correct_answer(self):
        """
        Correct answer given by player.
        """
        if self.state != self.AWAIT_ANSWER:
            logging.error("Cannot answer, not in AWAIT_ANSWER")
            return

        if self.selected_clue.is_daily_double():
            self.players[self.buzzed_player].score += self.wager
        else:
            self.players[self.buzzed_player].score += self.selected_clue.value
        self.dump_scores()

        # Disable all lit players.
        game_buttons.reset_player_lights()

        logging.debug("Correct answer, Going to DISPLAY_QUESTION state")
        self.state = self.DISPLAY_QUESTION
        self.flash_player_score = True

    def incorrect_answer(self):
        """
        Incorrect answer given by player.
        """
        if self.state != self.AWAIT_ANSWER:
            logging.error("Cannot answer, not in AWAIT_ANSWER")
            return

        if self.selected_clue.is_daily_double():
            self.players[self.buzzed_player].score -= self.wager
        else:
            self.players[self.buzzed_player].score -= self.selected_clue.value
        self.dump_scores()

        # Disable all lit players.
        game_buttons.reset_player_lights()

        logging.debug("Incorrect answer, Going to AWAIT_BUZZ state")
        self.state = self.AWAIT_BUZZ
        # Resetting timeout to number of seconds players get to buzz in.
        self.timeout_start = time.time()
        self.buzzer_lockouts = {}
        self.flash_player_score = True

    def select_clue(self, clue):
        """
        Host selected a clue.
        """
        if self.state != self.IDLE:
            logging.error("Cannot select clue when not in IDLE state")
            return

        # Clear the list of players that have buzzed in.
        self.buzzed_players = []

        self.selected_clue = clue
        self.buzzer_lockouts = {}
        if self.selected_clue.is_daily_double():
            logging.debug("Going to DAILY_DOUBLE_AWAIT_WAGER state")
            self.flash_daily_double = True
            self.state = self.DAILY_DOUBLE_AWAIT_WAGER
        else:
            logging.debug("Going to DISPLAY_CLUE state")
            self.state = self.DISPLAY_CLUE

    def bar(self):
        """
        Multi-purpose bar (space bar).
        """
        if self.state == self.DISPLAY_CLUE:
            # In DISPLAY_CLUE state, unlock the buzzers.
            logging.debug("Unlocking buzzers, going to AWAIT_BUZZ state")
            self.state = self.AWAIT_BUZZ
            self.timeout_start = time.time()
        elif self.state == self.AWAIT_ANSWER:
            # In AWAIT_ANSWER state, inhibit the answer timeout beep
            logging.debug("Inhibiting answer timeout beep")
            self.timeout_start = None
        elif self.state == self.DISPLAY_QUESTION:
            # Same as cancel, return from question to game board
            logging.debug("Going to IDLE state")
            self.state = self.IDLE
            self.handle_round_completion()
        elif self.state == self.DAILY_DOUBLE_AWAIT_WAGER:
            logging.debug("Going to DISPLAY_CLUE, clear daily double")
            self.state = self.DISPLAY_CLUE
            self.clear_daily_double = True
        elif self.state == self.FINAL_ROUND:
            logging.debug('Going to FINAL_ROUND_WAGER, clear final round')
            self.state = self.FINAL_ROUND_WAGER
        elif self.state == self.FINAL_ROUND_WAGER:
            logging.debug('Going to FINAL_ROUND_CLUE, clear final round category')
            self.state = self.FINAL_ROUND_CLUE
        elif self.state == self.FINAL_ROUND_CLUE:
            logging.debug('Going to FINAL_ROUND_QUESTION, clear final round clue')
            self.state = self.FINAL_ROUND_QUESTION

    def cancel(self):
        if self.state == self.DISPLAY_QUESTION:
            # cancel from display question screen returns to game board
            logging.debug("Cancel, going to IDLE state")
            self.state = self.IDLE
            self.handle_round_completion()
        elif self.state == self.DISPLAY_CLUE:
            # cancel from display clue goes to display question
            logging.debug("Cancel, going to DISPLAY_QUESTION state")
            self.state = self.DISPLAY_QUESTION
        elif self.state == self.AWAIT_BUZZ:
            # cancel from await buzz goes to display question
            logging.debug("Cancel, going to DISPLAY_QUESTION state")
            self.state = self.DISPLAY_QUESTION
        else:
            logging.error("Cannot cancel from this state")

    def check_timeout_beep(self):
        flag = self.timeout_beep
        self.timeout_beep = False
        return flag

    def check_flash_player_name(self):
        flag = self.flash_player_name
        self.flash_player_name = False
        return flag

    def check_flash_player_score(self):
        flag = self.flash_player_score
        self.flash_player_score = False
        return flag

    def check_flash_daily_double(self):
        flag = self.flash_daily_double
        self.flash_daily_double = False
        return flag

    def check_clear_daily_double(self):
        flag = self.clear_daily_double
        self.clear_daily_double = False
        return flag

    def check_update_game_board(self):
        flag = self.update_game_board
        self.update_game_board = False
        return flag

    def handle_round_completion(self):
        completed = True
        for category in self.categories:
            for clue in category.clues:
                if clue.state == 'unanswered':
                    completed = False
        if completed:
            logging.debug('The round is completed.')
            if self.current_round == 'round1':
                logging.debug('Advance from round 1 to round 2')
                self.load_round('round2')
                self.update_game_board = True
            elif self.current_round == 'round2':
                logging.debug('Advance from round 2 to final round')
                self.state = self.FINAL_ROUND
            else:
                logging.error('Round over, what to do now?')

    def adjust_score(self, player, offset):
        self.players[player].score += offset
        self.dump_scores()

    def set_score(self, player, score):
        self.players[player].score = score
        self.dump_scores()

    def set_daily_double_wager(self, wager):
        self.wager = wager

    def dump_scores(self):
        s = ''
        for player in self.players:
            s += '%s: %d, ' % (player.name, player.score)
        logging.info(s)


###############################################################################
## Statements
###############################################################################

game = Game()

