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
Implementation of shadowed text.
"""

###############################################################################
## Imports
###############################################################################

import clutter
import logging
import re
from pango import ALIGN_CENTER


###############################################################################
## Classes
###############################################################################

class Text(clutter.Box):
    """
    Shadowed text.
    """

    def __init__(self, font, text):
        """
        """
        super(Text, self).__init__(clutter.FixedLayout())

        self.text = clutter.Text(font, text)
        self.text.set_line_alignment(ALIGN_CENTER)
        self.text.set_line_wrap(True)
        self.text.set_color(clutter.Color(255, 255, 255))

        self.shadow = clutter.Text(font, text)
        self.text.set_line_alignment(ALIGN_CENTER)
        self.text.set_line_wrap(True)
        self.shadow.set_color(clutter.Color(0, 0, 0))
        offset = int(self.font_size() / 24) + 2
        self.shadow.set_position(offset, offset)

        self.add(self.shadow)
        self.add(self.text)

    def font_size(self):
        """
        Return the font size or the number of points for the font.
        """
        font_size = 0
        font = self.text.get_font_name()
        match = re.search('\d+', font)
        if match:
            font_size = int(match.group().strip())
        return font_size

    def set_color(self, color):
        """
        Set the color of our text by passing this call off to the actual text.
        """
        self.text.set_color(color)

