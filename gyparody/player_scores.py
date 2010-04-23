# Brandon Edens
# 2010-04-22
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

from config import config
from text import Text


###############################################################################
## Classes
###############################################################################

class PlayerScore(clutter.Box):
    """
    Box containing player name and score.
    """

    def __init__(self, player):
        """
        """
        super(PlayerScore, self).__init__(clutter.BoxLayout())
        self.player = player
        layout = self.get_layout_manager()
        layout.set_vertical(True)
        self.player_name_text = Text(config.player_name_font,
                                     self.player.name)
        layout.pack(self.player_name_text,
                    True, False, False,
                    clutter.BOX_ALIGNMENT_CENTER,
                    clutter.BOX_ALIGNMENT_CENTER)
        self.player_score_text = Text(config.player_score_font,
                                      "$%d" % self.player.score)
        layout.pack(self.player_score_text,
                    True, False, False,
                    clutter.BOX_ALIGNMENT_CENTER,
                    clutter.BOX_ALIGNMENT_CENTER)
        self.set_color(config.square_background_color)

    def update(self):
        """
        Update the score information for player.
        """
        self.player_score_text.set_text(config.player_score_font,
                                        "$%d" % self.player.score)

class PlayerScoreBox(clutter.Box):
    """
    A box containing player names and scores.
    """

    def __init__(self, players):
        """
        """
        super(PlayerScoreBox, self).__init__(clutter.BoxLayout())
        self.set_color(clutter.Color(0, 255, 0))
        layout = self.get_layout_manager()
        layout.set_vertical(True)
        layout.set_spacing(30)

        for player in players:
            score_box = PlayerScore(player)
            layout.pack(score_box,
                        True, True, True,
                        clutter.BOX_ALIGNMENT_CENTER,
                        clutter.BOX_ALIGNMENT_CENTER)

    def update(self):
        """
        Update each player score.
        """
        for child in self.get_children():
            child.update()

