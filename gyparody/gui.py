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
import cluttergst
import logging

from admin import Admin
from config import config
from game import game
from game_board import GameBoard
from game_board import ClueSquare
from game_buttons import game_buttons
from player_scores import PlayerScore, PlayerScoreBox
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
        self.set_color(config.square_background_color)
        self.clue_item = Text('', '')
        self.clue_item.set_size(self.get_width(), self.get_height())

    def set_audio(self, filename):
        """
        """
        self.remove(self.clue_item)
        tex = cluttergst.VideoTexture()
        tex.set_filename(filename)
        tex.set_playing(True)
        self.clue_item = Text(config.clue_overlay_font, 'Audio File')
        self.clue_item.set_size(self.get_width(), self.get_height())
        self.add(self.clue_item)

    def set_image(self, filename):
        """
        """
        self.remove(self.clue_item)
        self.clue_item = clutter.Texture(filename)
        self.add(self.clue_item)

    def set_text(self, text):
        """
        """
        self.remove(self.clue_item)
        self.clue_item.set_text(config.clue_overlay_font, text)
        self.clue_item.set_size(self.get_width(), self.get_height())
        self.add(self.clue_item)

    def set_video(self, filename):
        """
        """
        self.remove(self.clue_item)
        self.clue_item = cluttergst.VideoTexture()
        self.clue_item.set_filename(filename)
        self.clue_item.set_keep_aspect_ratio(True)
        #self.clue_item.set_height(config.fullscreen_height * 0.8)
        self.clue_item.set_width(config.fullscreen_width * 0.9)
        self.add(self.clue_item)
        self.clue_item.set_playing(True)

    def repeat(self):
        """
        """
        pass

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

        self.admin = Admin()

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
        self.connect('allocation-changed', self.on_allocation_changed)

        self.board_box = clutter.Box(clutter.BoxLayout())

        # Instantiate the game board which is the collection of squares to show
        # on screen.
        self.game_board = GameBoard()
        self.board_box.add(self.game_board)

        # Determine whether or not to display player scores.
        self.player_score_box = None
        if config.display_player_scores:
            self.player_score_box = PlayerScoreBox(game.get_players())
            board_box_layout = self.board_box.get_layout_manager()
            if config.player_scores_position == 'east':
                layout = self.player_score_box.get_layout_manager()
                layout.set_vertical(True)
                board_box_layout.pack(self.player_score_box,
                                      True, True, True,
                                      clutter.BOX_ALIGNMENT_CENTER,
                                      clutter.BOX_ALIGNMENT_CENTER)
            if config.player_scores_position == 'south':
                layout = self.player_score_box.get_layout_manager()
                layout.set_vertical(False)
                board_box_layout.pack(self.player_score_box,
                                      True, True, True,
                                      clutter.BOX_ALIGNMENT_CENTER,
                                      clutter.BOX_ALIGNMENT_CENTER)
            else:
                self.board_box.add(self.player_score_box)

        # Add the box with the board in it to the screen.
        self.add(self.board_box)

        # Overlay box for displaying clue information and answers
        self.clue_overlay = ClueOverlay()
        self.clue_overlay.set_size(self.get_width(), self.get_height())
        self.add(self.clue_overlay)
        self.clue_overlay.set_opacity(0)

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
            game_buttons.player_set(0, True)
            game.buzz(0)
            self.update()
        elif event.keyval == clutter.keysyms.b:
            # player B rings in.
            game_buttons.player_set(1, True)
            game.buzz(1)
            self.update()
        elif event.keyval == clutter.keysyms.c:
            # player C rings in.
            game_buttons.player_set(2, True)
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
        elif event.keyval == clutter.keysyms.z:
            logging.debug('resetting player lights')
            game_buttons.reset_player_lights()
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
        elif event.keyval == clutter.keysyms.p:
            # DEBUG - for testing end of round condition without clicking everything.
            # don't leave this active in production code!
            for category in game.categories:
                for clue in category.clues:
                    clue.state = 'selected'
            game.categories[0].clues[0].state = 'unanswered'
        elif event.keyval == clutter.keysyms.f:
            # Fullscreen play area.
            self.set_fullscreen(not self.get_fullscreen())

    def set_size(self, width, height):
        """
        """
        try:
            super(GUI, self).set_size(width, height)
            self.board_box.set_size(width, height)
            self.game_board.set_size(width * 0.9, height)
            self.category_overlay.set_size(width, height)
            self.player_buzz_overlay.set_size(width, height)
        except AttributeError:
            # If there is an attribute error then its most likely because
            # self.game_board did not exist because the stage is first
            # loading. Therefore we simply pass on this exception as during
            # loading correctly size of internals will be set.
            pass

    def on_allocation_changed(self, stage, box, flags):
        """
        """
        self.clue_overlay.set_size(self.get_width(), self.get_height())
        self.game_board.set_size(self.get_width() * 0.9, self.get_height())
        self.category_overlay.set_size(self.get_width(), self.get_height())
        self.player_buzz_overlay.set_size(self.get_width(), self.get_height())

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
        # Read incoming game button presses if they exist.
        player1, player2, player3 = game_buttons.read()
        if player1:
            game.buzz(0)
        elif player2:
            game.buzz(1)
        elif player3:
            game.buzz(2)
        game_buttons.reset_buttons()
        self.update()
        return True

    def update(self):
        """
        Update the GUI based on the current state of the game.
        """
        if game.check_update_game_board():
            self.remove(self.game_board)
            self.game_board = GameBoard()
            self.game_board.set_size(self.get_width(), self.get_height())
            self.add(self.game_board)
            self.game_board.lower_bottom()
        if game.check_timeout_beep():
            logging.debug("****************** BZZZZZT! ******************")
            tex = cluttergst.VideoTexture()
            tex.set_filename(config.sound_timeout)
            tex.set_playing(True)
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
                if game.selected_clue.get_type() == 'audio':
                    self.clue_overlay.set_audio(game.selected_clue.answer['audio'])
                elif game.selected_clue.get_type() == 'image':
                    self.clue_overlay.set_image(game.selected_clue.answer['image'])
                elif game.selected_clue.get_type() == 'text':
                    self.clue_overlay.set_text(game.selected_clue.answer)
                elif game.selected_clue.get_type() == 'video':
                    self.clue_overlay.set_video(game.selected_clue.answer['video'])
                self.clue_overlay.set_opacity(255)
                self.clue_overlay.set_scale(0.1, 0.1)
                self.clue_overlay.animate(clutter.LINEAR,
                                          500,
                                          'scale-x', 1,
                                          'scale-y', 1)
            elif new_gui_state == self.SHOW_QUESTION:
                self.clue_overlay.set_text(game.selected_clue.question)
                self.clue_overlay.set_opacity(255)
                self.clue_overlay.animate(clutter.LINEAR,
                                          500,
                                          'scale-x', 1,
                                          'scale-y', 1)
            elif new_gui_state == self.SHOW_GAME_BOARD:
                logging.debug("Hiding clue overlay")
                self.clue_overlay.set_opacity(0)

            self.gui_state = new_gui_state

