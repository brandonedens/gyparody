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

###############################################################################
## Classes
###############################################################################

class Admin(clutter.Stage):
    """
    """

    def __init__(self):
        super(Admin, self).__init__()

        self.set_fullscreen(False)
        self.set_size(400, 300)
        self.set_user_resizable(False)

        box = clutter.Box(clutter.BoxLayout())
        box.get_layout_manager().set_vertical(True)
        self.add(box)

        self.scores = []
        for i in range(3):
            box.add(clutter.Text(config.admin_font, 'Set player %d score:' % (i+1)))

            score = clutter.Text(config.admin_font, '%d'%i)
            score.player = i
            self.scores.append(score)
            score.set_activatable(True)
            score.set_reactive(True)
            score.set_editable(True)
            score.connect('button-release-event',
                lambda actor, event: self.set_key_focus(actor))
            score.connect('activate',
                lambda actor: self.set_score(actor.player))
            box.add(score)


        box.add(clutter.Text(config.admin_font, 'Daily Double Wager:'))
        self.wager = clutter.Text(config.admin_font, '0')
        self.wager.set_reactive(True)
        self.wager.set_editable(True)
        self.wager.connect('button-release-event',
            lambda actor, event: self.set_key_focus(self.wager))
        self.wager.connect('text-changed',
            lambda actor: game.set_daily_double_wager(self.get_wager()))
        box.add(self.wager)

        # Connect the callback listeners
        self.connect('key-press-event', self.on_press)

        self.show()

    def set_score(self, player):
        score = self.scores[player]
        print player
        try:
            s = int(score.get_text())
        except ValueError:
            return
        game.set_score(player, s)
        score.set_text('0')

    def on_press(self, actor, event):
        """
        """
        if event.keyval == clutter.keysyms.Escape:
            clutter.main_quit()

    def get_wager(self):
        try:
            return int(self.wager.get_text())
        except ValueError:
            return 0

