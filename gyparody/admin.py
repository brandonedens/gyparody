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


###############################################################################
## Classes
###############################################################################

class PlayerScoreBox(clutter.Box):
    """
    """

    def __init__(self):
        super(PlayerScoreBox, self).__init__(clutter.BoxLayout())

        self.set_color(config.background_color)
        layout = self.get_layout_manager()
        layout.set_vertical(True)

        self.players = game.get_players()

        self.scores = []
        for player in self.players:
            text = clutter.Text(config.admin_font, 'Player %s score:' % player.name)
            text.set_color('white')
            self.add(text)

            score = clutter.Text(config.admin_font, "%d" % player.score)
            score.set_color('white')
            score.player = player
            self.scores.append(score)
            score.set_activatable(True)
            score.set_reactive(True)
            score.set_editable(True)
            score.connect('activate',
                lambda actor: self.set_score(actor))
            self.add(score)
            layout.set_fill(score, True, False)

    def set_score(self, score):
        try:
            s = int(score.get_text())
        except ValueError:
            return
        score.player.score = s
        self.update()

    def update(self):
        """
        """
        pass
        #for score in self.scores:
        #    score.set_text("%d" % score.player.score)

class FinalJeopardyBox(clutter.Box):

    def __init__(self):
        super(FinalJeopardyBox, self).__init__(clutter.BoxLayout())

        self.set_color(config.background_color)
        layout = self.get_layout_manager()
        layout.set_vertical(True)

        text = clutter.Text(config.admin_font_header, "FINAL JEOPARDY")
        self.add(text)

        self.players = game.get_players()
        for player in self.players:
            text = clutter.Text(config.admin_font, 'Player %s ($%d) wager:' % (player.name,
                                                                               player.score))
            text.set_color('white')
            self.add(text)

            wager = clutter.Text(config.admin_font, "0")
            wager.set_color('white')
            wager.player = player
            wager.value = 0
            wager.set_activatable(True)
            wager.set_reactive(True)
            wager.set_editable(True)
            wager.connect('activate',
                lambda actor: self.set_wager(actor))
            self.add(wager)
            layout.set_fill(wager, True, False)

            correct = clutter.Text(config.admin_font, "CORRECT")
            correct.set_color('green')
            correct.player = player
            correct.wager = wager
            correct.set_reactive(True)
            correct.connect('button-release-event',
                            lambda actor, event: self.correct(actor))
            self.add(correct)
            layout.set_fill(correct, True, False)

            wrong = clutter.Text(config.admin_font, "WRONG")
            wrong.set_color('red')
            wrong.player = player
            wrong.wager = wager
            wrong.set_reactive(True)
            wrong.connect('button-release-event',
                          lambda actor, event: self.wrong(actor))
            self.add(wrong)
            layout.set_fill(wrong, True, False)

    def set_wager(self, wager):
        try:
            w = int(wager.get_text())
        except ValueError:
            return
        wager.value = w

    def correct(self, actor):
        """
        """
        wager = actor.wager
        logging.info("Final jeopardy player %s ($%d) correct. Wager value = %d" % (wager.player.name,
                                                                                   wager.player.score,
                                                                                   wager.value))
        wager.player.score += wager.value
        logging.info("Player %s score now %d" % (wager.player.name, wager.player.score))

    def wrong(self, actor):
        """
        """
        wager = actor.wager
        logging.info("Final jeopardy player %s ($%d) wrong. Wager value = %d" % (wager.player.name,
                                                                                 wager.player.score,
                                                                                 wager.value))

        wager.player.score -= wager.value
        logging.info("Player %s score now %d" % (wager.player.name, wager.player.score))

    def update(self):
        """
        Do nothing on update.
        """
        pass

class IdleBox(clutter.Box):
    """
    """

    def __init__(self):
        super(IdleBox, self).__init__(clutter.FlowLayout(clutter.FLOW_VERTICAL))

        self.player_score_box = PlayerScoreBox()
        self.add(self.player_score_box)

        #self.game_board = GameBoard()
        #self.game_board.set_scale(0.6, 0.6)
        #self.add(self.game_board)

    def set_size(self, width, height):
        super(IdleBox, self).set_size(width, height)
        #self.game_board.set_size(width, height)
        #self.game_board.set_scale(0.6, 0.6)

    def update(self):
        self.player_score_box.update()

