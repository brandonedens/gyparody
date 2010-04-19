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

class PlayerScoreOverlay(clutter.Box):
    """
    An overlay for player score information.
    """

    def __init__(self):
        """
        """
        super(PlayerScoreOverlay, self).__init__(clutter.BinLayout(
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

    SHOW_GAME_BOARD = 'SHOW_GAME_BOARD'
    SHOW_CLUE = 'SHOW_CLUE'
    SHOW_QUESTION = 'SHOW_QUESTION'

    def __init__(self):
        super(GUI, self).__init__()

        logging.info('Initializing game gui.')

        self.gui_state = self.SHOW_GAME_BOARD

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

        # Overlay box for displaying clue information and answers
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

        # Overlay box for displaying player score.
        self.player_score_overlay = PlayerScoreOverlay()
        self.player_score_overlay.set_size(self.get_width(),
                                          self.get_height())
        self.player_score_overlay.set_opacity(0)
        self.add(self.player_score_overlay)

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
            logging.debug('Notify game clue selected')
            game.select_clue(clue_square.clue)

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()
        elif event.keyval == clutter.keysyms.a:
            # player A rings in.
            game.buzz(0)
            self.update()
        elif event.keyval == clutter.keysyms.b:
            # player B rings in.
            game.buzz(1)
            self.update()
        elif event.keyval == clutter.keysyms.c:
            # player C rings in.
            game.buzz(2)
            self.update()
        elif event.keyval == clutter.keysyms.space:
            # multi-purpose bar press
            game.bar()
            self.update()
        elif event.keyval == clutter.keysyms.x:
            # cancel
            game.cancel()
            self.update()
        elif event.keyval == clutter.keysyms.y:
            # correct answer
            game.correct_answer()
            self.update()
        elif event.keyval == clutter.keysyms.n:
            # incorrect answer
            game.incorrect_answer()
            self.update()
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

    def on_tick(self):
        """
        Call back associated with each tick.
        """
        game.on_tick()
        self.update()
        return True

    def update(self):
        """
        Update the GUI based on the current state of the game.
        """
        if game.check_timeout_beep():
            logging.debug("****************** BZZZZZT! ******************")
        if game.check_flash_player_name():
            player_name = game.players[game.buzzed_player].name
            self.player_buzz_overlay.set_opacity(255)
            self.player_buzz_overlay.set_text(player_name)
            self.player_buzz_overlay.animate(clutter.EASE_IN_CUBIC,
                                             1000,
                                             'opacity', 0)
        if game.check_flash_player_score():
            player = game.players[game.buzzed_player]
            text = '%s\n$%d' % (player.name, player.score)
            self.player_buzz_overlay.set_opacity(255)
            self.player_buzz_overlay.set_text(text)
            self.player_buzz_overlay.animate(clutter.EASE_IN_CUBIC,
                                             1000,
                                             'opacity', 0)

        if game.state == game.IDLE:
            new_gui_state = self.SHOW_GAME_BOARD
        elif game.state in (game.DISPLAY_CLUE, game.AWAIT_BUZZ, game.AWAIT_ANSWER):
            new_gui_state = self.SHOW_CLUE
        elif game.state == game.DISPLAY_QUESTION:
            new_gui_state = self.SHOW_QUESTION
        else:
            logging.error('Invalid game state')

        if self.gui_state != new_gui_state:
            logging.debug("State %s to %s" % (self.gui_state, new_gui_state))
            if new_gui_state == self.SHOW_CLUE:
                self.clue_overlay.set_text(game.selected_clue.answer)
                self.clue_overlay.set_opacity(255)
                self.clue_overlay.animate(clutter.LINEAR,
                                          500,
                                          'width', self.get_width(),
                                          'height', self.get_height())
            elif new_gui_state == self.SHOW_QUESTION:
                self.clue_overlay.set_text(game.selected_clue.question)
                self.clue_overlay.set_opacity(255)
                self.clue_overlay.animate(clutter.LINEAR,
                                          500,
                                          'width', self.get_width(),
                                          'height', self.get_height())
            elif new_gui_state == self.SHOW_GAME_BOARD:
                logging.debug("Hiding clue overlay")
                self.clue_overlay.set_opacity(0)

            self.gui_state = new_gui_state

