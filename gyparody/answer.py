# Brandon Edens
# 2010-03-20
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
from pango import ALIGN_CENTER

from config import config
from text import Text


###############################################################################
## Constants
###############################################################################

VALUE_FONT_COLOR = clutter.Color(217, 161, 71)

VALUE_FONT = "Haettenschweiler 64"

SAMPLE_TEXT = """DEAR SIR LANCELOT:
ARTHUR'S GONE
GRAILING. MEET ME
UNDER THE ROUND
TABLE AFTER
MATINS. XXO,
THIS QUEEN"""

###############################################################################
## Classes
###############################################################################

class Answer(clutter.Box):
    """
    """

    def __init__(self, answer, value):
        """
        """
        super(Answer, self).__init__(
            clutter.BinLayout(clutter.BIN_ALIGNMENT_CENTER,
                              clutter.BIN_ALIGNMENT_CENTER))
        self.set_color(config.square_background_color)

        self.answer = answer['answer']
        self.question = answer['question']

        self.text = Text(config.answer_value_font, "$%s" % value)
        self.text.set_color(VALUE_FONT_COLOR)
        self.add(self.text)