class ClueBox(clutter.Box):
    """
    Box for holding host clue information.
    """

    def __init__(self):
        super(ClueBox, self).__init__(clutter.FlowLayout(clutter.FLOW_VERTICAL))
        layout = self.get_layout_manager()
        layout.set_column_spacing(10)
        layout.set_row_spacing(10)
        self.set_color(config.background_color)

        # Add clue answer and question.
        clue_box = clutter.Box(clutter.BoxLayout())
        self.add(clue_box)
        clue_layout = clue_box.get_layout_manager()
        clue_layout.set_vertical(True)

        clue = game.get_selected_clue()
        text = clutter.Text(config.admin_font_header, "CLUE")
        text.set_color('white')
        clue_layout.pack(text, False, False, False,
                         clutter.BOX_ALIGNMENT_START,
                         clutter.BOX_ALIGNMENT_CENTER)
        text = clutter.Text(config.admin_font, "Answer\n%s" % clue.answer)
        text.set_color('green')
        clue_layout.pack(text, False, False, False,
                         clutter.BOX_ALIGNMENT_START,
                         clutter.BOX_ALIGNMENT_CENTER)
        text = clutter.Text(config.admin_font, "Question\n%s" % clue.question)
        text.set_color('red')
        clue_layout.pack(text, False, False, False,
                         clutter.BOX_ALIGNMENT_START,
                         clutter.BOX_ALIGNMENT_CENTER)

        # Add player buzz in information.
        buzz_box = clutter.Box(clutter.BoxLayout())
        self.add(buzz_box)
        buzz_layout = buzz_box.get_layout_manager()
        buzz_layout.set_vertical(True)
        text = clutter.Text(config.admin_font_header, 'PLAYER BUZZES')
        buzz_layout.pack(text, False, False, False,
                         clutter.BOX_ALIGNMENT_START,
                         clutter.BOX_ALIGNMENT_CENTER)
        self.players = []
        for player in game.get_players():
            text = clutter.Text(config.admin_font, "Player %s" % player.name)
            text.set_color('white')
            text.player = player
            self.players.append(text)
            buzz_layout.pack(text, False, False, False,
                             clutter.BOX_ALIGNMENT_START,
                             clutter.BOX_ALIGNMENT_CENTER)

        if game.selected_clue.is_daily_double():
            dd_box = clutter.Box(clutter.BoxLayout())
            self.add(dd_box)
            dd_layout = dd_box.get_layout_manager()
            dd_layout.set_vertical(True)
            for player in game.get_players():
                text = clutter.Text(config.admin_font, "Player %s" % player.name)
                text.set_color('white')
                text.player = player
                text.set_reactive(True)
                text.connect('button-release-event',
                             lambda actor, event: self.choose_team(actor))
                dd_box.add(text)
            text = clutter.Text(config.admin_font, 'Daily Double Wager:')
            text.set_color('white')
            dd_box.add(text)
            self.wager = clutter.Text(config.admin_font, '0')
            self.wager.set_color('white')
            self.wager.set_reactive(True)
            self.wager.set_editable(True)
            self.wager.connect('text-changed',
                lambda actor: game.set_daily_double_wager(self.get_wager()))
            dd_box.add(self.wager)
            dd_layout.set_fill(self.wager, True, False)

    def choose_team(self, text):
        """
        """
        player = text.player
        logging.debug("Chose daily double player %s" % player.name)
        game.set_buzzed_player(game.get_player_index(player))

    def get_wager(self):
        try:
            return int(self.wager.get_text())
        except ValueError:
            return 0

    def update(self):

        for player in self.players:
            if player.player == game.get_buzzed_player():
                player.set_color('red')
            else:
                player.set_color('white')

class Admin(clutter.Stage):
    """
    """

    ADMIN_DISPLAY_CLUE = 'ADMIN_DISPLAY_CLUE'
    ADMIN_IDLE = 'ADMIN_IDLE'
    ADMIN_INIT = 'ADMIN_INIT'
    ADMIN_FINAL_ROUND = 'FINAL_ROUND'

    def __init__(self):
        super(Admin, self).__init__()

        self.set_fullscreen(False)
        self.set_size(config.admin_screen_width, config.admin_screen_height)
        self.set_user_resizable(True)
        self.set_color('black')

        self.state = self.ADMIN_INIT

        # Connect the callback listeners
        self.connect('key-press-event', self.on_press)
        self.connect('allocation-changed', self.on_allocation_changed)

        self.show()

    def on_allocation_changed(self, stage, box, flags):
        """
        """
        for child in self.get_children():
            child.set_size(stage.get_width(), stage.get_height())

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()

    def on_tick(self):
        """
        """
        for child in self.get_children():
            child.update()

        new_state = self.state
        if game.state == game.IDLE:
            new_state = self.ADMIN_IDLE
        elif game.state == game.DISPLAY_CLUE or game.state == game.DAILY_DOUBLE_AWAIT_WAGER:
            new_state = self.ADMIN_DISPLAY_CLUE
        elif game.state == game.FINAL_ROUND:
            new_state = self.ADMIN_FINAL_ROUND

        if self.state != new_state:
            if new_state == self.ADMIN_IDLE:
                self.remove_all()
                idle_box = IdleBox()
                idle_box.set_size(self.get_width(), self.get_height())
                self.add(idle_box)
            elif new_state == self.ADMIN_DISPLAY_CLUE:
                self.remove_all()
                clue_box = ClueBox()
                clue_box.set_size(self.get_width(), self.get_height())
                self.add(clue_box)
            elif new_state == self.ADMIN_FINAL_ROUND:
                self.remove_all()
                final_round = FinalJeopardyBox()
                final_round.set_size(self.get_width(), self.get_height())
                self.add(final_round)

            self.state = new_state

